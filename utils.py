import os
import base64
import json
import io
import hashlib
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

# OpenAI é opcional para permitir que o app suba mesmo sem a lib instalada
try:
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore[assignment]

# Tentar importar qrcode, se não existir, criar fallback
try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


def get_openai_client():
    """Obtém cliente OpenAI com fallback para diferentes fontes de API key."""
    if OpenAI is None:
        raise ImportError(
            "Pacote 'openai' não instalado. Instale com `pip install -r requirements.txt` "
            "ou `uv sync` antes de usar as funções de IA."
        )

    # Primeiro, tenta chave customizada do usuário
    custom_key = os.environ.get("CUSTOM_OPENAI_API_KEY")
    if custom_key:
        return OpenAI(api_key=custom_key)
    
    # Segundo, tenta variável de ambiente padrão
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return OpenAI(api_key=env_key)
    
    # Terceiro, tenta Replit AI Integrations
    ai_key = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
    ai_base = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")
    if ai_key and ai_base:
        return OpenAI(api_key=ai_key, base_url=ai_base)
    
    raise ValueError("Nenhuma API key configurada. Configure OPENAI_API_KEY ou use a sidebar.")


def is_rate_limit_error(exception: BaseException) -> bool:
    """Verifica se é erro de rate limit para retry."""
    error_msg = str(exception)
    return (
        "429" in error_msg
        or "RATELIMIT_EXCEEDED" in error_msg
        or "quota" in error_msg.lower()
        or "rate limit" in error_msg.lower()
        or (hasattr(exception, "status_code") and exception.status_code == 429)
    )


# ============================================
# FUNÇÕES DE GERAÇÃO DE LISTA DE CHURRASCO
# ============================================

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def gerar_lista_churrasco(descricao: str) -> dict:
    """Gera lista de compras inteligente baseada na descrição do churrasco."""
    prompt = f"""Você é um especialista em churrascos brasileiros, manja tudo de carne, bebida e quantidade!

O usuário descreveu o churrasco assim:
"{descricao}"

Analise o contexto (número de pessoas, duração, se bebem muito ou pouco, homens/mulheres, etc) e calcule as quantidades ideais.

Regras de cálculo:
- Carne: média 400g por homem, 300g por mulher, 200g por criança
- Se durar mais de 4 horas, aumente 20%
- Cerveja: 1 litro por pessoa que bebe (se "bebem muito", 1.5L)
- Refrigerante: 500ml por pessoa
- Água: 500ml por pessoa
- Carvão: 1kg para cada 2kg de carne
- Pão de alho: 2 unidades por pessoa
- Gelo: 2kg para cada 5 pessoas

Retorne APENAS um JSON válido neste formato (sem markdown, só o JSON puro):
{{
    "resumo": "texto resumindo o churrasco de forma engraçada e informal",
    "pessoas": número total estimado,
    "duracao_estimada": "ex: 4 horas",
    "carnes": [
        {{"item": "Picanha", "quantidade": "2kg", "preco_estimado": 150.00}},
        {{"item": "Linguiça Toscana", "quantidade": "1kg", "preco_estimado": 25.00}}
    ],
    "bebidas": [
        {{"item": "Cerveja Brahma Lata", "quantidade": "24 unidades", "preco_estimado": 80.00, "alcoolica": true}},
        {{"item": "Coca-Cola 2L", "quantidade": "3 unidades", "preco_estimado": 30.00, "alcoolica": false}}
    ],
    "acompanhamentos": [
        {{"item": "Pão de Alho", "quantidade": "20 unidades", "preco_estimado": 25.00}},
        {{"item": "Farofa pronta", "quantidade": "500g", "preco_estimado": 8.00}}
    ],
    "carvao_gelo": [
        {{"item": "Carvão", "quantidade": "5kg", "preco_estimado": 25.00}},
        {{"item": "Gelo", "quantidade": "4kg", "preco_estimado": 16.00}}
    ],
    "total_estimado": valor total estimado em reais,
    "dicas": ["dica 1 sobre o churrasco", "dica 2"]
}}"""

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é o Mestre do Churrasco. Responda sempre em JSON válido, sem markdown."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        max_tokens=2000
    )
    
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


# ============================================
# FUNÇÕES DE EXTRAÇÃO DE NOTA FISCAL
# ============================================

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def extrair_itens_nota(image_bytes: bytes) -> dict:
    """Extrai itens de uma foto de nota fiscal usando Vision."""
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = """Analise esta nota fiscal/cupom de supermercado e extraia TODOS os itens com seus preços.

Classifique cada item como:
- "alcoolica": true se for bebida alcoólica (cerveja, vinho, vodka, whisky, cachaça, etc)
- "alcoolica": false para todo o resto

Retorne APENAS um JSON válido neste formato (sem markdown):
{
    "itens": [
        {"nome": "PICANHA KG", "preco": 89.90, "alcoolica": false},
        {"nome": "BRAHMA LATA 350ML", "preco": 3.50, "alcoolica": true},
        {"nome": "COCA COLA 2L", "preco": 9.90, "alcoolica": false}
    ],
    "total_nota": valor total da nota se visível,
    "total_alcoolico": soma dos itens alcoólicos,
    "total_nao_alcoolico": soma dos itens não alcoólicos,
    "estabelecimento": "nome do estabelecimento se visível",
    "data_compra": "data da compra se visível"
}

Se não conseguir ler algum valor, faça sua melhor estimativa.
Se a imagem não for uma nota fiscal, retorne: {"erro": "Não consegui identificar uma nota fiscal nesta imagem"}"""

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=2000
    )
    
    content = response.choices[0].message.content or "{}"
    return json.loads(content)


# ============================================
# FUNÇÕES DE CÁLCULO DE DIVISÃO
# ============================================

def calcular_divisao(itens: list, participantes: list, quem_bebeu: list) -> dict:
    """Calcula a divisão justa da conta."""
    total_alcoolico = sum(item['preco'] for item in itens if item.get('alcoolica', False))
    total_nao_alcoolico = sum(item['preco'] for item in itens if not item.get('alcoolica', False))
    total_geral = total_alcoolico + total_nao_alcoolico
    
    num_participantes = len(participantes)
    num_bebedores = len(quem_bebeu)
    
    if num_participantes == 0:
        return {"erro": "Nenhum participante informado"}
    
    valor_base = total_nao_alcoolico / num_participantes
    valor_alcool_por_pessoa = total_alcoolico / num_bebedores if num_bebedores > 0 else total_alcoolico / num_participantes
    
    divisao = {}
    for pessoa in participantes:
        if num_bebedores > 0:
            valor_pessoa = valor_base + valor_alcool_por_pessoa if pessoa in quem_bebeu else valor_base
        else:
            # Nobody marked as drinker: split everything equally
            valor_pessoa = valor_base + valor_alcool_por_pessoa
        divisao[pessoa] = round(valor_pessoa, 2)
    
    return {
        "total_geral": round(total_geral, 2),
        "total_alcoolico": round(total_alcoolico, 2),
        "total_nao_alcoolico": round(total_nao_alcoolico, 2),
        "num_participantes": num_participantes,
        "num_bebedores": num_bebedores,
        "valor_base_por_pessoa": round(valor_base, 2),
        "valor_alcool_por_bebedor": round(valor_alcool_por_pessoa, 2),
        "divisao": divisao
    }


# ============================================
# FUNÇÕES DE COBRANÇA WHATSAPP
# ============================================

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def gerar_cobranca_whatsapp(nome: str, valor: float, itens_consumidos: list | None = None, pix_key: str = "churrasco@pix.com", bebeu: bool = False) -> str:
    """Gera mensagem amigável de cobrança com personalidade Sincera."""
    itens_texto = ""
    if itens_consumidos:
        itens_texto = f"Itens do rolê: {', '.join(itens_consumidos[:5])}"
    
    comportamento_bebida = "Essa pessoa BEBEU álcool (provável ressaca hoje)." if bebeu else "Essa pessoa NÃO bebeu álcool (só prejuízo na comida)."

    prompt = f"""Gere uma mensagem de cobrança para:
Nome: {nome}
Valor: R$ {valor:.2f}
Status: {comportamento_bebida}
{itens_texto}
Chave Pix: {pix_key}

Siga RIGOROSAMENTE sua personalidade de Churrasqueiro Sincerão."""

    system_prompt = """Você é o 'Churrasqueiro Sincerão'. Sua missão é cobrar os amigos do churrasco no WhatsApp.

PERSONALIDADE:
Brasileiro, engraçado, usa gírias (tipo "meu consagrado", "chefia", "campeão"), levemente irônico, mas amigo.

REGRAS DE CLASSIFICAÇÃO:
1. Se a pessoa BEBEU:
   - Faça piadas sobre a ressaca brava de hoje.
   - Diga que ela bebeu "como se não houvesse amanhã".
   - Ameaçe (zoeira) servir cerveja quente ou no copo de requeijão na próxima se não pagar.

2. Se a pessoa NÃO BEBEU:
   - Faça piadas sobre o prejuízo que ela deu na picanha/carne.
   - Brinque que "comeu por três" ou que estava "com a lombriga solta".
   - Diga que ser sóbrio custa caro também.

OBRIGATÓRIO NA MENSAGEM:
- O valor exato (R$).
- A Chave Pix.
- Emojis divertidos.
- Máximo de 4-5 linhas.

Exemplo (Bebeu):
"Fala Betão, meu consagrado! 🍺 Ontem tu bebeu como se não houvesse amanhã, mas o amanhã chegou e a conta também! O prejuízo da sua alegria ficou em R$ 85,00. Faz esse Pix cair logo senão na próxima tua cerveja vem quente! 🤡
💸 Pix: 1199999-9999"

Exemplo (Não Bebeu):
"Grande Ana! 🥩 Mandou bem na picanha ontem hein, prejuízo puro! Como tu não bebeu, sobrou espaço pra carne né? A conta desse banquete ficou em R$ 50,00. Manda o Pix pra garantir a vaga no próximo! 😉
💸 Pix: nomedopix@email.com"
"""

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )
    
    return response.choices[0].message.content or ""


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def gerar_cobranca_caloteiro(nome: str, valor: float, dias_atraso: int = 3) -> str:
    """Gera mensagem de cobrança para caloteiros."""
    prompt = f"""Gere uma mensagem MUITO engraçada de cobrança para um "caloteiro" depois de um churrasco.

Nome: {nome}
Valor: R$ {valor:.2f}
Dias de atraso: {dias_atraso}

A mensagem deve:
- Ser hilária e no estilo zoeira de amigos
- Fazer pressão cômica (tipo ameaçar contar pra galera)
- Usar gírias brasileiras
- Usar emojis
- Não ser realmente ofensiva
- Ter no máximo 4-5 linhas

Exemplo de tom: "Fala Pedro! A Picanha já foi digerida e virou saudade, mas o Pix ainda não caiu..."

Retorne APENAS a mensagem, sem aspas."""

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um mestre da zueira cobrando o caloteiro do churrasco."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400
    )
    
    return response.choices[0].message.content or ""


# ============================================
# FUNÇÕES DE QR CODE PIX
# ============================================

def gerar_payload_pix(chave_pix: str, nome_recebedor: str, cidade: str, valor: float, descricao: str = "") -> str:
    """
    Gera payload do Pix no formato EMV.
    Baseado na especificação do Banco Central do Brasil.
    """
    def formatar_campo(id_campo: str, valor_campo: str) -> str:
        tamanho = str(len(valor_campo)).zfill(2)
        return f"{id_campo}{tamanho}{valor_campo}"
    
    # Limpar e formatar valores
    nome_recebedor = nome_recebedor[:25].upper()
    cidade = cidade[:15].upper()
    valor_formatado = f"{valor:.2f}"
    
    # Merchant Account Information (campo 26)
    gui = formatar_campo("00", "br.gov.bcb.pix")
    chave = formatar_campo("01", chave_pix)
    if descricao:
        desc = formatar_campo("02", descricao[:25])
        mai = formatar_campo("26", gui + chave + desc)
    else:
        mai = formatar_campo("26", gui + chave)
    
    # Additional Data Field (campo 62)
    txid = formatar_campo("05", "***")
    adf = formatar_campo("62", txid)
    
    # Montar payload sem CRC
    payload = (
        formatar_campo("00", "01") +  # Payload Format Indicator
        formatar_campo("01", "12") +  # Point of Initiation (12 = QR dinâmico)
        mai +
        formatar_campo("52", "0000") +  # Merchant Category Code
        formatar_campo("53", "986") +   # Transaction Currency (986 = BRL)
        formatar_campo("54", valor_formatado) +
        formatar_campo("58", "BR") +    # Country Code
        formatar_campo("59", nome_recebedor) +
        formatar_campo("60", cidade) +
        adf +
        "6304"  # CRC placeholder
    )
    
    # Calcular CRC16 CCITT
    crc = calcular_crc16(payload)
    
    return payload + crc


def calcular_crc16(payload: str) -> str:
    """Calcula CRC16 CCITT para o payload Pix."""
    crc = 0xFFFF
    for byte in payload.encode('utf-8'):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return format(crc, '04X')


def gerar_qrcode_pix(chave_pix: str, nome_recebedor: str, cidade: str, valor: float, descricao: str = "") -> bytes | None:
    """Gera imagem do QR Code Pix."""
    if not HAS_QRCODE:
        return None
    
    payload = gerar_payload_pix(chave_pix, nome_recebedor, cidade, valor, descricao)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Converter para bytes
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return buffer.getvalue()


def gerar_link_pix_copia_cola(chave_pix: str, nome_recebedor: str, cidade: str, valor: float, descricao: str = "") -> str:
    """Gera o código Pix Copia e Cola."""
    return gerar_payload_pix(chave_pix, nome_recebedor, cidade, valor, descricao)


# ============================================
# FUNÇÕES DE HISTÓRICO E TEMPLATES
# ============================================

def gerar_id_churrasco() -> str:
    """Gera ID único para o churrasco."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_part = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:6]
    return f"churras_{timestamp}_{hash_part}"


def salvar_historico_local(historico: dict) -> dict:
    """Prepara dados do histórico para salvar (retorna dict para session_state)."""
    return {
        "id": gerar_id_churrasco(),
        "data_criacao": datetime.now().isoformat(),
        "dados": historico
    }


def criar_template_churrasco(nome: str, lista: dict) -> dict:
    """Cria um template reutilizável de churrasco."""
    return {
        "nome": nome,
        "criado_em": datetime.now().isoformat(),
        "pessoas_base": lista.get("pessoas", 10),
        "carnes": [item["item"] for item in lista.get("carnes", [])],
        "bebidas": [item["item"] for item in lista.get("bebidas", [])],
        "acompanhamentos": [item["item"] for item in lista.get("acompanhamentos", [])],
        "proporcoes": {
            "carne_por_pessoa_kg": 0.35,
            "cerveja_por_pessoa_l": 1.0,
            "refri_por_pessoa_l": 0.5
        }
    }


# ============================================
# TEMPLATES PRÉ-DEFINIDOS
# ============================================

TEMPLATES_PADRAO = {
    "tradicional": {
        "nome": "🥩 Churrasco Tradicional",
        "descricao": "O clássico! Picanha, linguiça, cerveja e refrigerante.",
        "pessoas_base": 10,
        "carnes": ["Picanha", "Linguiça Toscana", "Fraldinha", "Coração de Frango"],
        "bebidas_alcool": ["Cerveja Lata 350ml"],
        "bebidas_sem": ["Coca-Cola 2L", "Guaraná 2L", "Água 500ml"],
        "acompanhamentos": ["Pão de Alho", "Farofa", "Vinagrete", "Queijo Coalho"]
    },
    "premium": {
        "nome": "👑 Churrasco Premium",
        "descricao": "Para impressionar! Cortes nobres e drinks especiais.",
        "pessoas_base": 10,
        "carnes": ["Picanha Angus", "Ancho", "Costela Premium", "Cordeiro"],
        "bebidas_alcool": ["Cerveja Artesanal", "Vinho Tinto"],
        "bebidas_sem": ["Água com Gás", "Suco Natural", "Refrigerante Premium"],
        "acompanhamentos": ["Pão de Alho Recheado", "Chimichurri", "Salada Caprese", "Bruschetta"]
    },
    "economico": {
        "nome": "💰 Churrasco Econômico",
        "descricao": "Bom e barato! Sabor sem gastar muito.",
        "pessoas_base": 10,
        "carnes": ["Linguiça Calabresa", "Frango", "Cupim", "Acém"],
        "bebidas_alcool": ["Cerveja Popular"],
        "bebidas_sem": ["Refrigerante 2L", "Suco em Pó"],
        "acompanhamentos": ["Pão Francês", "Farofa Pronta", "Cebola", "Limão"]
    },
    "vegetariano": {
        "nome": "🥗 Churrasco Vegetariano",
        "descricao": "Delícias da grelha sem carne!",
        "pessoas_base": 10,
        "carnes": [],
        "vegetais": ["Queijo Coalho", "Abacaxi", "Cogumelos", "Berinjela", "Abobrinha", "Tofu Marinado"],
        "bebidas_alcool": ["Cerveja", "Vinho Branco"],
        "bebidas_sem": ["Suco Natural", "Água de Coco", "Refrigerante"],
        "acompanhamentos": ["Hummus", "Salada Mediterrânea", "Pão Sírio", "Guacamole"]
    }
}


def aplicar_template(template_id: str, num_pessoas: int) -> dict:
    """Aplica um template ajustando para o número de pessoas."""
    if template_id not in TEMPLATES_PADRAO:
        return {"erro": "Template não encontrado"}
    
    template = TEMPLATES_PADRAO[template_id]
    fator = num_pessoas / template["pessoas_base"]
    
    return {
        "template_usado": template["nome"],
        "pessoas": num_pessoas,
        "ajuste": f"Quantidades ajustadas de {template['pessoas_base']} para {num_pessoas} pessoas",
        "fator_multiplicador": round(fator, 2)
    }
