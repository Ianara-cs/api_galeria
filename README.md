# 📸 Sistema de Envio e Moderação de Fotos com Django

Este projeto é uma API desenvolvida com Django e Django REST Framework que permite o gerenciamento de usuários (admin e comuns), envio e moderação de fotos, sistema de curtidas e comentários. Ele também suporta upload múltiplo de imagens com integração ao Firebase ou armazenamento local.

---

## ✨ Funcionalidades

- 🔐 **Autenticação de usuários**
- 👥 **Administração de usuários** (criação, atualização, listagem)
- 📤 **Envio de fotos** (simples e múltiplo)
- ✅ **Moderação de fotos** (aprovar/reprovar)
- ❤️ **Curtir/Descurtir fotos**
- 💬 **Comentar em fotos**
- 🔎 **Filtros e paginação personalizada**
- ☁️ **Integração com Firebase Storage para produção**
- 🛡️ **Permissões por grupo (usuário comum vs. admin)**

---

## 💻 Front-end

O front-end da aplicação foi desenvolvido separadamente e está disponível no seguinte repositório:

🔗 **Repositório:** [https://github.com/Ianara-cs/front-galeria](https://github.com/Ianara-cs/front-galeria)


> O front-end foi desenvolvido com React.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- Django 4+
- Django REST Framework
- Firebase Admin SDK
- Django Filter
- UUID
- Pillow

---

## 🔐 Permissões e Acesso

- **Admin**:
  - Criar e editar usuários
  - Aprovar ou reprovar fotos
- **Usuário comum**:
  - Enviar fotos
  - Curtir e comentar em fotos aprovadas

---

## 🔄 Endpoints Principais

### 🔸 Usuários (`/api/usuarios/`)

| Método | Rota                 | Ação                     |
|--------|----------------------|--------------------------|
| GET    | `/`                  | Listar usuários          |
| POST   | `/`                  | Criar usuário            |
| PATCH  | `/:id/`              | Atualizar usuário        |
| GET    | `/me/`               | Dados do usuário logado  |

### 🔸 Fotos (`/api/fotos/`)

| Método | Rota                        | Ação                         |
|--------|-----------------------------|------------------------------|
| GET    | `/`                         | Listar fotos aprovadas       |
| POST   | `/`                         | Enviar uma nova foto         |
| POST   | `/upload-multiplas/`        | Upload de múltiplas fotos    |
| POST   | `/:id/aprovar/`             | Aprovar uma foto (admin)     |
| POST   | `/:id/reprovar/`            | Reprovar uma foto (admin)    |

### 🔸 Curtidas (`/api/curtidas/`)

| Método | Rota                         | Ação                |
|--------|------------------------------|---------------------|
| POST   | `/`                          | Curtir uma foto     |
| DELETE | `/foto/:foto_id/`           | Remover curtida     |

### 🔸 Comentários (`/api/comentarios/`)

| Método | Rota               | Ação                  |
|--------|--------------------|-----------------------|
| POST   | `/`                | Comentar em uma foto  |

---

## 🔐 Autenticação

Use autenticação via **token** (ex: JWT), conforme configuração do seu projeto.

---

## ☁️ Configuração de Armazenamento

No `settings.py`, configure:

```python
USE_FIREBASE_STORAGE = True  # ou False para uso local
FIREBASE_BUCKET_NAME = "nome-do-bucket"
```

---

## 🚀 Como Rodar Localmente

1. Clone o repositório:
```bash
git clone https://github.com/Ianara-cs/api_galeria.git
cd seu-projeto
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure variáveis de ambiente (.env ou settings.py) conforme necessário.

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

---

## 📸 Upload para Firebase

Para ativar o upload para Firebase:

- Crie um projeto no Firebase
- Gere uma chave do tipo **Admin SDK**
- Configure o Firebase com:
```python
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("caminho/para/firebase.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "nome-do-bucket"
})
```

---

## 👤 Autor

Desenvolvido por Ianara Costa – [@Ianara-cs](https://github.com/Ianara-cs)

---

## Como Rodar

Siga os passos abaixo para rodar o projeto localmente com Docker:

### Pré-requisitos

- Docker
- Docker Compose
- Arquivo `.env` com as variáveis de ambiente necessárias (exemplo abaixo)

### Variáveis de ambiente necessárias

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis (exemplo):

```env
SECRET_KEY=sua_chave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ALIAS=default
DB_ENGINE=django.db.backends.postgresql
DB_NAME=galeria
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db

DATABASE_URL=postgres://postgres:postgres@db:5432/galeria
SSL_REQUIRE=False

USE_FIREBASE_STORAGE=True
BUCKET_NAME=nome-do-seu-bucket

FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=seu_projeto
FIREBASE_PRIVATE_KEY_ID=sua_chave
FIREBASE_PRIVATE_KEY="sua_chave_privada"
FIREBASE_CLIENT_EMAIL=seu_email@projeto.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=seu_client_id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/...
FIREBASE_UNIVERSE_DOMAIN=googleapis.com
```

### Rodando com Docker

Execute os seguintes comandos:

```bash
# Subir os containers
docker-compose up --build

# O backend estará disponível em http://localhost:8000
```

### Rodando sem Docker

Se preferir executar localmente:

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar banco de dados e aplicar migrações
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Rodar o servidor
python manage.py runserver
```