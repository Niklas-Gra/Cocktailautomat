from machine import Pin
import time

# Pin 15 als digitalen Eingang definieren
eingang = Pin(15, Pin.IN)

while True:
    zustand = eingang.value()  # 0 = LOW, 1 = HIGH
    print("Pin 15 Zustand:", zustand)
    time.sleep(0.1)  # halbe Sekunde warten