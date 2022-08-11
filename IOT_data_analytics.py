import mysql.connector #importer le connecteur mysql pour python
import datetime #importer le module de date

# importer les librairies nécessaires pour extraire les données du dht11
import time
import board
import adafruit_dht
import psutil
import pandas as pd
# importer les librairies nécessaires pour utiliser Dash
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import webbrowser

#importer la librairie qui nous permettra de lancer le dashboard au lancement du programme
import webbrowser

#commecer l'extraction des données

    #si les broches sont en cours d'utilisation ,arrêter le processus
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
#définir le capteur comme objet
dht_pin=board.D23
sensor = adafruit_dht.DHT11(dht_pin)

#Enregistrer les données de connexion à la bd dans un dictionnaire

connection_params = {
    'host': "localhost",
    'user': "iot_dba",
    'password': "pass123",
    'database': "iot_db",
}
#Définir une fonction qui nous permettra d'évaluer les états d'alerte en fonction des constantes prélevées
def alert(th,seuil):
    status=""
    if th >= seuil:
        status="ALERT"
    else:
        status="NORMAL"
        
    return status

seuil_temperature=0
seuil_humidity=0
        
    
while True:
    
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        monitoring_date=datetime.datetime.today()
        status_temperature=alert(temperature,seuil_temperature)
        status_humidity=alert(humidity,seuil_humidity)
        
        request = """insert into DHT
             (temperature,humidity,monitoring_date,status_temperature,status_humidity)
             values (%s, %s, %s, %s, %s)"""
        
        params = (temperature,humidity,monitoring_date,status_temperature,status_humidity) 

        with mysql.connector.connect(**connection_params) as db :
            db.autocommit = True
            with db.cursor() as c:
                c.execute(request,params)
                c.execute(df_request)
                df=c.fetchall()
                df=pd.DataFrame(df,columns=dfc_name)
                
                

        
    except RuntimeError as error:
        #print(error.args[0])
        time.sleep(600.0)
        continue
    except Exception as error:
        #sensor.exit()
        raise error

    time.sleep(600.0)#toutes les 10 mins



