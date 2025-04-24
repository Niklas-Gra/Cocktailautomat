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
mqtt_topic = "cocktailautomat"

#--------------- LED konfiguration ---------------

led = Pin(4, Pin.OUT)
led_on = False

#LED Testen
led.on()
time.sleep(1)
led.off()

#---------- WLAN-Verbindung für Hauptprogramm ----------

def connect_to_wifi(WIFI_ssid, WIFI_password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_ssid, WIFI_password)
    while not wlan.isconnected():
        print("Verbinde mit WLAN...")
        time.sleep(1)
    print("Verbunden! IP:", wlan.ifconfig())

    
def sub_LED(topic, msg):
    global led_on
    daten = ujson.loads(msg)
    schalter = daten.get('Schalter1')
    print(schalter)
    if schalter == "ON":     # LED einschalten
        led_on = True
        print("LED AN")
    
    else:
        global led_on
        led_on = False
        print("LED AUS")

#--------------- Verbindungen ---------------
connect_to_wifi(WIFI_ssid, WIFI_password)


#--------------- MQTT client erzeugen -------------

mqtt_client = MQTTClient(mqtt_client_id, ip_adresse_mqtt_server, keepalive=60)
mqtt_client.set_callback(sub_LED)
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
    except OSError as e:
        print("MQTT Fehler:", e)
        reconnect()
           
    if led_on:
        led.on()
    else:
        led.off()
    time.sleep(0.5) 
