
# Etapas para implementação do Smash Picks App

## Passo 1: Especificação do App

### Descrição do Smash Picks

- O aplicativo web "Palpites do Torneio de Tênis" é uma plataforma para hospedar um bolão de apostas em torneios de tênis, permitindo que múltiplos usuários façam 15 palpites em um torneio de tenis. 
- O torneio de 128 jogadores funciona da seguinte forma:
    - Na primeira rodada, são realizados 64 jogos. Os vencedores avançam para a segunda rodada, onde há 32 jogos. 
    - Na terceira rodada, restam 16 jogadores e 16 jogos. 
    - A quarta rodada tem 8 jogos, levando às quartas de final com 4 jogos. 
    - As semifinais contam com apenas 2 jogos, e a final decide o campeão. 
    - Este é um torneio progressivo, onde os jogadores enfrentam eliminatórias até que apenas um permaneça como vencedor.
- O aplicativo foca em três etapas-chave de um torneio de tênis: Quartas de Final (QF), Semifinais (SF) e Final (F).
    - Dessa forma, os usuários devem escolher 8 jogadores para as QF, 4 para a SF, 2 finalistas e 1 campeão
- Jogadores:
    - os jogadores são identificados pelo nome, pais e seed
    - cada jogador está associado com um identificador de posição de quarterfinal (qf_number)
    - isso garante a uma validação de entrada de dados para a QF, pois o jogador estará vinculado a um qf_number associado a cada uma das oitos possiveis para QF (ex: QF1, QF2, ..., QF8)
- Games:
    - Um jogo está associado a uma rodada, com inicio na QF
    - Cada jogo possui um player1, player2 e winner
    - Os jogos seguem o seguinte mapeamento:
        - QF1: players com qf_number=1
        - QF2: players com qf_number=2
        ...
        - QF8: players com qf_number=8
        - SF1: QF1, QF2
        - SF2: QF3, QF4
        - SF3: QF5, QF6
        - SF4: QF7, QF8
        - F1: SF1, SF2
        - F2: SF3, SF4
        - Champion: F1, F2
- Picks:
    - Os palpites são um conjunto de 15 escolhas: QF1, QF2, QF3, QF4, QF5, QF6, QF7, QF8, SF1, SF2, SF3, SF4, F1, F2, Champion
    - Os palpites (picks) são um conjunto de 15 escolhas e estão associados com game da seguinte forma:
        - QF1: player1, game=1
        - QF2: player2, game=1
        - QF3: player1, game=2
        - QF4: player2, game=2
        - QF5: player1, game=3
        - QF6: player2, game=3
        - QF7: player1, game=4
        - QF8: player2, game=4
        - SF1: player1, game=5, winner do game=1
        - SF2: player2, game=5, winner do game=2
        - SF3: player1, game=6, winner do game=3
        - SF4: player2, game=6, winner do game=4
        - F1: player1, game=7, winner do game=5
        - F2: player2, game=7, winner do game=7
        - Champion: winner do game=7

### Pontuação

- O sistema de pontuação adotado é baseado em pesos atribuídos a cada fase do torneio: 1 ponto para as QF, 2 pontos para as Semifinais (SF), 3 pontos para a Final (F) e 4 pontos para acertar o campeão.  
- Durante o torneio, será calculada a pontuação dos usuários, iniciando a partir das Quartas de Final (QF).
- Após cada partida, haverá uma atualização do total de pontos possíveis para cada participante. 
- Atualização das pontuações
    - Arquivo csv com classificados da R1, R2, ..., QF, SF, F, Champion
    - Executar o arquivo Leaderboard_update.py para cada rodada

### Páginas do app

- A página Pick permite que os usuários façam as 15 escolhas do torneio por meios de células de escolha dropdown.
- A página Leaderboard do aplicativo incluirá tabela de classificação e gráficos de barras empilhados de pontos possíveis e ganhos, por rodada.
- A página Picks Overview possui uma tabela em que é possível comparar a escolha de cada participante com o resultado oficial.
- A página Users possui as informações da conta do participante

### Modelos de dados

- Há as seguintes classes:
	- User(id,username, email, password_hash, picks)
	- RoundType(QF,SF,F)
	- Player(id, name, country, seed, qf_number)
	- Game(id, round, player1_id, player2_id, winner_id)
	- Pick(id, user_id, game_id, player1_id, player2_id, winner_id, round)
	- Pontuacoes(id,ranking_pp,ranking_pg,username,pontos_possiveis,pontos_ganhos, rodada, data_atualizacao)
    - Tournaments (id, name, short_name, year, status)

### Rotas

- Temos as seguintes rotas:
	- '/players', methods=['GET']: Rota para obter todos os jogadores
	- '/submit_picks', methods=['POST']: Rota para enviar os picks de um participante
	- '/pontuacoes/rodada/<rodada>', methods=['GET']: Rota para obter as pontuações por rodada
	- '/api/PicksOverview', methods=['GET']: Rota para obter os Picks de todos os usuários
	- '/api/classified-players', methods=['GET']: Rota para obter os jogadores classificados

### Tecnologia

- Tecnologias usadas: 
    - Backend: Python, Flask, SQLite
    - Frontend: React, Bootstrap
- Configurar Ambiente de Desenvolvimento:
    - VS Code: Usar o VS Code para o desenvolvimento do projeto na fase local, com auxílio do GitHub copilot.
    - Framework Web: Flask para gerenciar as rotas, interações com o banco de dados e lógica de negócios.

## Passo 2: Funcionalidades do Web App

- [X] Autenticação de usuários.
- [X] Seleção de palpites (picks).
- [X] Submissão e armazenamento de palpites.
- [X] Cálculo de pontos
- [X] Exibição do ranking.
- [ ] Acompanhanento em tempo real do ranking por meio de apis (ex: https://api-tennis.com/)

## Passo 3: Design e Prototipagem

- [X] Esboçar as Telas: Crie wireframes para as páginas principais (Tela Chave do Torneio e Tela de Resultado).
- [X] Design de Interface: Desenvolva o design detalhado, incluindo esquema de cores, tipografia e elementos de UI.

## Passo 4: Estrutura do projeto

- [X] Backend
    - [X] Arquivo Python principal (app.py) para a lógica do servidor Flask.
    - [X] Pasta para modelos do banco de dados SQLite.
    - [X] Pasta para rotas do Flask que lidam com requisições e respostas HTTP.
- [X] Frontend
    - [X] Arquivos HTML para as páginas da interface do usuário.
    - [X] Arquivos CSS para estilização.
    - [X] Arquivos JavaScript para lógica do front-end.

## Passo 5: Passos iniciais

- [X] Configurar o ambiente de desenvolvimento.
- [X] Instalar Flask, SQLite e outras dependências necessárias.
- [X] Inicializar um repositório Git para versionamento do projeto

## Passo 6: Desenvolvimento

- [X] Backend:
    - [X] Configurar o servidor Flask.
- [X] Modelagem de dados:
    - [X] Usuários
    - [X] Torneios
    - [X] Jogos
    - [X] Jogadores
- [X] Configurar a conexão com o banco de dados SQLite.
- [X] Front-end inicial:
    - [X] Criar páginas básicas em HTML.
    - [X] Adicionar estilos CSS.
    - [X] Implementar funcionalidades básicas em JavaScript.
- [X] Rota POST para `submitPicks`:
    - [X] Receber o JSON `submitPicks` do frontend.
    - [X] Validar e processar os dados para gerar objetos `Game`.
    - [X] Salvar os objetos `Game` na base de dados.
- [X] Criação da Classe `User` sem autenticação:
    - [X] Representa um usuário no sistema.
    - [X] Adicionar campos como `id`, `username`
    - [X] Relacionamento com a classe `Picks`.
- [X] Atualização da pontuação no frontend    
    - [X] Cálculo de Pontos:
        - [X] Incluir rotina de atualização dos vencedores a cada rodada
        - [X] Criar função para calcular os pontos possíveis e ganhos com base reais dos jogos.
        - [X] Desenvolver lógica para ordenar usuários com base nos pontos calculados.
    - [X] Estrutura do Banco de Dados
        - [X] Criar tabela `Pontuações` para armazenar pontos de cada usuário por rodada.
        - [X] Criar view `ViewPontuações` que consolida dados de pontuação dos usuários.
    - [X] Atualização de Pontuações
        - [X] Desenvolver rotina para atualizar `Pontuações` e `ViewPontuações` para cada rodada.
    - [X] Desenvolvimento da API
        - [X] Criar endpoints da API para recuperar pontuações dos usuários por rodada.
    - [X] Integração com o Frontend
        - [X] Desenvolver componentes no frontend React para exibir a tabela de ranking.
        - [X] Utilizar React Bootstrap para estilizar a tabela de ranking.
- [X] Página PicksOverview:
    - [X] Criar uma rota API para retornar os palpites dos usuários com o mapeamento:
        - QF1, QF2, QF3, QF4, QF5, QF6, QF7, QF8, SF1, SF2, SF3, SF4, F1, F2, Champion
    - [X] Criar uma rota API para retornar os jogadores classificados a partir das QFs
    - [X] A página PicksOverview.js deve receber os dados de PicksOverview e Results e construir uma tabela
    - [X] A tabela deve fazer uma formatação condicional comparando os resultados com os Picks
- [X] Página Picks no React
    - [X] Refazer a página de Picks
- [X] Modelo de Usuário e Banco de Dados
	- [X] Definir modelo de usuário: Criar classe User com SQLAlchemy, incluindo id, username, email, password_hash.
	- [X] Hashing de senhas: Implementar método para definir e verificar senha hash.
	- [X] Configurar banco de dados: Inicializar o banco de dados e criar tabelas.
- [X] Implementação de Flask-Login
	- [X] Configurar user_loader: Implementar a função que carrega o usuário a partir do ID.
	- [X] Login e logout: Criar rotas para login e logout utilizando Flask-Login.
- [X] Formulários com Flask-WTF
	- [X] Formulário de Registro: Criar classe de formulário com validações para registro.
	- [X] Formulário de Login: Criar classe de formulário com validações para login.
- [X] Rotas e Views
	- [X] Rota de registro: Implementar a view que processa o formulário de registro.
	- [X] Rota de login: Implementar a view que processa o formulário de login.
	- [X] Logout: Implementar a rota para logout.
- [X] Recuperação de Senha
	- [X] Formulário de recuperação: Criar formulário para solicitar redefinição de senha.
	- [X] Enviar e-mail: Implementar a lógica para enviar um e-mail com o link de redefinição.
	- [X] Redefinir senha: Criar rota e formulário para permitir ao usuário redefinir a senha.
- [X] Implementar o submit Picks no React
    - [X] Pegar o username juntamente com o conjunto de picks e criar json de picks de um usuário no react
    - [X] Implementar rota submit_picks para salvar o pick do usuário no db no react      
- [ ] Implementação da classe Tournaments e adaptação para diferentes tamanhos de torneios.
    - [X] Atributos Básicos: 
        - [X] id, name, start_date, end_date, location
    - [X] Modificações nas Outras Classes:
        - [X] Player: Adicionar um relacionamento muitos-para-muitos com Tournaments ??
        - [X] Game: Incluir uma chave estrangeira tournament_id para associar cada jogo a um torneio específico.
        - [X] Pick: A classe Pick também deve incluir uma referência ao torneio para o qual o palpite é feito, adicionando um tournament_id.
        - [X] Pontuações: Incluir tournament_id para associar as pontuações a torneios específicos.
    - [X] Alterações no Banco de Dados:
        - [X] Adicionar a tabela Tournaments e atualizar tabelas existentes para incluir chaves estrangeiras referenciando Tournaments, conforme necessário.
        - [X] Atualizar índices e chaves estrangeiras para manter a integridade referencial.
    - [X] Atualização das Rotas:
        - [X] Criar novas rotas para gerenciar torneios (criar, ler, atualizar, deletar).
        - [X] Atualizar as rotas existentes para incluir o identificador do torneio nos parâmetros, de modo a filtrar dados por torneio.
            - [X] /players/
            - [X] /submit_picks
            - [X] /pontuacoes/rodada/<rodada>
            - [X] /api/PicksOverview
            - [X] /api/classified-players
    - [X] Interface de Usuário para Gerenciamento de Torneios:
        - [X] Desenvolver páginas para a criação, visualização, e gestão de torneios.
        - [X] Permitir que os usuários selecionem o torneio para o qual desejam fazer palpites ou visualizar resultados.
    - [X] Atualização de Páginas Existentes:
        - [X] Página Pick: Permitir que os usuários escolham o torneio antes de fazerem seus palpites.
        - [X] Leaderboard: Permitir a seleção de torneios e exibir dados relevantes ao torneio selecionado.
        - [X] Picks Overview: Permitir a seleção de torneios e exibir dados relevantes ao torneio selecionado.
        - [X] Página de Tournament: Seletor de Torneio e disponibilização de link exclusivo para grupo de Whatsapp.
    - [X] Adaptações no Envio e na Recuperação de Dados:
        - [X] Modificar as chamadas de API para incluir o identificador do torneio como parte das requisições, garantindo que os dados enviados ou solicitados sejam relevantes ao torneio selecionado.
- [ ] PicksOverview.
    - [X] Integrar a api /classified-players com o PicksOverview
- [ ] Footnote
    - [ ] Quem somos
    - [ ] Regras
    - [ ] Formulário de Sugestões
    - [ ] Termos de uso e Política de Privacidade
    - [ ] Siga-nos 
- [ ] Segurança e Proteção
	- [ ] Proteção CSRF: Garantir que todos os formulários utilizem tokens CSRF.
        - [ ] Login
        - [ ] Logout
        - [ ] SignUp
        - [ ] Submit Picks
	- [X] Segurança de senha: Assegurar que as senhas sejam hashadas antes de salvar no banco de dados.
	- [ ] Proteção adicional: Implementar medidas adicionais conforme necessário (HTTPS, headers de segurança).    
- [ ] Documentação
    - [ ] Criar documentação do app que inclua:
        - [ ] Descrição do app
        - [ ] Lógica do negócio
        - [ ] Explicação geral das principais funções
        - [ ] Lógica completa de um torneio, incluindo:
            - [ ] Criação do torneio no backend 
            - [ ] Carregamento dos jogadores do torneio
            - [ ] Descrição do operacional para atualizar os resultados dos jogos

## Passo 7: Correções

- [ ] Incluir rota para a confirmação do email no signup
- [X] Incluir fluxo de redefinição de senha caso o login falhe
- [X] Incluir link de redefinição de senha na tela do login
- [ ] Criar Rodapé
    - [ ] Quem somos
    - [ ] Missão do Smash Picks
    - [ ] Regras do Smash Picks
        - Os palpites somente são aceitos após a divulgação da chave e antes do início do torneio
        - Explicar os pesos dos palpites
        - Explicar o critério de desempate
    - [X] Formulário de sugestões
        - Criar formulário no google form com apenas um campo aberto para o recebimento de sugestões
- [X] TournamentPage
    - [X] Incluir texto e link quando:
        - [X] Status "Open": 
            - Faça os seus palpites na Página Picks (/picks)
        - [X] Status "On Progress: 
            - Compare o seu palpite com os demais participantes (/picksoverview) 
            - Acompanhe o seu desempenho na Página Leaderboard (/leaderboard)
- [ ] PicksPage
    - [ ] Incluir botão "Submit" para limpar seleção
- [ ] Criar UserPage
    - [ ] Mostrar quais torneios o participante está inscrito
    - [ ] Exigir os picks do participante
- [X] Rotas condicionais:
    - [X] Só deve estar disponivel a página Picks quando o status do torneio for "Open"
    - [X] As peginas PicksOverview e Leaderboard devem ficar disponíveis quando o status do torneio for "On Progress"
    - [X] As páginas Picks, PicksOverview e Leaderboard não devem estar disponíveis quando o status do torneio for "Closed"

## Passo 8: Deploy e Lançamento

- [ ] Deploy de backend: google cloud run
- [ ] Deploy de frontend: vercel

## Passo 9: Revisão e Iteração

- [ ] Coletar Feedback: Receba feedback dos usuários e stakeholders.
- [ ] Ajustes e Melhorias: Faça as melhorias necessárias no design, usabilidade e funcionalidades.
- [ ] Refatoração: Otimizar o código para melhor manutenção e desempenho.

## Passo 10: Manutenção e Atualização

- [ ] Suporte Contínuo: Forneça suporte técnico e responda a feedbacks e problemas dos usuários.
- [ ] Atualizações Regulares: Continue desenvolvendo novas funcionalidades e melhorias.
