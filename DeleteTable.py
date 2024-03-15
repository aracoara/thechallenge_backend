from sqlalchemy import create_engine, text

# Substitua o caminho abaixo pelo caminho completo para o arquivo do banco de dados SQLite
DATABASE_URI = 'sqlite:///D:\\TENIS\\thechallenge_backend\\instance\\thechallenge.db'

def drop_alembic_tmp_games_table():
    engine = create_engine(DATABASE_URI)
    
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS _alembic_tmp_games"))
            print('"_alembic_tmp_games" table dropped.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    drop_alembic_tmp_games_table()

# from sqlalchemy import create_engine, text

# # Substitua o caminho abaixo pelo caminho completo para o arquivo do banco de dados SQLite
# DATABASE_URI = 'sqlite:///D:\\TENIS\\thechallenge_backend\\instance\\thechallenge.db'

# def drop_rounds_table():
#     engine = create_engine(DATABASE_URI)
    
#     try:
#         with engine.connect() as conn:
#             conn.execute(text("DROP TABLE IF EXISTS rounds"))
#             print('"rounds" table dropped.')
#     except Exception as e:
#         print(f'An error occurred: {e}')

# if __name__ == '__main__':
#     drop_rounds_table()
