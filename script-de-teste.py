#!/usr/bin/python3

# importa a API
from Recursos.DeviceManagerAPI import DeviceManager
import time

# instancia a classe da API passando o nome do cenario e o ip da cloudlet
DM = DeviceManager("tes", "192.168.0.107")

# guarda os dispositivos do cénario em uma variavel
dispositivos = DM.getDevices()

# inicia a app desejada nos dispositivos
for android in dispositivos:
	DM.start_app(android, "br.ufc.great.matrixoperation/.MainActivity")

# tempo para que o app descubra o cloudlet
print("\nTempo para os dispositivos se comunicarem com o cloudlet.")
time.sleep(15)

# define a qtd de repeticoes, a activity e os argumentos a serem executados
for android in dispositivos:
	DM.exec_activity(android, "br.ufc.great.matrixoperation/.MainActivity", "--es 'operation' 'mul' --ei 'size' 500", 5)
