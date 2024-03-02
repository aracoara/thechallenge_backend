import pandas as pd
from tennis_app.models import Player, Tournament
from tennis_app import app
from tennis_app.utils import process_and_update_rounds

tournament_short_name = 'AO'
tournament_year = 2024

# Definindo o caminho do arquivo
etapas_torneio = {
    ## RIO 2024
    # "R1": 'tennis_app/assets/RIO24/RIO-24-Results - R1.csv',
    # "R2": 'tennis_app/assets/RIO24/RIO-24-Results - R2.csv',
    # "R3": 'tennis_app/assets/RIO24/RIO-24-Results - R3.csv',
    # "R4": 'tennis_app/assets/RIO24/RIO-24-Results - R4.csv',
    # "QF": 'tennis_app/assets/RIO24/RIO-24-Results - QF.csv',
    # "SF": 'tennis_app/assets/RIO24/RIO-24-Results - SF.csv',
    # "F": 'tennis_app/assets/RIO24/RIO-24-Results - F.csv',
    # "Champion": 'tennis_app/assets/RIO24/RIO-24-Results - Champion.csv',

    ## AO 2024
    "R1": 'tennis_app/assets/AO24/AO-24-Results - R1.csv',
    "R2": 'tennis_app/assets/AO24/AO-24-Results - R2.csv',
    "R3": 'tennis_app/assets/AO24/AO-24-Results - R3.csv',
    "R4": 'tennis_app/assets/AO24/AO-24-Results - R4.csv',
    "QF": 'tennis_app/assets/AO24/AO-24-Results - QF.csv',
    "SF": 'tennis_app/assets/AO24/AO-24-Results - SF.csv',
    "F": 'tennis_app/assets/AO24/AO-24-Results - F.csv',
    "Champion": 'tennis_app/assets/AO24/AO-24-Results - Champion.csv',    
}

RoundUpdates = process_and_update_rounds(etapas_torneio, tournament_short_name, tournament_year)

## Imprimindo as atualizações
for round_update in RoundUpdates:
    print(round_update)
