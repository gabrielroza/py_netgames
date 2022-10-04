# Exemplo de uso

Para executar um exemplo de uso é necessário ter [instalado o pipenv](https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv). Pipenv é uma ferramenta que cria ambientes virtuais Python para execução de aplicações de forma isolada e simplificada.


## Executando um exemplo

1. Certifique-se de que [pipenv está instalado](https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv)
1. A partir da pasta sample/, execute `python -m pipenv install` para criar um ambiente Python com as dependências descritas no [Pipfile](./Pipfile) já instaladas
1. A partir da pasta sample/, execute `python -m pipenv shell` para iniciar um terminal no contexto do ambiente Python criado no passo anterior
1. A partir da pasta sample/ e dentro do shell acessado no passo anterior, [execute o módulo](https://docs.python.org/3/using/cmdline.html#cmdoption-m) `tkinter_sample` através do comando `python -m tkinter_sample`




