## Para utilizar o programa, é necessário ter os seguintes pacotes de python:
- requests
- matplotlib
- numpy
- pandas
- csv


## Prepare um arquivo de entrada (por exemplo, 'brasil.in') com uma cidade e seu estada em cada uma das linhas. Exemplo:

Santo André,SP\
São Paulo,SP\
Rio de Janeiro,RJ


## Para rodar o programa, basta rodar o script seguido com o arquivo das cidades ('brasil.in' no meu caso):

python corona_brasil.py brasil.in


Notas importantes: 

O gráfico do total do Brasil está incorreto por enquanto, será corrigido em breve

Os dados são agrupados em semanas para diminuir flutuação, portanto o último ponto pode estar em uma semana incompleta e provavelmente será menor que os outros. Deve ser desconsiderado!
