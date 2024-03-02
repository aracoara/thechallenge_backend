from tennis_app.utils import (process_results_data, gatherFormattedTournamentPicks, trackTournamentEliminations, compileValidTournamentPicks, 
                                    calculatePossiblePointsByTournament, calculateEarnedPoints, mergePossibleAndEarnedPoints)
from tennis_app.models import Pontuacoes
from tennis_app import app
from tennis_app.extensions import db
# import pandas as pd
import numpy as np
from datetime import datetime

# Crie uma instância do aplicativo Flask se ainda não tiver uma
app.app_context()

##########################################################################################
#########################ATUALIZAR OS RESULTADOS DA RODADA################################
##########################################################################################


# Caminho relativo para o arquivo CSV com os resultados
file_path_R1 = 'tennis_app/assets/R1-ao24.csv'
file_path_R2 = 'tennis_app/assets/R2-ao24.csv'
file_path_R3 = 'tennis_app/assets/R3-ao24.csv'
file_path_R4 = 'tennis_app/assets/R4-ao24.csv'
file_path_QF = 'tennis_app/assets/QF-ao24.csv'
file_path_SF = 'tennis_app/assets/SF-ao24.csv'
file_path_F = 'tennis_app/assets/F-ao24.csv'
file_path_Champion = 'tennis_app/assets/Champion-ao24.csv'

# Processando os resultados e mapeando os IDs dos jogadores
classificados_R1 = process_results_data(file_path_R1)
print("Classificados da R1:")
print(classificados_R1)
classificados_R2 = process_results_data(file_path_R2)
print("Classificados da R2:")
print(classificados_R2)
classificados_R3 = process_results_data(file_path_R3)
print("Classificados da R3:")
print(classificados_R3)
classificados_R4 = process_results_data(file_path_R4)
print("Classificados da R4:")
print(classificados_R4)
classificados_QF = process_results_data(file_path_QF)
print("Classificados da QF:")
print(classificados_QF)
classificados_SF = process_results_data(file_path_SF)
print("Classificados da SF:")
print(classificados_SF)
classificados_F = process_results_data(file_path_F)
print("Classificados da F:")
print(classificados_F)
Champion = process_results_data(file_path_Champion)
print("Champion:")
print(Champion)