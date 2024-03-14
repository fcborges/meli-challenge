# Use a imagem base do Python
FROM python:3.12

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /_init_

# Copie os requisitos de projeto e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copie o código-fonte para o contêiner
COPY . .

# Defina o comando padrão a ser executado quando o contêiner for iniciado
#CMD ["python", "_init_.py"]
CMD ["python", "_init_.py", "--host", "0.0.0.0"]
