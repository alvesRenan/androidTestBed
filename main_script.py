# -*- coding: utf-8 -*-

import os
import re
from Componentes.criador import Criador
from Componentes.gerente import Gerente
from Recursos.class_container import Container


class MainScript:

    def __init__(self):
        # outros scripts
        self.criador = Criador()
        self.gerente = Gerente()

        self.menu()

    def menu(self):
        print('===================================================')
        print('1 -> Create scenario')
        print('2 -> List existing scenarios')
        print('3 -> Options for scenarios')
        print('4 -> Exclude scenario')
        print('0 -> Exit')
        print('===================================================')
        option = input(">> ")

        if option == '1':
            self.criar_cenario()

        if option == '2':
            os.system('clear')
            self.gerente.listar_cenarios()
            self.menu()

        if option == '3':
            self.config_cenario()

        if option == '4':
            self.deleta_cenario()

        if option == '0':
            self.close()

    def criar_cenario(self):
        nome = input('Name of the new scenario: ')
        self.criador.criar_cenario(nome)

        self.menu()

    def deleta_cenario(self):
        os.system('clear')
        self.gerente.listar_cenarios()
        nome = input('Name of scenario to be removed: ')

        if not self.gerente.cenario_existe(nome):
            self.criador.deleta_cenario(nome)
            self.criador.delete_real_devices(nome)

        self.menu()

    def config_cenario(self):
        sair = False
        os.system('clear')
        self.gerente.listar_cenarios()
        nome_cenario = input('Enter the name of the scenario to be configured: ')

        os.system('clear')

        # caso retorne False quer dizer que o cenário já existe, caso contrário deve ser usada a opção 'Criar cenário'
        if not self.gerente.cenario_existe(nome_cenario):
            while not sair:
                print('=======================================')
                print('Scenario Options:')
                print('1 -> Add client')
                print('2 -> Add server')
                print('3 -> List containers of the scenario')
                print('4 -> Delete container')
                print('5 -> Connect to devices')
                print('6 -> Install APP')
                print('7 -> Restart a container')
                print('8 -> Create Nginx container')
                print('9 -> Load scenario from JSON')
                print('10 -> Add real device')
                print('11 -> Start scenario')
                print('12 -> Stop scenario')
                print('0 -> Back to main menu')
                print('=======================================')
                option = input('>> ')

                # carcterísticas do container cliente que será criado
                if option == '1':
                    nome = input('Enter the container name: ')

                    # checagem se o nome já existe
                    if not self.gerente.container_existe(nome):
                        # se False

                        print('Available network configurations: umts, lte, full')
                        rede = input('Entre the name of the network or define the value to be used in kbps (Ex: 620.0): ')
                        regex = re.match('lte|umts|full|[0-9]', rede)

                        if regex is None:
                            print('Network not supported! Using default network \'full\'')
                            rede = 'full'

                        print('Memory value (in MB) of the device (defalt value 512 MB)')
                        memory = input('Input the amount of memmory the device will have: ')

                        try:
                            if int(memory) < 512:
                                memory = '512'
                        except:
                            print("Invalid value, using default value.")
                            memory = '512'

                        # criação do objeto Container
                        novo_container = Container(
                            nome_container=nome,
                            nome_cenario=nome_cenario,
                            memory=memory)
                        # cria o container e insere no banco de dados
                        self.criador.criar_cliente(novo_container, rede)

                    # se True
                    else:
                        print('Name not allowed or already in use!')

                if option == '2':
                    nome = input('Enter the container name: ')

                    # checagem se o nome já existe
                    if not self.gerente.container_existe(nome):
                        # se False
                        print('Define the amount of memory the server or leave it empty to not limit.')
                        memory = input('Amount of memory of the server in megabytes: ')

                        try:
                            if int(memory):
                                # the docker api I'm using requires the memory value
                                # and the unit, in this case m for megabytes
                                # so, for example, 512m or 1024m
                                memory = memory + 'm'
                        except:
                            print("Invalid value, creating server with no memory limit.")
                            memory = ''

                        print('By default, there is no memory CPU utilization lmit.')
                        print('Limit the CPUs where the container can execute?')
                        cpus = input("Example: '0.7' for 70% , 0.5 for 50% or empty to not limit: ")

                        novo_container = Container(
                            nome_container=nome,
                            nome_cenario=nome_cenario,
                            memory=memory,
                            cpus=cpus)

                        bind_ports = input(
                            "Bind ports? (Y)es/(N)o (Making the port bind prevents more than one server container to be created): ")

                        if bind_ports.lower() == 'n':
                            self.criador.criar_server(novo_container, False)
                            print("After creating all the servers don't forget to create a Nginx container!")
                        else:
                            self.criador.criar_server(novo_container)

                    # se True
                    else:
                        print('Nome não permitido ou container já existe!')

                if option == '3':
                    os.system('clear')
                    self.gerente.listar_containers(nome_cenario)

                if option == '4':
                    nome = input('Enter the container name: ')

                    if self.gerente.container_existe(nome):
                        self.criador.deleta_container(nome)

                    else:
                        print('Container não existe ou não faz parte deste cenário!')

                if option == '5':
                    self.gerente.conectar_dispositivos(nome_cenario)

                if option == '6':
                    apk = input('Digite o caminho do apk: ')
                    self.gerente.install_app(apk, nome_cenario)

                if option == '7':
                    nome = input('Enter the container name: ')
                    if self.gerente.container_existe(nome):
                        self.gerente.restart_container(nome, nome_cenario)

                    else:
                        print('Container não existe!')

                if option == '8':
                    nome = input('Enter the container name: ')

                    if not self.gerente.container_existe(nome):
                        novo_container = Container(nome, nome_cenario)
                        self.criador.criar_nginx(novo_container)
                    else:
                        print("Name not allowed or already in use!")

                if option == '9':
                    file_path = input("Path to JSON file: ")

                    self.criador.create_from_json(file_path, nome_cenario)

                if option == '10':
                    name = input("Input the device name shown on ADB: ")
                    self.criador.add_real_device(name, nome_cenario)

                if option == '11':
                    print('This may take a while ...')
                    self.gerente.iniciar_cenario(nome_cenario)

                if option == '12':
                    print('This may take a while ...')
                    self.gerente.parar_cenario(nome_cenario)
                    self.criador.delete_real_devices(nome_cenario)

                if option == '0':
                    sair = True

            self.menu()

        else:
            print("Scenario not existent. Use the 'Create scenario' option or 'List existing scenarios'")
            self.menu()

    def close(self):
        pass


MainScript()
