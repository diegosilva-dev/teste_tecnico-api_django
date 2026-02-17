# ERP – Módulo de Gestão de Pedidos

API REST para gestão de pedidos de um sistema ERP, desenvolvida como teste técnico para a vaga de **Desenvolvedor Backend Pleno**, com foco em **consistência, concorrência, arquitetura limpa e boas práticas de DevOps**.

---

## 🧩 Contexto

Este projeto implementa um módulo crítico de **Gestão de Pedidos**, garantindo:

- Controle transacional de estoque
- Idempotência na criação de pedidos
- Fluxo de status controlado
- Concorrência segura
- Arquitetura em camadas
- Testes automatizados
- Ambiente containerizado

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **Django**
- **Django Rest Framework (DRF)**
- **MySQL 8**
- **Redis 7**
- **Pytest**
- **Docker & Docker Compose**
- **Swagger / OpenAPI**

---

## 📐 Arquitetura

O projeto segue uma **arquitetura em camadas**, inspirada em Clean Architecture:

Controller (ViewSet)
→ Service (Regras de Negócio)
→ Repository (ORM / Banco)


### Princípios aplicados
- Separação de responsabilidades
- SOLID
- Regras de negócio isoladas da camada HTTP
- Transações ACID para operações críticas

Mais detalhes podem ser encontrados em `ARCHITECTURE.md`.

---

## 📂 Estrutura do Projeto
src/
├── core/
├── customers/
├── products/
├── orders/
│   ├── services/
│   ├── views.py
│   ├── models.py
├── tests/
│   ├── unit/
│   ├── integration/
docker-compose.yml
Dockerfile
.env.example
README.md
ARCHITECTURE.md


---

## 🚀 Como Rodar o Projeto Localmente

### 1️⃣ Pré-requisitos

- Docker
- Docker Compose

---

### 2️⃣ Configuração do ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env

---

### 3️⃣ Subir os containers

docker-compose up --build


A API estará disponível em: 
http://localhost:8000

---

📖 Documentação da API (Swagger)

http://localhost:8000/docs

---

❤️ Health Check

Endpoint de verificação de saúde: GET /health

Resposta esperada:

json

{
  "status": "ok"
}

---

🧪 Testes Automatizados (Rodar todos os testes)

docker-compose exec api pytest

👤 Autor
Desenvolvido por Diego Silva Giacomin
Teste Técnico – Desenvolvedor Backend Pleno