#!/usr/bin/python3

import time

# importa a API
from DeviceManagerAPI import DeviceManager

# instancia a classe da API passando o nome do cenario e o ip da cloudlet
DM = DeviceManager("cenario-2", "10.0.0.2")

# guarda os dispositivos do cénario em uma variavel
dispositivos = DM.getDevices()

# inicia a app desejada nos dispositivos
for android in dispositivos:
	DM.start_app(android, "br.ufc.great.matrixoperation/.MainActivity")
	time.sleep(5)

# define a qtd de repeticoes, a activity e os argumentos a serem executados
for android in dispositivos:
	DM.exec_activity(android, "br.ufc.great.matrixoperation/.MainActivity", "--es 'operation' 'mul' --ei 'size' 500", 5)
