# -*- coding: utf-8 -*-

import os
import time
import random
import sqlite3
import Recursos.comandos as comandos
import threading
import subprocess as sp

class Android():
	
	def __init__(self, nome, console, vnc, rede):
		self._nome = nome
		self._console = console
		self._vnc = vnc
		self._rede = rede

	def getNome(self):
		return self._nome

	def getConsole(self):
		return self._console

	def getVNC(self):
		return self._vnc

	def getRede(self):
		return self._rede

	def start_app(self, activity, ip_cloudlet):
		console = self.getConsole()
		os.system(comandos.ACTIVITY % (console, activity))
		os.system(comandos.SET_CLOUDLET % (console, activity, ip_cloudlet))

	def exec_run(self, activity, ip_cloudlet, argumentos, repeticoes):
		num_interacoes = 1

		# ciclo de repeticoes da activity
		while num_interacoes <= repeticoes:
			print("Interacao numero %i do dispositivo %s" % (num_interacoes, self.getNome()))

			# chamada da activity
			os.system(comandos.EXEC % (self.getConsole(), activity, ip_cloudlet, argumentos))

			# loop para esperar os resultados
			while True:
				# captura dos resultados do logcat do dispositivo e escreve em um arquivo com o mesmo nome do container
				self.getResults()

				try:
					# retorna a quantidade de linhas do arquivo
					lines = sp.getoutput(comandos.COUNT_LINES % self.getNome())
					# se a quantidade for igual ao numero de repeticoes
					# a acitvity ja foi executado e pode-se ir para a proxima interacao
					if int(lines) == num_interacoes:
						num_interacoes += 1
						break
					# caso contratio o loop continua
				except:
					time.sleep(1)

		print("Execucoes do dispositivo %s foram concluidas!" % self.getNome())

	def getResults(self):
		os.system(comandos.RESULTS % (self.getConsole(), self.getNome()))

	def run(self, activity, ip_cloudlet, argumentos, repeticoes):
		android_thread = threading.Thread(target=self.exec_run, args=(activity, ip_cloudlet, argumentos, repeticoes,))
		android_thread.start()

class DeviceManager():

	def __init__(self, nome_cenario, ip_cloudlet):
		self.nome_cenario = nome_cenario
		self.ip_cloudlet = ip_cloudlet

	def getDevices(self):
		# conexão com a database
		conn = sqlite3.connect('DB/mydb.db')
		cur = conn.cursor()

		self.devices = []

		# seleção dos dispositivos que fazem parte do cenário e estão ativos
		cur.execute('SELECT * FROM containers WHERE nome_cenario = :nome AND estado_container = :estado AND is_server = 0',
					{ 'nome': self.nome_cenario, 'estado': 'EXECUTANDO' }
				)
		res = cur.fetchall()

		for i in range(len(res)):
			# 0 -> nome_cenario; 1 -> nome_container; 2 -> porta_6080; 3 -> porta do adb 5 -> rede; 6 -> estado

			console = res[i][3]
			vnc = 'localhost:%s' % str(res[i][2])

			# criação do objeto android
			android = Android(res[i][1], console, vnc, res[i][6])

			# lista com os dipositivos
			self.devices.append(android)

		# encerra a conexão
		conn.close()

		# retorna a lista com objetos
		return self.devices

	def start_app(self, android, activity):
		# iniciar o app e definir a cloudlet
		# exemplo: voce faz um for na lista de dispositivos e executa o metodo start_app para cada dispositivo na lista
		# for device in api.getDevices(cenario):
		# 	api.start_app(device, activity, argumentos)
		
		android.start_app(activity, self.ip_cloudlet)

	def exec_activity(self, android, activity, argumentos, repeticoes):
		android.run(activity, self.ip_cloudlet, argumentos, repeticoes)