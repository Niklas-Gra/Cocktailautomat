#---------------------------------------------------------------------------
# Programm zum testen der Datenübertragung vom Web zum Controller
# Ersteller : Niklas Granel
# Datum: 25.02.2025
# Version 1

#-------------------- Bibliotheken -------------------

import network
import ujson
import time
from umqtt.simple import MQTTClient
from machine import Pin

#-------------------- Zugänge -------------------

WIFI_ssid = "FRITZ!Box 7530 RR"
WIFI_password = "67307380203238062131"
ip_adresse_mqtt_server = "192.168.178.36"
mqtt_client_id = "esp32_cocktailautomat"
mqtt_topic = "zubetreiten_start"


#-------------------- Globale Variablen -------------------
Zutat_1 = None
Zutat_2 = None
Zutat_3 = None
schalter = None
start = None


#---------- WLAN-Verbindung für Hauptprogramm ----------

def connect_to_wifi(WIFI_ssid, WIFI_password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ssid, WIFI_password)
    while not wlan.isconnected():
        print("Verbinde mit WLAN...")
        time.sleep(1)
    print("Verbunden! IP:", wlan.ifconfig())

def connect_to_mqtt():
    try:
        mqtt_server = ip_adresse_mqtt_server
        mqtt_port = 1883
        client_id = mqtt_client_id
        client = MQTTClient(client_id, mqtt_server, port=mqtt_port)
        client.connect()
        print("Verbunden mit MQTT-Broker:", mqtt_server)
        return client
    except Exception as e:
        print("Fehler bei der Verbindung mit dem MQTT-Broker:", e)
        return None

    
def sub_Zahl(topic, msg):
    global Zutat_1, Zutat_2, Zutat_3, schalter, start
    try:
        daten = ujson.loads(msg)
        Zutat_1 = daten.get("zutat_1")
        Zutat_2 = daten.get("zutat_2")
        Zutat_3 = daten.get("zutat_3")
        schalter = daten.get("Schalter1")
        start = daten.get("Start_Button")
        print("Zustand Schalter:", schalter)
        print("Startbutton:", start)
        print("Empfangene Zahl:", Zutat_1)
        print("Zutat 1:", Zutat_1)
        print("Zutat 2:", Zutat_2)
        print("Zutat 3:", Zutat_3)
    except Exception as e:
        print("Fehler beim Parsen:", e)
        
def zubereiten():
    global schalter, start, Zutat_1, Zutat_2, Zutat_3
    if schalter == "ON" and start == "ON":
        print("erstens:", Zutat_1)
        print("zweitens:", Zutat_2)
        print("drittens:", Zutat_3)


#--------------- Verbindungen ---------------
connect_to_wifi(WIFI_ssid, WIFI_password)
connect_to_mqtt()


#--------------- MQTT client erzeugen -------------

mqtt_client = MQTTClient(mqtt_client_id, ip_adresse_mqtt_server, keepalive=60)
mqtt_client.set_callback(sub_Zahl)
time.sleep(1)
mqtt_client.connect()
mqtt_client.subscribe(mqtt_topic)
print("MQTT verbunden!") 

def reconnect():
    global mqtt_client
    try:
        mqtt_client.connect()
        mqtt_client.subscribe(mqtt_topic)
    except OSError as e:
        print("Verbindung fehlgeschlagen:", e)
        time.sleep(5)

while True:
    try:
        mqtt_client.check_msg()
        zubereiten()
        
    except OSError as e:
        print("MQTT Fehler:", e)
        reconnect()
           
     
