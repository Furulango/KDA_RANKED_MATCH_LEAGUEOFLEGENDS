

import lol_analysis_functions as laf
import kda as kda


api_key = 'api_key'
summoner_name = 'summoner_name'
server = 'server'
region = 'region'
cantidad_partidas = 1

laf.analizar_y_guardar_partidas(summoner_name, api_key, server, region, cantidad_partidas)

for i in range(1,cantidad_partidas):
    kda.analizar_kda(f"{summoner_name}_{i}")
