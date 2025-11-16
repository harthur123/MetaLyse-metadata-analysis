🚀 Guia da API MetaLyse para Frontend (Angular)

Este documento é o guia oficial para a integração entre o backend Flask e o frontend Angular do projeto MetaLyse.

1. Informações Gerais

    URL Base da API: http://127.0.0.1:5000/api/

    Formato dos Dados: Todas as requisições e respostas são em JSON, exceto o upload de arquivos.

    CORS: O backend já está configurado para aceitar requisições vindas de http://localhost:4200 (porta padrão do Angular).

2. 🔑 Fluxo de Autenticação (Obrigatório)

Quase todas as rotas são protegidas por JWT (JSON Web Token). O frontend precisa seguir este fluxo para acessar a API:

    Login: O usuário envia o e-mail e senha para a rota POST /api/auth/login.

    Armazenar Token: O backend responde com um access_token. O frontend deve salvar este token no localStorage do navegador.

    Enviar Token: Para todas as requisições futuras a rotas protegidas (Upload, Histórico, etc.), o Angular deve usar um HttpInterceptor para anexar este token ao cabeçalho (Header) da requisição.

        Cabeçalho: Authorization

        Valor: Bearer <token_salvo_no_localstorage>

3. Endpoints da API

Aqui estão todas as rotas (telas) que o frontend pode chamar.

👤 Autenticação (/api/auth)

Rotas para gerenciar o login, registro e contas de usuário.

POST /api/auth/register

    O que faz: Cria uma nova conta de usuário (normal).

    Proteção: Pública.

    Body (JSON):
    JSON

    {
      "username": "nome_do_usuario",
      "email": "usuario@email.com",
      "password": "SenhaForte123!"
    }

    Resposta Sucesso (201): {"message": "Usuário criado com sucesso!"}

    Respostas Erro:

        400 Bad Request: Campos faltando ou senha fraca.

        409 Conflict: E-mail ou username já cadastrado.

POST /api/auth/login

    O que faz: Autentica um usuário e retorna os tokens de acesso.

    Proteção: Pública.

    Body (JSON):
    JSON

{
  "email": "usuario@email.com",
  "password": "SenhaForte123!"
}

Resposta Sucesso (200):
JSON

    {
      "access_token": "eyJhbGciOiJIUz...",
      "refresh_token": "eyJ0eXAiOiJKV...",
      "user_role": "admin" // (ou "user")
    }

    Resposta Erro (401 Unauthorized): {"message": "Email ou senha inválidos"}

GET /api/auth/me

    O que faz: Busca os dados do usuário atualmente logado (útil para o "Olá, Harthur" no menu).

    Proteção: JWT Obrigatório.

    Headers: Authorization: Bearer <token>

    Resposta Sucesso (200):
    JSON

    {
      "id": 1,
      "username": "harthur",
      "email": "harthurhenrique214@gmail.com",
      "role": "admin"
    }

POST /api/auth/logout

    O que faz: Invalida o token de acesso atual (adiciona à blocklist).

    Proteção: JWT Obrigatório.

    Headers: Authorization: Bearer <token>

    Body: Vazio.

    Resposta Sucesso (200): {"message": "Logout bem-sucedido. O token foi invalidado."}

POST /api/auth/reset-password-request

    O que faz: Inicia o fluxo de "esqueci a senha". O backend enviará o e-mail.

    Proteção: Pública.

    Body (JSON):
    JSON

    {
      "email": "usuario_que_esqueceu@email.com"
    }

    Resposta Sucesso (200): {"message": "Se o email estiver cadastrado, um link será enviado."}

POST /api/auth/reset-password

    O que faz: Define a nova senha. O frontend deve pegar o token da URL (que o usuário clicou no e-mail) e enviá-lo no corpo.

    Proteção: Pública.

    Body (JSON):
    JSON

    {
      "token": "TOKEN_QUE_VEIO_NA_URL_DO_EMAIL",
      "new_password": "NovaSenhaForte456!"
    }

    Resposta Sucesso (200): {"message": "Senha atualizada com sucesso!"}

📤 Upload de Metadados (/api/metadata)

Rota principal para a análise de arquivos.

POST /api/metadata/upload

    O que faz: Envia um arquivo (PDF ou JPG) para análise. O arquivo físico é deletado após a análise.

    Proteção: JWT Obrigatório.

    Headers: Authorization: Bearer <token>

    Body: Atenção! Não é JSON. Deve ser form-data. O frontend (Angular) deve usar FormData.

        Key: file

        Value: (O arquivo .pdf ou .jpg que o usuário selecionou)

    Resposta Sucesso (201):
    JSON

    {
      "message": "Upload e extração concluídos com sucesso!",
      "file": {
        "nome": "Curriculo.pdf",
        "tipo": "application/pdf",
        "tamanho_bytes": 216739,
        "hash": "a4996a90999..."
      },
      "metadados_extraidos": {
        "Author": "Harthur",
        "Creator": "Microsoft Word 2016",
        "page_count": "1"
        // ... ou os dados do exiftool para JPEGs
      }
    }

📋 Consulta de Histórico (/api/history)

Rotas para o "Caso de Uso: Histórico" (Visão de Usuário e Admin).

GET /api/history/me

    O que faz: Retorna o histórico de uploads apenas do usuário logado.

    Proteção: JWT Obrigatório.

    Headers: Authorization: Bearer <token>

    Filtro (Opcional): Para implementar a barra de busca (A.4), adicione um parâmetro na URL.

        Exemplo: /api/history/me?search=Curriculo

    Resposta Sucesso (200): Uma lista de registros.
    JSON

    [
      {
        "id": 1,
        "nome_arquivo": "Curriculo.pdf",
        "tipo_arquivo": "application/pdf",
        "tamanho_bytes": 216739,
        "data_analise": "2025-11-14T19:40:00",
        "hash": "a4996a90999...",
        "usuario_responsavel": "harthur",
        "metadados_extraidos": { ... }
      }
    ]

GET /api/history/all

    O que faz: (SÓ PARA ADMINS) Retorna o histórico de todos os usuários.

    Proteção: JWT Obrigatório (e o usuário deve ter role: "admin")

    Headers: Authorization: Bearer <token>

    Filtro (Opcional): O admin pode buscar por nome de arquivo ou nome de usuário (A.2).

        Exemplo: /api/history/all?search=outro_usuario

    Resposta Sucesso (200): Uma lista de registros (mesmo formato do /me).

    Resposta Erro (403 Forbidden): {"message": "Acesso negado. Requer privilégios de administrador."}

GET /api/history/<id>

    O que faz: Pega os detalhes de um registro específico (para "expandir" o registro).

    Proteção: JWT Obrigatório.

    Headers: Authorization: Bearer <token>

    Resposta Sucesso (200): Um único objeto de registro (mesmo formato do /me).

    Resposta Erro (404 Not Found): {"message": "Registro não encontrado ou acesso não autorizado."}

⚠️ Resumo de Erros Comuns

    400 Bad Request: JSON mal formatado ou campos faltando (ex: password faltando no login).

    401 Unauthorized: O usuário tentou acessar uma rota protegida sem enviar um Authorization header.

    403 Forbidden: O usuário está logado, mas não é um admin (ex: tentou acessar /api/history/all).

    404 Not Found: A URL está errada (ex: /api/register em vez de /api/auth/register).

    422 Unprocessable Entity: O Authorization header foi enviado, mas o token está expirado, inválido ou foi revogado (logout).