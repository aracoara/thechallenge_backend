from tennis_app import app
from tennis_app.extensions import db
from tennis_app.models import Pick, Pontuacoes, User

def delete_picks_by_user(user_id):
    """Deleta registros na tabela 'picks' para um usuário específico."""
    Pick.query.filter(Pick.user_id == user_id).delete(synchronize_session='fetch')

def delete_pontuacoes_by_user(user_id):
    """Deleta registros na tabela 'pontuacoes' para um usuário específico."""
    user_username = db.session.query(User.username).filter(User.id == user_id).scalar()
    Pontuacoes.query.filter_by(username=user_username).delete(synchronize_session='fetch')

def delete_user(user_id):
    """Deleta um usuário específico na tabela 'users'."""
    User.query.filter(User.id == user_id).delete(synchronize_session='fetch')

def delete_user_records(user_id):
    """Agrupa as operações de exclusão de registros relacionados a um usuário específico."""
    with app.app_context():
        try:
            delete_picks_by_user(user_id)
            delete_pontuacoes_by_user(user_id)
            # delete_user(user_id)
            
            db.session.commit()
            print("Registros deletados com sucesso.")
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao deletar registros: {e}")

if __name__ == '__main__':
    user_id = 38  # Defina o user_id que você deseja deletar
    delete_user_records(user_id)
