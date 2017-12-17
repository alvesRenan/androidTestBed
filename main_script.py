# -*- coding: utf-8 -*-

import os
import comandos
from criador import Criador
from gerente import Gerente
from class_container import Container

class Main_Script():

	def __init__(self):
		# outros scripts
		self.criador = Criador()
		self.gerente = Gerente()

		self.menu()

	def menu(self):
		print('===================================================')
		print('1 -> Criar cenário')
		print('2 -> Listar cenários existentes')
		print('3 -> Opções para cenários existentes')
		print('4 -> Excluir cenário')
		print('0 -> Sair')
		print('===================================================')
		option = input(">> ")

		if (option == '1'):
			self.criar_cenario()

		if (option == '2'):
			os.system('clear')
			self.gerente.listar_cenarios()
			self.menu()

		if (option == '3'):
			self.config_cenario()

		if (option == '4'):
			self.deleta_cenario()

		if (option == '0'):
			self.close()

	def criar_cenario(self):
		nome = input('Nome do novo cenário: ')
		
		# se False ele chama esta função novamente para a inserção de outro nome
		if (self.criador.criar_cenario(nome) == False):
			self.criar_cenario()

		self.menu()

	def deleta_cenario(self):
		os.system('clear')
		self.gerente.listar_cenarios()
		nome = input('Nome do cenário que será excluido: ')

		if (not self.gerente.cenario_existe(nome)):
			self.criador.deleta_cenario(nome)

		self.menu()

	def config_cenario(self):
		sair = False
		nome_cenario = input('Digite o nome do cenário: ')

		os.system('clear')

		# caso retorne False quer dizer que o cenário já existe, caso contrário deve ser usada a opção 'Criar cenário'
		if (self.gerente.cenario_existe(nome_cenario) == False):
			while (sair == False):
				check = False

				print('=======================================')
				print('Opções de Cenários:\n')
				print('1 -> Adicionar cliente')
				print('2 -> Adicionar servidor')
				print('3 -> Listar containers do cenário')
				print('4 -> Apagar container')
				print('5 -> Conectar-se aos dispositivos')
				print('6 -> Instalar APP')
				print('8 -> Iniciar cenário')
				print('9 -> Parar cenário')
				print('0 -> Voltar para o menu principal')
				print('=======================================')
				option = input('>> ')

				# carcterísticas do container cliente que será criado
				if (option == '1'):
					while (check == False):
						#tipo = 'cliente'
						nome = input('Digite o nome do container: ')
						
						# checagem se o nome já existe
						if (self.gerente.container_existe(nome) == False):
						# se False
							
							print('Configurações de rede disponíveis: umts, lte, full')
							regex = ['umts', 'lte', 'full']

							rede = input('Digite o nome da rede a ser usada: ')
							if (rede not in regex):
								os.system('clear')
								print('Rede não compatível!')
								self.gerente.listar_containers(nome_cenario)
								self.config_cenario()

							# criação do objeto Container
							novo_container = Container(nome, nome_cenario)
							# cria o container e insere no banco de dados
							self.criador.criar_cliente(novo_container, rede)
							

						# se True
						else:
							print('O nome já existe!')

						# fim do loop
						check = True

				if (option == '2'):
					while (check == False):
						#tipo = 'server'
						nome = input('Digite o nome do container: ')

						# checagem se o nome já existe
						if (self.gerente.container_existe(nome) == False):
						# se False
							novo_container = Container(nome, nome_cenario)
							self.criador.criar_server(novo_container)

						# se True
						else:
							print('O nome já existe!')

						# fim do loop
						check = True

				if (option == '3'):
					os.system('clear')
					self.gerente.listar_containers(nome_cenario)

				if (option == '4'):
					nome = input('Digite o nome do container: ')
					
					if (self.gerente.container_existe(nome) == True):
						self.criador.deleta_container(nome)

					else:
						print('Container não existe ou não faz parte deste cenário!')

				if (option == '5'):
					self.gerente.conectar_dispositivos(nome_cenario)

				if (option == '6'):
					apk  = input('Digite o caminho do apk: ')
					self.gerente.install_app(apk, nome_cenario)

				if (option == '8'):
					print('Esta ação pode demorar um pouco ...')
					self.gerente.iniciar_cenario(nome_cenario)

				if (option == '9'):
					print('Esta ação pode demorar um pouco ...')
					self.gerente.parar_cenario(nome_cenario)

				if (option == '0'):
					sair = True
			
			self.menu()

		else:
			print('Cenário não existente. Use a opção \'Criar cenário\' ou a opção \'Listar cenários existentes\'')
			self.menu()

	def close(self):
		pass

Main_Script()