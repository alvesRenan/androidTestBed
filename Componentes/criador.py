# -*- coding: utf-8 -*-

import docker
import sqlite3
from .gerente import Gerente

class Criador():
	
	def __init__(self):
		self.gerente = Gerente()
		# conexão com o docker, utilize o comando 'docker version' e descubra a versão da API do servidor
		self.client = docker.from_env(version='1.26')
		# conexao com o sqlite
		self.conn = sqlite3.connect('DB/mydb.db')
		# criacao do cursor
		self.cur = self.conn.cursor()
		# tantativa de criacao da tabela containers e cenarios
		with self.conn:
			self.cur.execute(
				"""CREATE TABLE IF NOT EXISTS  containers (
						nome_cenario text,
						nome_container text,
						porta_6080 integer,
						porta_5554 integer,
						porta_5555 integer,
						rede text,
						estado_container text default 'CRIADO',
						is_server integer default 0,
						memory text,
						cpus text
					)"""
				)

			self.cur.execute(
				"""CREATE TABLE IF NOT EXISTS cenarios(
						nome_cenario text,
						estado_cenario text default 'PARADO'
					)"""
				)

		# procurar as maiores portas em uso e definindo o valor das portas para novos containers
		self.cur.execute('SELECT MAX(porta_6080) FROM containers')
		resposta = self.cur.fetchone()
		if resposta[0] == None:
			self.porta_6080 = 6080
		else:
			self.porta_6080 = resposta[0] + 1

		self.cur.execute('SELECT MAX(porta_5554) FROM containers')
		resposta = self.cur.fetchone()
		if resposta[0] == None:
			self.porta_5554 = 5554
		else:
			self.porta_5554 = resposta[0] + 2

		self.cur.execute('SELECT MAX(porta_5555) FROM containers')
		resposta = self.cur.fetchone()
		if resposta[0] == None:
			self.porta_5555 = 5555
		else:
			self.porta_5555 = resposta[0] + 2

	def criar_cenario(self, nome_cenario):
		if self.gerente.cenario_existe(nome_cenario):
			# insercao no arquivo mydb.db
			with self.conn:
				try:
					self.cur.execute(
						"INSERT INTO cenarios (nome_cenario) VALUES (:nome)",
						{'nome': nome_cenario}
					)

					print('Cenario criado')

					return True
				
				except Exception as e:
					print(e)
					return False
		else:
			print('O nome ja existe!')
			return False

	def deleta_cenario(self, nome_cenario):
		self.cur.execute('SELECT nome_container FROM containers WHERE nome_cenario = :nome', {'nome': nome_cenario})
		res = self.cur.fetchall()

		for i in range(len(res)):
			for container in self.client.containers.list(all=True):
				if container.name == res[i][0]:
					self.deleta_container(container.name)

		with self.conn:
			try:
				self.cur.execute('DELETE FROM cenarios WHERE nome_cenario = :nome', {'nome': nome_cenario})
			except Exception as e:
				raise e

	def criar_cliente(self, novo_container, rede):
		with self.conn:
			try:
				self.cur.execute(
					"INSERT INTO containers (nome_cenario, nome_container, porta_6080, porta_5554, porta_5555, rede, memory, cpus) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
					(novo_container.cenario, novo_container.nome, self.porta_6080, self.porta_5554, self.porta_5555, rede, novo_container.memory, novo_container.cpus)
				)

				self.client.containers.run(
					'renanalves/android-testbed',
					cap_add=['NET_ADMIN'],
					detach=True,
					privileged=True,
					# network='isolated_nw',
					publish_all_ports=True,
					name=novo_container.nome,
					ports={
						'6080/tcp': self.porta_6080,
						'5554/tcp': self.porta_5554,
						'5555/tcp': self.porta_5555
					}
				)
				
				self.porta_6080 += 1
				self.porta_5554 += 2
				self.porta_5555 += 2

			except Exception as e:
				print(e)
				return 0

	def  criar_server(self, novo_container):
		self.client.containers.run(
			'renanalves/server-testbed',
			detach=True,
			tty=True,
			stdin_open=True,
			privileged=True,
			# network = 'isolated_nw',
			ports={
				'30015/tcp': 30015,
				'31000/tcp': 31000,
				'36114/tcp': 36114,
				'36381/tcp': 36381,
				'36415/tcp': 36415,
				'36241/tcp': 36241,
				'40000/tcp': 40000,
				'40001/tcp': 40001,
				'40005/tcp': 40005,
				'40006/tcp': 40006,
				'40010/tcp': 40010,
				'40011/tcp': 40011,
				'40020/tcp': 40020
			},
			publish_all_ports=True,
			cap_add=['NET_ADMIN'],
			name=novo_container.nome,
			cpuset_cpus=novo_container.cpus
		)

		with self.conn:
			try: 
				self.cur.execute(
					"INSERT INTO containers (nome_cenario, nome_container, porta_6080, porta_5554, porta_5555, rede, is_server, cpus) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
					(novo_container.cenario, novo_container.nome, None, None, None, None, 1, novo_container.cpus)
				)

			except Exception as e:
				print(e)

	def deleta_container(self, nome_container):
		for container in self.client.containers.list(all=True):
			if container.name == nome_container:
				print('Deletando o container %s' % container.name)
				container.remove(force=True)
				
				with self.conn:
					self.cur.execute('DELETE FROM containers WHERE nome_container = :nome', {'nome': nome_container})

