# Usar uma imagem oficial do Ubuntu
FROM ubuntu:latest

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y wget unzip curl python3 python3-pip python3-venv

# Baixar e instalar o Chrome para Linux
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -fy

# Instalar o Chromedriver
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Criar e ativar um ambiente virtual Python
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Instalar Selenium e WebDriver Manager dentro do ambiente virtual
RUN pip install --no-cache-dir selenium webdriver-manager

# Definir diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar todos os arquivos do projeto para dentro do contêiner
COPY . /app

# Comando padrão para iniciar a aplicação
CMD ["python", "auto_aposta.py"]
