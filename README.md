# androidTestBed
Ferramenta para a criação de ambientes de testes com dispositivos Android

- Download da imagem do cliente:
   docker pull renanalves/android-testbed

- Download da imagem do servidor:
   docker pull renanalves/server-testbed

## Primeiros passos
Primeiro é necessário saber qual a versão da API utilizado pela parte servidor do Docker:
```
# docker version
```
Se você não estiver utilizando a versão 1.26, é necessário modificar os arquivos criador.py e gerente.py nas linhas 12 e 14 respectivamente (A menor versão suportada é a 1.21).

O próximo passo é a criação da rede utilizada pelos containers (a subnet não é obrigatória):
```
# docker network create --subnet 10.0.0.0/16 isolated_nw
```
## Utilizando a ferramenta
O passo a passo para a utilização da ferramenta e também como ela está estrutura podem ser visto no link abaixo:
https://www.dropbox.com/s/bipjyqt5npdad5e/TCC_II_Renan.pdf?dl=0
