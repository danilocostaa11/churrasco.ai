# Churrasco.ai 🥩

<div align="center">

![Churrasco.ai](https://img.shields.io/badge/Churrasco.ai-v2.0-ff6b35?style=for-the-badge&logo=fire&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**Organize seu churrasco sem burocracia, parça!** 🔥

[Demo](https://churrasco-ai.streamlit.app) · [Reportar Bug](https://github.com/seu-user/churrasco-ai/issues) · [Sugerir Feature](https://github.com/seu-user/churrasco-ai/issues)

</div>

---

## 🎯 O Problema que Resolvemos

Organizar churrasco é trabalhoso:
- Quanto de carne comprar para 15 pessoas?
- Quem bebeu cerveja paga igual quem só tomou água?
- Como cobrar o caloteiro sem ser chato?

**Churrasco.ai resolve tudo isso com IA!**

---

## ✨ Features

### 🥩 Planejador Inteligente
- Descreva seu churrasco em linguagem natural
- IA calcula quantidades ideais de carnes, bebidas e acompanhamentos
- Estimativa de preços atualizada

### 💰 Divisão Justa da Conta
- Tire foto da nota fiscal
- IA extrai todos os itens automaticamente
- Quem não bebeu álcool não paga cerveja!
- Divisão matemática perfeita

### 📲 Cobrança no WhatsApp
- Mensagens engraçadas geradas por IA
- Modo "Caloteiro" para os atrasados
- **QR Code Pix dinâmico** para pagamento instantâneo
- Pix Copia e Cola

### 📋 Templates Prontos
- Tradicional, Premium, Econômico, Vegetariano
- Crie e salve seus próprios templates

---

## 🚀 Quick Start

### Pré-requisitos
- Python 3.11 ou superior
- Chave de API da OpenAI

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/seu-user/churrasco-ai.git
cd churrasco-ai

# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure sua API key
cp .env.example .env
# Edite .env e adicione sua OPENAI_API_KEY

# Execute o app
streamlit run app.py
```

Acesse: http://localhost:8501

---

## 🌐 Deploy

### Streamlit Cloud (Recomendado)

1. Fork este repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu GitHub
4. Selecione o repositório e branch `main`
5. Configure o secret `OPENAI_API_KEY` em Settings > Secrets
6. Deploy!

### Railway

```bash
# Instale Railway CLI
npm install -g @railway/cli

# Login e deploy
railway login
railway init
railway up
```

Configure a variável `OPENAI_API_KEY` no dashboard do Railway.

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `OPENAI_API_KEY` | Chave da API OpenAI | ✅ |
| `DEFAULT_PIX_KEY` | Chave Pix padrão | ❌ |
| `DEFAULT_ORGANIZER_NAME` | Nome do organizador | ❌ |

### Usando na Interface

Você também pode configurar a API Key diretamente na sidebar do app.

---

## 📁 Estrutura do Projeto

```
churrasco-ai/
├── app.py              # Interface principal Streamlit
├── utils.py            # Funções de IA, cálculos e Pix
├── requirements.txt    # Dependências Python
├── pyproject.toml      # Configuração do projeto
├── .env.example        # Exemplo de variáveis de ambiente
├── .gitignore          # Arquivos ignorados pelo Git
├── .streamlit/
│   └── config.toml     # Configuração do Streamlit
└── README.md           # Este arquivo
```

---

## 🛣️ Roadmap

- [x] Planejador de churrasco com IA
- [x] Leitor de nota fiscal (Vision)
- [x] Divisão justa da conta
- [x] Mensagens de cobrança engraçadas
- [x] QR Code Pix dinâmico
- [x] Templates de churrasco
- [x] Design premium dark mode
- [ ] Histórico persistente (banco de dados)
- [ ] Integração com Zé Delivery
- [ ] App mobile nativo
- [ ] Suporte a PIX com valor variável

---

## 🤝 Contribuindo

Contribuições são bem-vindas!

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova feature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👨‍💻 Autor

Feito com 🔥 no Brasil

---

<div align="center">

**Se esse projeto te ajudou, deixa uma ⭐!**

</div>
