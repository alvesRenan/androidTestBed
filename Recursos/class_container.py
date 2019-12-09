class Container:
	
	def __init__(self, nome_container, nome_cenario, cpus=None, memory=None):
		# nome do container
		self.nome = nome_container
		# cenario ao qual o container pertence
		self.cenario = nome_cenario
		# qtd de memoria RAM
		self.memory = memory
		# cps disponiveis para o container
		self.cpus = cpus
