# -*- coding: utf-8 -*-

import os
import time
import random
import sqlite3
import Recursos.comandos as comandos
import threading
import subprocess as sp

class Android():

	def __init__(self, nome, console, vnc, rede, time_stamp):
		self.nome = nome
		self.console = console
		self.vnc = vnc
		self.rede = rede
		self.time_stamp = time_stamp

	def start_app(self, activity, ip_cloudlet):
		# Inicia o app
		os.system(comandos.ACTIVITY % (self.console, activity))
		# Define o IP da cloudlet
		os.system(comandos.SET_CLOUDLET % (self.console, activity, ip_cloudlet))

	def exec_run(self, action, ip_cloudlet, argumentos, repeticoes):
		# limpa o logcat para remover resultados de experimentos anteriores
		os.system(comandos.CLEAR_LOG % self.console)

		num_interacoes = 1

		# ciclo de repeticoes da activity
		while num_interacoes <= repeticoes:
			print("Interacao numero %i do dispositivo %s" % (num_interacoes, self.nome))

			# chamada da activity
			os.system(comandos.EXEC % (self.console, action, argumentos))

			# loop para esperar os resultados
			while True:
				# captura dos resultados do logcat do dispositivo e escreve em um arquivo
				# com o mesmo nome do container
				self.get_results()

				try:
					# retorna a quantidade de linhas do arquivo
					lines = sp.getoutput(comandos.COUNT_LINES % (self.time_stamp, self.nome))
					# se a quantidade for igual ao numero de repeticoes
					# a acitvity ja foi executado e pode-se ir para a proxima interacao
					if int(lines) == num_interacoes:
						num_interacoes += 1
						break
					# caso contratio o loop continua
				except:
					time.sleep(1)

		print("Execucoes do dispositivo %s foram concluidas!" % self.nome)

	def get_results(self):
		os.system(comandos.RESULTS % (self.console, self.time_stamp, self.nome))
		os.system(comandos.ERRORS % (self.console, self.time_stamp, 'errors-' + self.nome))

	def run(self, action, ip_cloudlet, argumentos, repeticoes):
		# time.sleep(random.randrange(1, 5))

		android_thread = threading.Thread(target=self.exec_run, args=(action, ip_cloudlet, argumentos, repeticoes,))
		android_thread.start()

class DeviceManager():

	def __init__(self, nome_cenario, ip_cloudlet):
		self.nome_cenario = nome_cenario
		self.ip_cloudlet = ip_cloudlet

		# cria a pasta para guardar os arquivos de saida
		self.time_stamp = time.strftime("%d-%m-%Y_%H:%M:%S")
		os.mkdir(self.time_stamp)

	def get_devices(self):
		# conexão com a database
		conn = sqlite3.connect('DB/mydb.db')
		cur = conn.cursor()

		devices = []

		# seleção dos dispositivos que fazem parte do cenário e estão ativos
		cur.execute('SELECT * FROM containers WHERE nome_cenario = :nome AND estado_container = :estado AND is_server = 0',
					{ 'nome': self.nome_cenario, 'estado': 'EXECUTANDO' }
				)
		res = cur.fetchall()

		for i in range(len(res)):
			""" 
				0 -> nome_cenario
				1 -> nome_container
				2 -> porta_6080
				3 -> porta_5554
				4 -> porta_5555
				5 -> rede
				6 -> estado
				7 -> servidor ou não 
				8 -> memoria
				9 -> cpus
			"""
			vnc = 'localhost:%s' % str(res[i][2])

			# criação do objeto android
			android = Android(res[i][1], res[i][3], vnc, res[i][5], self.time_stamp)

			# lista com os dipositivos
			devices.append(android)

		# encerra a conexão
		conn.close()

		# retorna a lista com objetos
		return devices

	def start_app(self, android, activity):
		android.start_app(activity, self.ip_cloudlet)
		print("Stated activity {} on device {}".format(activity, androi.nome))

	def exec_activity(self, android, action, argumentos, repeticoes):
		android.run(action, self.ip_cloudlet, argumentos, repeticoes)
