#---------------------------------------------------------------------------
# Programm füt den Betrieb eines Cocktailautomaten mit Node Red bedienung
# Ersteller : Niklas Granel
# Datum: 05 .05.2025
# Version 1.1

#-------------------- Bibliotheken -------------------

import network
import ujson
import time
from umqtt.simple import MQTTClient
from machine import Pin

#-------------------- Pins -------------------

# Digitalausgänge

pumpe_1 = Pin(35, Pin.OUT)
pumpe_2 = Pin(36, Pin.OUT)
pumpe_3 = Pin(37, Pin.OUT)
pumpe_4 = Pin(38, Pin.OUT)
pumpe_5 = Pin(39, Pin.OUT)
pumpe_6 = Pin(40, Pin.OUT)
pumpe_7 = Pin(41, Pin.OUT)
pumpe_6 = Pin(42, Pin.OUT)

#Digitaleingänge

glas_vorhanden = Pin(4, Pin.IN) # Pulldown

#I2S
sda = Pin(6)
scl = Pin(7)

#-------------------- Zugänge -------------------

WIFI_ssid = "FRITZ!Box 7530 RR"
WIFI_password = "67307380203238062131"
ip_adresse_mqtt_server = "192.168.178.36"
mqtt_client_id = "esp32_cocktailautomat"
mqtt_topic_zubereiten_start = "zubetreiten_start"
mqtt_topic_zutaten = "zutaten"
mqtt_topic_hand = "hand"
mqtt_topic_statusmeldungen = "statusmeldungen"
mqtt_topic_mengen_doku = "mengen_doku"

#-------------------- Globale Variablen -------------------

zutat_1 = 0
zutat_2 = 0
zutat_3 = 0
zutat_4 = 0
zutat_5 = 0
zutat_6 = 0
zutat_7 = 0
zutat_8 = 0
start_button = "OFF"
fuellstand_zutat_1 = 0
fuellstand_zutat_2 = 0
fuellstand_zutat_3 = 0
fuellstand_zutat_4 = 0
fuellstand_zutat_5 = 0
fuellstand_zutat_6 = 0
fuellstand_zutat_7 = 0
fuellstand_zutat_8 = 0
status_glas_vorhanden = "OFF"
pumpe_1_hand = "OFF"
pumpe_2_hand = "OFF"
pumpe_3_hand = "OFF"
pumpe_4_hand = "OFF"
pumpe_5_hand = "OFF"
pumpe_6_hand = "OFF"
pumpe_7_hand = "OFF"
pumpe_8_hand = "OFF"

#---------- I2C erzeugen ----------

id = 0
i2c = I2C(id=id, sda=sda, scl=scl)

#---------- WLAN-Verbindung für Hauptprogramm ----------

def connect_to_wifi(WIFI_ssid, WIFI_password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ssid, WIFI_password)
    while not wlan.isconnected():
        print("Verbinde mit WLAN...")
        time.sleep(1)
    print("Verbunden! IP:", wlan.ifconfig())

#---------- Subprogramm Zutaten aufschlüsseln ----------

def sub_zutaten(topic, msg):
    global zutat_1, zutat_2, zutat_3, zutat_4, zutat_5, zutat_6, zutat_7, zutat_8
    try:
        daten = ujson.loads(msg)
        zutat_1 = daten.get("zutat_1")
        zutat_2 = daten.get("zutat_2")
        zutat_3 = daten.get("zutat_3")
        zutat_4 = daten.get("zutat_4")
        zutat_5 = daten.get("zutat_5")
        zutat_6 = daten.get("zutat_6")
        zutat_7 = daten.get("zutat_7")
        zutat_8 = daten.get("zutat_8")
        print("Zutat 1:", zutat_1)
        print("Zutat 2:", zutat_2)
        print("Zutat 3:", zutat_3)
        print("Zutat 4:", zutat_4)
        print("Zutat 5:", zutat_5)
        print("Zutat 6:", zutat_6)
        print("Zutat 7:", zutat_7)
        print("Zutat 8:", zutat_8)
    except Exception as e:
        print("Fehler beim Parsen:", e)

#---------- Subprogramm Zubereitung starten ----------

def sub_zubereitung_start(topic, msg):
    global start_button
    try:
        daten = ujson.loads(msg)
        start_button = daten.get("Start_Button")
        print("Startbutton:", start_button)
    except Exception as e:
        print("Fehler beim Parsen:", e)

#---------- Subprogramm Handbetrieb ----------

def sub_handbetrieb(topic, msg):
    global pumpe_1_hand, pumpe_2_hand, pumpe_3_hand, pumpe_4_hand, pumpe_5_hand, pumpe_6_hand, pumpe_7_hand, pumpe_8_hand
    try:
        daten = ujson.loads(msg)
        pumpe_1_hand = daten.get("Pumpe1")
        pumpe_2_hand = daten.get("Pumpe2")
        pumpe_3_hand = daten.get("Pumpe3")
        pumpe_4_hand = daten.get("Pumpe4")
        pumpe_5_hand = daten.get("Pumpe5")
        pumpe_6_hand = daten.get("Pumpe6")
        pumpe_7_hand = daten.get("Pumpe7")
        pumpe_8_hand = daten.get("Pumpe8")
        print("Pumpe 1 Hand", pumpe_1_hand)
        print("Pumpe 2 Hand", pumpe_2_hand)
        print("Pumpe 3 Hand", pumpe_3_hand)
        print("Pumpe 4 Hand", pumpe_4_hand)
        print("Pumpe 5 Hand", pumpe_5_hand)
        print("Pumpe 6 Hand", pumpe_6_hand)
        print("Pumpe 7 Hand", pumpe_7_hand)
        print("Pumpe 8 Hand", pumpe_8_hand)
    except Exception as e:
        print("Fehler beim Parsen:", e)

#---------- Subprogramm globale Topicabfrage ----------

def globale_topicabfrage(topic, msg):
    topic = topic.decode()
    if topic == mqtt_topic_zubereiten_start:
        sub_zubereitung_start(topic, msg)
    elif topic == mqtt_topic_zutaten:
        sub_zutaten(topic, msg)
    elif topic == mqtt_topic_hand:
        sub_handbetrieb(topic, msg)
        
#---------- Subprogramm reconnect MQTT ----------

def reconnect():
    global mqtt_client
    try:
        mqtt_client.connect()
        mqtt_client.subscribe(mqtt_topic_zubereiten_start)
        mqtt_client.subscribe(mqtt_topic_zutaten)
        mqtt_client.subscribe(mqtt_topic_hand)
    except OSError as e:
        print("Verbindung fehlgeschlagen:", e)
        time.sleep(5)
        
#--------------- Verbindungen ---------------
        
connect_to_wifi(WIFI_ssid, WIFI_password)

#--------------- MQTT client erzeugen -------------
mqtt_client = MQTTClient(mqtt_client_id, ip_adresse_mqtt_server, keepalive=30)
mqtt_client.set_callback(globale_topicabfrage)
mqtt_client.connect()
mqtt_client.subscribe(mqtt_topic_zubereiten_start)
mqtt_client.subscribe(mqtt_topic_zutaten)
mqtt_client.subscribe(mqtt_topic_hand)

while True:
    try:
        mqtt_client.check_msg()
       
    except OSError as e:
        print("MQTT Fehler:", e)
        reconnect()

