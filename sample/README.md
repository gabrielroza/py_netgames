# Exemplo de uso

Para executar um exemplo de uso é necessário ter [instalado o pipenv](https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv). Pipenv é uma ferramenta que cria ambientes virtuais Python para execução de aplicações de forma isolada e simplificada.


## Executando um exemplo

1. Certifique-se de que [pipenv está instalado](https://pipenv.pypa.io/en/latest/install/#pragmatic-installation-of-pipenv):  
![screenshot](./img/pipenv%20installation.gif)
1. A partir da pasta sample/, execute `python -m pipenv install` para criar um ambiente Python com as dependências descritas no [Pipfile](./Pipfile) já instaladas:  
![screenshot](./img/pipfile%20installation.gif)
1. A partir da pasta sample/, execute `python -m pipenv shell` para iniciar um terminal no contexto do interpretador Python criado no passo anterior. Então, execute `python -m tkinter_sample` para rodar o exemplo:  
![screenshot](./img/run%20sample.gif)
1. Repita o passo anterior em outro terminal para executar duas instâncias do jogo, que então poderão conectar-se uma a outra:  
![screenshot](./img/match.gif)

## Modelagem 

![screenshot](./img/py_netgames_sample%20tkinter_sample.jpg)

Com a biblioteca py-netgames-client, a comunicação entre diferentes instâncias de um jogo é realizada através de duas classes:
1. `PyNetgamesServerProxy`: Utilizada para iniciar e finalizar conexões, solicitar partidas e enviar jogadas. Métodos:
    -  `add_listener(listener: PyNetgamesServerListener)`: Adiciona uma implementação de `PyNetgamesServerListener` aos listeners da instância de `PyNetgamesServerProxy`. Listeners são notificados do recebimento de partidas e jogadas, além de confirmações dos métodos seguintes.
    -  `send_connect()`: Solicita uma conexão. A conexão é confirmada através do método `receive_connection_success` dos listeners registrados.
    -  `send_match(amount_of_players: int)`: Solicita uma partida para a quantidade de jogadores informados. A solicitação é confirmada através do método `receive_connection_success` dos listeners registrados.
    -  `send_move(match_id: UUID, payload: Dict[str, any])`: Envia uma jogada.`match_id` deve ser o identificador da partida recebida pelo listener através do método `receive_match`. `payload` é um dicionário que contém os dados do jogo em questão. Neste exemplo, `payload` contém as informações do tabuleiro de jogo da velha. É importante notar que este dicionário deve conter chaves do tipo `str` e valores de tipos cuja qual serialização é possível: `dict`, `list`, `tuple`, `str`, `int`, `float`, `bool` e `None`.
    -  `send_disconnect()`: Solicita desconexão.
2. `PyNetgamesServerListener`: Classe abstrata que deve ser implementada e adicionada a um `PyNetgamesServerProxy` através do método `add_listener`. Em suma, é responsável pelo recebimento de partidas, jogadas e confirmações de ações assíncronas. Métodos:
    - `receive_connection_success()`: Método chamado quando uma conexão solicitada através do método `send_connect` é confirmada.
    - `receive_match(match: MatchStartedMessage)`: Método chamado quando uma partida é confirmada, após solicitação via `send_match`. O parâmetro recebido é um objeto que contém os campos `match_id`, o identificador da partida, e `position`, um inteiro que indica a vez do jogador.
    - `receive_move(message: MoveMessage)`: Método chamado quando uma jogada é recebida, após uma partida estar em vigor (recebida via `receive_match`). O parâmetro recebido é um objeto que contém os campos `match_id`, o identificador da partida, e `position`, um inteiro que indica a vez do jogador.
    - `receive_error(error: Exception)`: Método chamado na eventualidade de um erro ocorrer na biblioteca. O tratamento recomendado é resetar o jogo para seu estado inicial.
    - `receive_disconnect`: Método chamado quando ocorre uma desconexão. O tratamento recomendado é resetar o jogo para seu estado inicial.
    - `receive_match_requested_success`: Método de sobrescrita opcional, chamado quando uma solicitação de partida realizada via `send_match` é confirmada.
    - `receive_move_sent_success`: Método de sobrescrita opcional, chamado quando um envio de jogada realizada via `send_move` é confirmado.

## Uso com IDEs

Para que IDEs visualizem corretamente a instalação de dependências realizadas dentro de um ambiente Pipenv, é necessário apontar para o interpretador correto, aquele criado pelo pipenv `pipenv install`.

-  No caso do VSCode isso pode ser feito, após a instalação do plugin de Python, através do fluxo [Select Interpreter](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment)
- No caso do PyCharm, através do [Setting an existing Python interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#add-existing-interpreter)

