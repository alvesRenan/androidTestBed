# -*- coding: utf-8 -*-

import os
import time
import docker
import sqlite3
import Recursos.comandos as comandos
import subprocess as sp
from texttable import Texttable

class Gerente():
	def __init__(self):
		# conexão com o docker, utilize o comando 'docker version' e descubra a versão da API do servidor
		self.client = docker.from_env(version='1.26')
		# conexao com o sqlite
		self.conn = sqlite3.connect('DB/mydb.db')
		# criacao do cursor
		self.cur = self.conn.cursor()

	def listar_cenarios(self):
		self.cur.execute('SELECT * FROM cenarios')
		res = self.cur.fetchall()

		table = Texttable()
		table.add_row(['Nome do Cenário', 'Estado do Ceńário'])

		for i in range(len(res)):
			# posição 0 contém o nome e posição 1 o estado
			table.add_row([res[i][0], res[i][1]])

		print(table.draw())

	# cria a tabela de listagem dos containers
	def listar_containers(self, nome_cenario):
		self.cur.execute('SELECT * FROM containers WHERE nome_cenario = :nome', { 'nome': nome_cenario })
		res = self.cur.fetchall()

		table = Texttable()
		table.header(['Nome Container', 'IP', 'VNC', 'Emulador', 'Rede', 'Memória', 'Estado'])

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
			"""
			
			# coletando o IP do container
			ip = sp.getoutput(comandos.GET_IP % res[i][1])

			if res[i][7] == 0:
				# criando o edereço para o noVNC
				vnc = 'localhost:%s' % str(res[i][2])
				memory = res[i][8]
				console_adb = 'emulator-%s' % str(res[i][3])
			else:
				vnc = 'NONE'
				memory = 'NONE'
				console_adb = 'NONE'

			# configurações de formatação da tabela
			table.set_cols_width([12, 10, 15, 15, 5, 8, 15])
			table.set_cols_align(['l', 'c', 'c', 'c', 'c', 'c', 'c'])

			# adiciona uma linha na tabela
			table.add_row([res[i][1], ip, vnc, console_adb, res[i][5], memory, res[i][6]])

		# mostra a tabela
		print(table.draw())

	def listar_console_dispositivos(self, nome_cenario):
		self.cur.execute('SELECT porta_5554 FROM containers WHERE nome_cenario = :nome AND is_server = :var', { 'nome': nome_cenario, 'var': 0 })
		consoles = []

		for i in self.cur.fetchall():
			consoles.append(i[0])

		return consoles

	# checa se um cenário existe
	def cenario_existe(self, nome_cenario):
		# coloca o nome em formato de tupla para comparacao futura
		nome = (nome_cenario,)
		
		self.cur.execute("SELECT nome_cenario FROM cenarios WHERE nome_cenario = :nome", { 'nome': nome_cenario })
		resultado = self.cur.fetchall()

		# checagem de nome unico
		for i in resultado:
			# comparacao com as tuplas retornadas
			if i == nome:
				return False

		return True

	# checa se o container existe
	def container_existe(self, nome_container):
		# coloca o nome em formato de tupla para comparacao futura
		nome = (nome_container,)
		self.cur.execute("SELECT nome_container FROM containers")
		
		# checagem por nome repetido de containers
		for i in self.cur.fetchall():
			if i == nome:
				# nome existe
				return True

		# nome nao existe
		return False

	def iniciar_emulador(self, lista_containers):
		time.sleep(10)

		for container in self.client.containers.list(all=True):
			for i in lista_containers:
				# posição 0 contém o nome do container a posição 1 contém o tipo de rede que ele deve usar
				if i[0] == container.name:
					# posição 2 diz se ele é cliente ou servidor
					if i[2] == 0:
						try:
							# posição 3 tem a qtd de memoria usada pelo emulador
							container.exec_run(comandos.START_EMU % (i[1], i[3]), detach=True)
						except:
							pass

	def iniciar_cenario(self, nome_cenario):
		# retorna o nome e o tipo de rede de containers em estado PARADO ou CRIADO do cenário
		self.cur.execute(
			'SELECT nome_container, rede, is_server, memory FROM containers WHERE nome_cenario = ? AND (estado_container = ? OR estado_container = ?)', 
			(nome_cenario, 'CRIADO', 'PARADO')
		)
		resultado = self.cur.fetchall()

		# lista de containers ativos
		for container in self.client.containers.list(all=True):
			# resultado dos containers que fazem parte do cenário
			for i in resultado:
				# posição 0 contém o nome do container a posição 1 contém o tipo de rede que ele deve usar
				if i[0] == container.name:
					# caso seja um container cliente
					if i[2] == 0:
						# inicia o container
						container.restart()
					# caso seja um container servidor
					else:
						# inicia o container
						container.restart()
						# captura o ip do container
						ip_servidor = sp.getoutput(comandos.GET_IP % i[0])
						# forma um comando sed
						cmd = comandos.MPOS_IP_CHANGE % ip_servidor
						# configura o IP do container no arquivo de configuração do MpOS
						container.exec_run("sh -c '%s'" % cmd)
						# inicia o cloudlet
						container.exec_run("sh -c '%s'" % comandos.START_MPOS, detach=True)

					# atualiza o estado do container no banco para EXECUTANDO
					with self.conn:
						try:
							self.cur.execute("UPDATE containers SET estado_container = ? WHERE nome_container = ?", ('EXECUTANDO', i[0]))
						except Exception as e:
							raise e

		self.iniciar_emulador(resultado)

		# atualiza o estado cenario no banco para ATIVO
		with self.conn:
			try:
				self.cur.execute("UPDATE cenarios SET estado_cenario = :novo_estado WHERE nome_cenario = :nome", { 'novo_estado': 'ATIVO', 'nome': nome_cenario })
			except Exception as e:
				raise e

	def parar_cenario(self, nome_cenario):
		self.cur.execute(
			'SELECT nome_container, is_server FROM containers WHERE nome_cenario = ? AND (estado_container = ? OR estado_container = ?)', 
			(nome_cenario, 'CRIADO', 'EXECUTANDO')
		)
		
		resultado = self.cur.fetchall()

		for container in self.client.containers.list():
			for i in resultado:
				# posição 0 contém o nome do container a posição 1 diz se o container é cliente ou servidor
				if i[0] == container.name:
					# se for servidor
					if i[1] == 1:
						# coleta o IP do servidor
						ip_servidor = sp.getoutput(comandos.GET_IP % container.name)
						# forma o comando sed
						cmd = comandos.MPOS_DEFAULT % ip_servidor
						# retira o IP do servidor no arquivo config.properties
						container.exec_run("sh -c '%s'" % cmd)

					# para o cintainer
					container.stop()

					# atualiza o estado do container no banco para PARADO
					with self.conn:
						try:
							self.cur.execute("UPDATE containers SET estado_container = ? WHERE nome_container = ?", ('PARADO', i[0]))
						except Exception as e:
							raise e

		# atualiza o estado cenario no banco para ATIVO
		with self.conn:
			try:
				self.cur.execute("UPDATE cenarios SET estado_cenario = :novo_estado WHERE nome_cenario = :nome", { 'novo_estado': 'PARADO', 'nome': nome_cenario })
			except Exception as e:
				raise e # Latest commit a9494d7  4 days ago


	# conexão com os emuladores pelo adb
	def conectar_dispositivos(self, nome_cenario):
		os.system(comandos.ADB_KILL)
		output = sp.getoutput(comandos.ADB_START)
		# os.system(comandos.ADB_START)

		print(output)
			
	# instalar app
	def install_app(self, apk, nome_cenario):
		consoles = self.listar_console_dispositivos(nome_cenario)

		for i in consoles:
			saida = os.system(comandos.INSTALL_APP % (i, apk))
			print(saida)

	def restart_container(self, nome_container):
		for container in self.client.containers.list():
			if container.name == nome_container:
				print('Reiniciando o container %s' % nome_container)
				container.restart()

				with self.conn:
					self.cur.execute(
						'SELECT nome_container, rede, is_server, memory FROM containers WHERE nome_container = ? AND estado_container = ?',
						(nome_container, 'EXECUTANDO'))

					resultado = self.cur.fetchall()

				print('Reiniciando o emulador no container %s' % nome_container)
				self.iniciar_emulador(resultado)
