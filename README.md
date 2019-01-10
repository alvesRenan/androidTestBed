# androidTestBed
Ferramenta para a criação de ambientes de testes com dispositivos Android

## Primeiros passos
Primeiro é necessário saber qual a versão da API utilizado pela parte servidor do Docker:
```
# docker version
```
Se você não estiver utilizando a versão 1.26, é necessário modificar os arquivos criador.py e gerente.py nas linhas 12 e 14 respectivamente (a menor versão suportada é a 1.21).

Fazendo o download das Imagens:
- Download da imagem do cliente:
   docker pull renanalves/android-testbed

- Download da imagem do servidor (nova versão disponível):
   docker pull renanalves/server-testbed

## Utilizando a ferramenta

OBS.: Os vídeos são de uma versão mais antiga da ferramenta mas ainda são válidos poís houveram apenas adições de novas opções e refinamento das antigas.

Um vídeo demonstrando a instalação pode ser encontrado em:
https://youtu.be/7nu-24ESTl0

Alem de um vídeo demonstrando a ferramenta em execução:
https://youtu.be/uZj6Gl6R19Q

O passo a passo para a utilização da ferramenta e também como ela está estrutura podem ser visto no link abaixo:
http://www.repositorio.ufc.br/bitstream/riufc/29546/1/2017_tcc_rabarbosa.pdf

Repositório do aplicativo MatrixOperationsKotlin:
https://github.com/alvesRenan/KotlinMpOS
