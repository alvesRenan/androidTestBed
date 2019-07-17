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
        nome_cenario = input('Digite o nome do cenário que será configurado: ')

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
                    nome = input('Digite o nome do container: ')

                    # checagem se o nome já existe
                    if not self.gerente.container_existe(nome):
                        # se False

                        print('Configurações de rede disponíveis: umts, lte, full')
                        rede = input('Digite o nome da rede a ser usada ou defina o valor em kbps (Ex: 620.0): ')
                        regex = re.match('lte|umts|full|[0-9]', rede)

                        if regex is None:
                            print('Rede não compatível! Utilizando rede padrão \'full\'')
                            rede = 'full'

                        print('Configuração de memória RAM (em MB) do dispositivo (valor padrão 512 MB)')
                        memory = input('Digite a quantidade de memória do dispositivo: ')

                        try:
                            if int(memory) < 512:
                                memory = '512'
                        except:
                            print("Valor inválido, utilizando valor padrão.")
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
                        print('Nome não permitido ou container já existe!')

                if option == '2':
                    nome = input('Digite o nome do container: ')

                    # checagem se o nome já existe
                    if not self.gerente.container_existe(nome):
                        # se False
                        print('Defina a quantidade de memória do servidor ou deixe em vazio para não limitar.')
                        memory = input('Quantidade de memória do servidor em megabytes: ')

                        try:
                            if int(memory):
                                # the docker api I'm using requires the memory value
                                # and the unit, in this case m for megabytes
                                # so, for example, 512m or 1024m
                                memory = memory + 'm'
                        except:
                            print("Valor inválido, criando servidor sem limite de memória.")
                            memory = ''

                        print('Por padrão, não há limite na utilização de CPU.')
                        print('Limitar as CPU onde o container pode executar?')
                        cpus = input("Exemplo: '0.7' para 70% , 0.5 para 50% ou vazio para não limitar: ")

                        novo_container = Container(
                            nome_container=nome,
                            nome_cenario=nome_cenario,
                            memory=memory,
                            cpus=cpus)

                        bind_ports = input(
                            "Fazer o bind das portas? (S)im/(N)ão (Fazer o bind das portas impede que mais de um container servidor seja criado): ")

                        if bind_ports.lower() == 'n':
                            self.criador.criar_server(novo_container, False)
                            print("Após criar todos os servidores não esqueça de criar um container NGINX!")
                        else:
                            self.criador.criar_server(novo_container)

                    # se True
                    else:
                        print('Nome não permitido ou container já existe!')

                if option == '3':
                    os.system('clear')
                    self.gerente.listar_containers(nome_cenario)

                if option == '4':
                    nome = input('Digite o nome do container: ')

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
                    nome = input('Digite o nome do container: ')
                    if self.gerente.container_existe(nome):
                        self.gerente.restart_container(nome, nome_cenario)

                    else:
                        print('Container não existe!')

                if option == '8':
                    nome = input('Digite o nome do container: ')

                    if not self.gerente.container_existe(nome):
                        novo_container = Container(nome, nome_cenario)
                        self.criador.criar_nginx(novo_container)
                    else:
                        print("Nome não permitido ou container já existe!")

                if option == '9':
                    file_path = input("Caminho para o arquivo JSON: ")

                    self.criador.create_from_json(file_path, nome_cenario)

                if option == '10':
                    name = input("Input the device name shown on ADB: ")
                    self.criador.add_real_device(name, nome_cenario)

                if option == '11':
                    print('Esta ação pode demorar um pouco ...')
                    self.gerente.iniciar_cenario(nome_cenario)

                if option == '12':
                    print('Esta ação pode demorar um pouco ...')
                    self.gerente.parar_cenario(nome_cenario)
                    self.criador.delete_real_devices(nome_cenario)

                if option == '0':
                    sair = True

            self.menu()

        else:
            print('Cenário não existente. Use a opção \'Criar cenário\' ou a opção \'Listar cenários existentes\'')
            self.menu()

    def close(self):
        pass


MainScript()
