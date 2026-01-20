# Churrasco.ai 🥩

Aplicação web mobile-first para organizar churrascos de forma divertida e sem burocracia.

## Visão Geral

O Churrasco.ai resolve dois problemas principais:
1. **Planejar o churras**: Calcula a lista de compras ideal baseado na descrição natural do evento
2. **Rachar a conta**: Divide a conta de forma justa (quem não bebeu não paga a cerveja!)

## Stack Técnica

- **Frontend/Backend**: Streamlit (Python)
- **IA/Inteligência**: OpenAI API (GPT-4o) via Replit AI Integrations
- **Manipulação de Imagem**: Pillow (PIL)
- **Retry/Rate Limiting**: Tenacity

## Estrutura do Projeto

```
├── app.py              # Interface principal Streamlit
├── utils.py            # Funções de IA e cálculos
├── pyproject.toml      # Dependências Python
└── .streamlit/
    └── config.toml     # Configuração do Streamlit
```

## Funcionalidades

### Tab 1: Planejar o Rolê
- Input em linguagem natural (ex: "10 amigos, sábado à tarde, bebem muito")
- IA calcula quantidades de carnes, bebidas, acompanhamentos
- Mostra estimativa de preços

### Tab 2: Rachar a Conta
- Upload de foto da nota fiscal
- IA (Vision) extrai itens e preços
- Seleção de participantes com checkbox "Bebeu Álcool?"
- Divisão justa: itens comuns divididos por todos, álcool só por quem bebeu
- Geração de mensagens de cobrança para WhatsApp com piadas

## Configuração

O app usa Replit AI Integrations (não precisa de chave API própria). As variáveis de ambiente são gerenciadas automaticamente:
- `AI_INTEGRATIONS_OPENAI_API_KEY`
- `AI_INTEGRATIONS_OPENAI_BASE_URL`

## Execução

```bash
streamlit run app.py --server.port 5000
```

## Design System

- **Estilo**: Mobile-first, moderno, uso de emojis
- **Tom de Voz**: Informal, estilo "boleiro" brasileiro
- **Cores**: Gradientes laranja/roxo, cards com bordas coloridas

## Próximos Passos (Roadmap)

- [ ] QR Code Pix dinâmico
- [ ] Histórico de churrascos (banco de dados)
- [ ] Templates de churrasco salvos
- [ ] Links de afiliados (Zé Delivery, açougues)
