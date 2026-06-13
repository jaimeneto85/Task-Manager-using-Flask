# Este estágio serve apenas para compilar e preparar as dependências
FROM python:3.12-alpine AS builder
WORKDIR /app
RUN apk add --no-cache gcc musl-dev libffi-dev
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Este estágio é a imagem final que será usada para rodar a aplicação
FROM python:3.12-alpine
WORKDIR /app
# Criando um usuário não-root para rodar a aplicação de forma mais segura
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /root/.local /home/appuser/.local
COPY todo_project/ .
# Ajustando as permissões para o usuário não-root
RUN chown -R appuser:appgroup /app
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
# Definindo a variável de ambiente para produção
ENV FLASK_ENV=production
# Exponndo a porta que a aplicação Flask usará
EXPOSE 5000
# Comando para rodar a aplicação
CMD ["python", "run.py"]