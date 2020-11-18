import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.105",8080))

while True:
    x=input("Ingrese 1 o 0 para conmutar")
    s.send(bytes(x,"utf-8"))