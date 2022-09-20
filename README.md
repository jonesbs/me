## Conversor de logs

### Requisitos
Python 3.9+

### Instalação
Execute os comandos abaixo para iniciar a instalação de dependencias:

```
$ make init
```

O comando acima irá criar um ambiente virtual e instalar as dependencias necessarias e preparar o schema do banco.
Nesse exemplo em questão foi utilizado o banco de dados SQLite devido a facilidade de portabilidade.


### Execução

```
$ make import
```
O comando acima irá importa o arquivo *logs.txt* dentro da pasta do projeto.

--------

```
$ make report
```
O comando acima irá criar três arquivos com final *report.csv* dentro da pasta do projeto.

------

### Obesrvações do projeto

Foi levado em consideração a necessidade de eficiencia em termos de uso de memoria, por tanto foi utilizado ao maximo o recurso de processamento
assincrono e uso de cursor para evitar o uso excessivo de memoria e permitir que o sistema possa processar arquivos grandes.




