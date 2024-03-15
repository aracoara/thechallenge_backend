from tennis_app import app
from tennis_app.models import Pick, Tournament, Player, User
from flask import jsonify

import logging
from sqlalchemy import event
from sqlalchemy.engine import Engine
from tennis_app import app

# Desativar logging do SQLAlchemy
# logging.getLogger('sqlalchemy').handler = []
# logging.getLogger('sqlalchemy').propagate = False

# # Desativar echo de todas as engines criadas
# @event.listens_for(Engine, "connect")
# def set_sqlalchemy_log_off(dbapi_connection, connection_record):
#     dbapi_connection.isolation_level = None 
#     cursor = dbapi_connection.cursor()
#     cursor.execute("SET session sql_log_bin=0;")
#     cursor.close()

user_id =36
short_name = "IW"
year = 2024
with app.app_context():
    def get_user_name_by_id(user_id):
        user = User.query.get(user_id)
        return user.username if user else "Unknown User"
    def get_player_name_by_id(player_id):
        player = Player.query.get(player_id)
        return player.name if player else "Unknown"
    # player = Player.query.get(player_id)
    username = User.query.get(user_id).username
    user = User.query.get(user_id)
    # print(f'Username: {username}')
    tournament = Tournament.query.filter_by(short_name=short_name, year=year).first()
    picks = Pick.query.filter_by(tournament_id=tournament.id).all()
    picks_output = []

    # Organize picks by user
    picks_by_user = {}
    for pick in picks:
        user_id = pick.user_id
        if user_id not in picks_by_user:
            picks_by_user[user_id] = []
        picks_by_user[user_id].append(pick)
    # print(f'Picks by user: {picks_by_user}')
    for user_id, user_picks in picks_by_user.items():
        user_output = {"User": get_user_name_by_id(user_id), "tournament_id": tournament.id}
        for pick in user_picks:
            player_name = get_player_name_by_id(pick.player_id)
            user_output[pick.position] = player_name
        picks_output.append(user_output)
    print(f'Picks output: {picks_output}')


    

