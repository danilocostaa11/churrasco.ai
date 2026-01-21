FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema para Pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta do Streamlit
EXPOSE 8501

# Configurar variáveis de ambiente padrão
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Comando de inicialização
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
