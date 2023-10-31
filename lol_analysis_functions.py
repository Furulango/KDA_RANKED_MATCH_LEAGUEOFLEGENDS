import requests
import json

def obtener_puuid(summoner_name, api_key, server):
    url_summoner = f"https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    response = requests.get(url_summoner, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        summoner_data = response.json()
        return summoner_data['puuid']
    else:
        print(f"Error al obtener PUUID: {response.status_code}")
        return None

def obtener_id_partida_especifica(puuid, api_key, region, numero_partida):
    queue = '420'  # Código para RANKED_SOLO_5x5
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&queue={queue}&start={numero_partida - 1}&count=1"
    response = requests.get(url, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        partidas = response.json()
        return partidas[0] if partidas else None
    else:
        print(f"Error {response.status_code}: {response.json()}")
        return None

def obtener_detalles_partida_y_guardar(match_id, api_key, region, numero_partida,summoner_name):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers={"X-Riot-Token": api_key})

    if response.status_code == 200:
        detalles_partida = response.json()
        nombre_archivo = f"{summoner_name}_{numero_partida}.json"
        with open(nombre_archivo, 'w') as archivo:
            json.dump(detalles_partida, archivo, indent=4)
        print(f"Detalles de la partida {numero_partida} guardados en '{nombre_archivo}'")
    else:
        print(f"Error {response.status_code}: {response.json()}")

def analizar_y_guardar_partidas(summoner_name, api_key, server, region, cantidad_partidas):
    puuid = obtener_puuid(summoner_name, api_key, server)
    if not puuid:
        return

    for numero_partida in range(1, cantidad_partidas + 1):
        match_id = obtener_id_partida_especifica(puuid, api_key, region, numero_partida)
        if match_id:
            obtener_detalles_partida_y_guardar(match_id, api_key, region, numero_partida,summoner_name)
        else:
            print(f"No se pudo obtener el ID de la partida {numero_partida}")
