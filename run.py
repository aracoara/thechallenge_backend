## Arquivo de entrada da aplicação

# run.py
from tennis_app import app

if __name__ == '__main__':
    app.run(debug=True)


# venv\Scripts\activate # Ativar ambiente virtual

# # comandos para subir alterações no git
# git init
# git status
# git add .
# git commit -m "Descrever o que foi feito"
# git branch
# git checkout -b feature/html
# git push --set-upstream origin novo_frontend

## comando para definir a variável de ambiente FLASK_APP para indicar ao Flask qual é o arquivo de entrada da sua aplicação
# flask db heads
# $env:FLASK_APP = "D:\TENIS\smash_picks_backend\tennis_app"
# flask db init
# flask db migrate -m "Add qf_number to Player"
# flask db upgrade

# atualizar o arquivo requirements.txt    
# pip freeze > requirements.txt
    