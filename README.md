# androidTestBed
Ferramenta para a criação de ambientes de testes com dispositivos Android

## Primeiros passos
Primeiro é necessário saber qual a versão da API utilizado pela parte servidor do Docker:
```
# docker version
```
Se você não estiver utilizando a versão 1.26, é necessário modificar os arquivos criador.py e gerente.py nas linhas 12 e 14 respectivamente (a menor versão suportada é a 1.21).

O próximo passo é a criação da rede utilizada pelos containers (a subnet não é obrigatória):
```
# docker network create --subnet 10.0.0.0/16 isolated_nw
```

Fazendo o download das Imagens:
- Download da imagem do cliente:
   docker pull renanalves/android-testbed

- Download da imagem do servidor (nova versão disponível):
   docker pull renanalves/server-testbed

## Utilizando a ferramenta
Um vídeo demonstrando a instalação pode ser encontrado em:
https://youtu.be/7nu-24ESTl0

Alem de um vídeo demonstrando a ferramenta em execução:
https://youtu.be/uZj6Gl6R19Q

O passo a passo para a utilização da ferramenta e também como ela está estrutura podem ser visto no link abaixo:
http://www.repositorio.ufc.br/bitstream/riufc/29546/1/2017_tcc_rabarbosa.pdf

Repositório do aplicativo MatrixOperationsKotlin (nova versão disponível):
https://github.com/alvesRenan/KotlinMpOS
