import json
import pandas as pd

import json
import pandas as pd

def analizar_kda(nombre_archivo):
    try:
        with open(f"{nombre_archivo}.json", 'r') as archivo:
            datos_partida = json.load(archivo)

        jugadores = datos_partida.get("info", {}).get("participants", [])
        
        # Crear listas para los equipos
        equipo_azul = []
        equipo_rojo = []

        for jugador in jugadores:
            equipo_id = jugador.get("teamId")
            nombre_invocador = jugador.get("summonerName", "Desconocido")
            kills = jugador.get("kills", 0)
            deaths = jugador.get("deaths", 0)
            assists = jugador.get("assists", 0)
            kda = "Perfecto" if deaths == 0 else f"{(kills + assists) / deaths:.2f}"

            if equipo_id == 100:
                equipo_azul.append([nombre_invocador, kills, deaths, assists, kda])
            else:
                equipo_rojo.append([nombre_invocador, kills, deaths, assists, kda])

        # Convertir listas en DataFrames de pandas
        df_azul = pd.DataFrame(equipo_azul, columns=["Invocador", "Kills", "Deaths", "Assists", "KDA"])
        df_rojo = pd.DataFrame(equipo_rojo, columns=["Invocador", "Kills", "Deaths", "Assists", "KDA"])

    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no existe.")
    except json.JSONDecodeError:
        print(f"Error al decodificar {nombre_archivo}. Asegúrate de que sea un archivo JSON válido.")


    df_separador = pd.DataFrame([""] * len(df_azul), columns=["Separador"])
    df_total = pd.concat([df_azul, df_separador, df_rojo], axis=1)
    nombre_archivo_csv = f"KDA_Combinado_{nombre_archivo}.csv"
    df_total.to_csv(nombre_archivo_csv, index=False)

    df_combinado = pd.concat([df_azul, df_rojo])
    nombre_archivo_csv = f"KDA_Combinado_{nombre_archivo}.csv"
    df_combinado.to_csv(nombre_archivo_csv, index=False)
    print(f"KDA de ambos equipos guardados en '{nombre_archivo_csv}'")