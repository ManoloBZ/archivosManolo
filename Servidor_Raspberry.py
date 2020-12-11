import socket
import RPi.GPIO as GPIO
from time import sleep
import threading
import datetime

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8080))
s.listen(5)

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(8,GPIO.OUT)
servo1 = GPIO.PWM(8,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

toggle=False;
TIEMPO = []
HORA_ACTUAL=datetime.datetime.now().strftime("%H")
MINUTO_ACTUAL=datetime.datetime.now().strftime("%M")
HORA="0"
MINUTO="0"

def ACTUADOR():
    servo1.ChangeDutyCycle(5.8)
    sleep(0.1)
    servo1.ChangeDutyCycle(0)
    sleep(1)
    servo1.ChangeDutyCycle(2)

def RCV_DATA():
    global HORA
    global MINUTO
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
        with clientsocket:
            while True:
                try:
                    x = clientsocket.recv(1024)#.decode("utf-8","strict")
                    y = bytearray(x)
                    del y[0]
                    del y[0]
                    Data = y.decode()
                    print(Data)
                    if Data:
                        TIEMPO.append(Data)
                except:
                    print(TIEMPO)
                    HORA = TIEMPO[0]
                    MINUTO = TIEMPO[1]
                    del TIEMPO[:]
                    print("Client Disconnected1")
                    break
                if not x:
                    print("Client Disconnected2")
                    break
def Hora_programada():
    global toggle
    toggle2 = False
    while True:
        HORA_ACTUAL=datetime.datetime.now().strftime("%H")
        MINUTO_ACTUAL=datetime.datetime.now().strftime("%M")
        H1 = int(HORA)
        H2 = int(HORA_ACTUAL)
        M1 = int(MINUTO)
        M2 = int(MINUTO_ACTUAL)
        print("Son las ", H2, ":",M2)
        if H1 and M1:
            print("La hora programada es ", H1, ":",M1)
            if H1==99 and M1 ==99 and (not toggle2):
                ACTUADOR()
                toggle2=True
            elif H1!=99:
                toggle2=False 
            if (H1==H2) and (M1==M2) and (not toggle):
                print("Se ha accionado el actuador")
                ACTUADOR()
                toggle= True
            elif H1 != H2 or M1 != M2:
                print("No es la Hora")
                toggle = False
        sleep(1)
P1 = threading.Thread(target=RCV_DATA)
P2 = threading.Thread(target=Hora_programada)
P1.start()
P2.start()
