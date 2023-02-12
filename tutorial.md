# Tutorial

A forma primária de utilizar py_netgames se dá através de um artefato Python reutilizável chamado py-netgames-client. Disponibilizado via pip, existem diversas formas de obtê-lo, porém é recomendado que seja feito através de um ambiente Python virtual.

* Um esqueleto de projeto configurado para baixar o py-netgames-client via ambiente virtual Python, com instruções de uso, pode ser encontrado em [py_netgames_template](https://github.com/gabrielroza/py_netgames_template)
* Exemplos de jogos implementado com py-netgames-client, com instruções de execução, podem ser encontrados neste [link](https://github.com/gabrielroza/py_netgames/tree/main/sample)
    
    * Atenção para a biblioteca gráfica utilizada, são disponibilizados os códigos fonte de implementações com [tkinter](https://github.com/gabrielroza/py_netgames/tree/main/sample/tkinter_sample) e [pygame](https://github.com/gabrielroza/py_netgames/tree/main/sample/pygame_sample)


## Casos de uso


## Estrutura de classes

A estrutura básica de classes de py-netgames-client é a seguinte:

![screenshot](/imgs/py_netgames_client_public_classes.jpg)

Com py-netgames-client, a comunicação entre diferentes instâncias de um jogo é realizada através de duas classes:
1. `PyNetgamesServerProxy`: Utilizada para iniciar e finalizar conexões, solicitar partidas e enviar jogadas. Métodos:
    -  `add_listener(listener: PyNetgamesServerListener)`: Adiciona uma implementação de `PyNetgamesServerListener` aos listeners da instância de `PyNetgamesServerProxy`. Listeners são notificados do recebimento de partidas e jogadas, além de confirmações dos métodos seguintes.
    -  `send_connect()`: Solicita uma conexão. A conexão é confirmada através do método `receive_connection_success` dos listeners registrados.
        * :warning: Caso o método `send_connect()` seja chamado sem nenhum argumento, será possível conectar apenas com outras instâncias locais do jogo. Para conectar com outras máquinas, utilize um servidor remoto, como por exemplo: `send_connect(address="wss://py-netgames-server.fly.dev")`  	      
    -  `send_match(amount_of_players: int)`: Solicita uma partida para a quantidade de jogadores informados. A solicitação é confirmada através do método `receive_match` dos listeners registrados.
        * Um jogo é identificado por um [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) gerado pelo py-netgames durante a instanciação de `PyNetgamesServerProxy`, em um arquivo chamado gameid.txt. **Diferentes instâncias de um mesmo jogo devem usar o mesmo id para se conectarem**. Caso diferentes instâncias estejam conectadas e solicitando partida, porém a mesma não é iniciada, certifique-se através dos logs que ambas as instâncias estão com o mesmo id. Exemplo de logs:
                `INFO:py_netgames_client:Found game_id at /tkinter_sample/gameid.txt with value 9e6daf0b-69a1-4524-9ac0-6fd140865425`  
                `INFO:py_netgames_client:Game identified by game_id: 9e6daf0b-69a1-4524-9ac0-6fd140865425. Different instances of the same game must use the same game_id id in order to have matches.`
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