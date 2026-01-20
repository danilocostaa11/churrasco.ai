import os
import base64
import json
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception


def get_openai_client():
    custom_key = os.environ.get("CUSTOM_OPENAI_API_KEY")
    if custom_key:
        return OpenAI(api_key=custom_key)
    
    ai_key = os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY")
    ai_base = os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")
    return OpenAI(api_key=ai_key, base_url=ai_base)


def is_rate_limit_error(exception: BaseException) -> bool:
    error_msg = str(exception)
    return (
        "429" in error_msg
        or "RATELIMIT_EXCEEDED" in error_msg
        or "quota" in error_msg.lower()
        or "rate limit" in error_msg.lower()
        or (hasattr(exception, "status_code") and exception.status_code == 429)
    )


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def gerar_lista_churrasco(descricao: str) -> dict:
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
    "total_estimado": valor total estimado em reais
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
    
    content = response.choices[0].message.content
    return json.loads(content)


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def extrair_itens_nota(image_bytes: bytes) -> dict:
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
    "total_nao_alcoolico": soma dos itens não alcoólicos
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
    
    content = response.choices[0].message.content
    return json.loads(content)


def calcular_divisao(itens: list, participantes: list, quem_bebeu: list) -> dict:
    total_alcoolico = sum(item['preco'] for item in itens if item.get('alcoolica', False))
    total_nao_alcoolico = sum(item['preco'] for item in itens if not item.get('alcoolica', False))
    total_geral = total_alcoolico + total_nao_alcoolico
    
    num_participantes = len(participantes)
    num_bebedores = len(quem_bebeu)
    
    if num_participantes == 0:
        return {"erro": "Nenhum participante informado"}
    
    valor_base = total_nao_alcoolico / num_participantes
    valor_alcool_por_pessoa = total_alcoolico / num_bebedores if num_bebedores > 0 else 0
    
    divisao = {}
    for pessoa in participantes:
        if pessoa in quem_bebeu:
            divisao[pessoa] = round(valor_base + valor_alcool_por_pessoa, 2)
        else:
            divisao[pessoa] = round(valor_base, 2)
    
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


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def gerar_cobranca_whatsapp(nome: str, valor: float, itens_consumidos: list = None, pix_key: str = "churrasco@pix.com") -> str:
    itens_texto = ""
    if itens_consumidos:
        itens_texto = f"Itens do rolê: {', '.join(itens_consumidos[:5])}"
    
    prompt = f"""Gere uma mensagem engraçada de cobrança no estilo brasileiro, informal, de um amigo cobrando outro depois de um churrasco.

Nome da pessoa: {nome}
Valor a pagar: R$ {valor:.2f}
{itens_texto}
Chave Pix: {pix_key}

A mensagem deve:
- Ser engraçada e amigável (estilo "boleiro")
- Mencionar o valor exato
- Incluir a chave Pix
- Usar emojis
- Não ser ofensiva
- Ter no máximo 3-4 linhas

Retorne APENAS a mensagem, sem aspas ou formatação extra."""

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um amigo brasileiro engraçado cobrando a galera do churrasco."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    
    return response.choices[0].message.content


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=64),
    retry=retry_if_exception(is_rate_limit_error),
    reraise=True
)
def gerar_cobranca_caloteiro(nome: str, valor: float, dias_atraso: int = 3) -> str:
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
    
    return response.choices[0].message.content
