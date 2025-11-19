🎨 MetaLyse - Frontend (Interface Angular)

Esta é a interface de usuário do projeto MetaLyse, desenvolvida em Angular (v16+). Ela oferece uma experiência visual moderna para realizar uploads, visualizar metadados complexos e gerenciar o histórico de análises.

A aplicação utiliza Angular Material para componentes visuais e se comunica via HTTP com a API Flask.

📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

    Node.js (Versão 16 ou superior recomendada)

    NPM (Gerenciador de pacotes, vem com o Node)

🚀 Instalação e Execução (Passo a Passo)

Siga estes passos para iniciar a interface.

1. Entre na Pasta

Abra o terminal e navegue até a pasta do frontend:
Bash

cd frontend

2. Instale as Dependências

Isso vai baixar o Angular e todas as bibliotecas necessárias (Material, RxJS, etc.) listadas no package.json.
Bash

npm install

(Isso pode levar alguns minutos).

3. Inicie o Servidor de Desenvolvimento

Bash

npm start

Ou, se preferir usar o CLI direto: ng serve

🔗 Conectando ao Backend

    ⚠️ IMPORTANTE: O Frontend não funciona sozinho. Ele precisa que o servidor Python esteja rodando.

    Certifique-se de que o backend está online em: http://127.0.0.1:5000/

🖥️ Acessando a Aplicação

Após iniciar o comando acima, abra seu navegador e acesse:

👉 http://localhost:4200/

🛠️ Solução de Problemas Comuns

    Erro de CORS ou Conexão Recusada:

        Verifique se o Backend (python run.py) está rodando.

        Verifique se o Backend está na porta 5000.

    Erro 401 Unauthorized no Upload:

        Seu token expirou. Faça Logout e Login novamente para renovar sua sessão.

    Tela em Branco ou Erro de Módulo:

        Tente parar o servidor (Ctrl+C) e rodar npm install novamente para garantir que nenhuma biblioteca ficou faltando.
