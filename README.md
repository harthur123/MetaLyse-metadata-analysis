🔍 MetaLyse - Sistema de Análise de Metadados

    ⚠️ DOCUMENTAÇÃO TÉCNICA DETALHADA Este projeto é modular. Para detalhes específicos de instalação, dependências e solução de erros, consulte os arquivos README.md dentro de cada pasta:
* 🛡️ **Backend (API & Banco de Dados):** [Clique aqui para ler backend/README.md](backend/README.md)
* 🎨 **Frontend (Interface Angular):** [Clique aqui para ler frontend/README.md](frontend/README.md)
        
📖 Sobre o Projeto

MetaLyse é uma solução Full-Stack completa para extração, análise e histórico de metadados de arquivos digitais. O sistema permite que usuários façam upload de documentos (PDF) e imagens (JPG), extraindo informações técnicas profundas (como dados de GPS, Câmera, Autor, Software de Edição) que muitas vezes ficam ocultas.

O projeto foi construído com foco em Segurança, Arquitetura Limpa e Experiência do Usuário.

🛠️ Tecnologias Utilizadas

O projeto é dividido em duas grandes partes integradas via API REST:

🛡️ Backend (API)

    Linguagem: Python 3

    Framework: Flask

    Banco de Dados: SQLite (com SQLAlchemy ORM)

    Segurança: JWT (JSON Web Tokens) com Blocklist para Logout e Bcrypt para senhas.

    Motor de Análise: ExifTool & PyPDF2

🎨 Frontend (Interface)

    Framework: Angular (v16+)

    Estilização: Angular Material & CSS3

    Comunicação: HTTP Client com Interceptadores de Token

    Recursos: Drag-and-Drop, Visualização de PDF/Imagem, Tabelas Dinâmicas.

📂 Estrutura do Projeto

Bash

MetaLyse-metadata-analysis/
│
├── backend/           # Código fonte da API Python
│   ├── src/           # Controllers, Models e Services
│   ├── instance/      # Banco de dados (app.db)
│   ├── uploads/       # Área temporária de arquivos
│   ├── exiftool.exe   # Ferramenta essencial de análise
│   └── README.md      # 📘 Guia detalhado do Backend
│
├── frontend/          # Código fonte da Interface Angular
│   ├── src/           # Componentes, Serviços e Páginas
│   └── README.md      # 📙 Guia detalhado do Frontend
│
└── README.md          # (Este arquivo)

🚀 Como Rodar o Projeto (Guia Rápido)

Para o sistema funcionar, você precisa rodar o Backend e o Frontend simultaneamente em terminais diferentes.

Passo 1: Iniciar o Backend (Porta 5000)

Consulte o arquivo backend/README.md para detalhes de instalação de dependências e criação do Admin.
PowerShell

cd backend
# Ative o ambiente virtual (venv)
.\venv\Scripts\Activate.ps1 
# Inicie o servidor
python run.py

    O servidor ficará online em: http://127.0.0.1:5000

Passo 2: Iniciar o Frontend (Porta 4200)

Consulte o arquivo frontend/README.md para detalhes de instalação do Node modules.

Abra um novo terminal e execute:
PowerShell

cd frontend
# Inicie a aplicação Angular
npm start

    Acesse a aplicação em: http://localhost:4200

✨ Funcionalidades Principais

1. Autenticação e Segurança

    Cadastro Seguro: Validação de senhas fortes (Maiúsculas, símbolos, números).

    Login JWT: Tokens de acesso com expiração e Refresh Tokens.

    Recuperação de Senha: Fluxo completo com envio de e-mail e token seguro.

    Logout Real: Invalidação de tokens via Blocklist no servidor.

2. Análise de Arquivos

    Suporte a PDF: Extrai contagem de páginas, autor original, software criador e datas internas.

    Suporte a Imagens (JPG): Utiliza o poderoso ExifTool para extrair dados EXIF (Modelo da Câmera, ISO, Abertura, GPS Latitude/Longitude).

    Privacidade: O arquivo físico é analisado e deletado imediatamente do servidor, mantendo apenas os dados no histórico.

3. Histórico e Auditoria

    Painel do Usuário: Cada usuário vê seu próprio histórico de uploads.

    Painel do Administrador: Usuários com permissão elevada podem ver, filtrar e auditar o histórico de todos os usuários do sistema.

👥 Autores

Desenvolvido como projeto acadêmico para a disciplina de Desenvolvimento Full Stack.

    Harthur Henrique (Backend & Integração)

    [Nome do seu Colega] (Frontend & UI)
