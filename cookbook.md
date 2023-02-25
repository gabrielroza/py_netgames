# Framework Cookbook

Um cookbook de framework é um conjunto de instruções, guias e exemplos que fornecem aos desenvolvedores um roteiro passo a passo para usar um framework específico, neste caso o py-netgames.

## Obtenção do framework

A forma primária de utilizar py-netgames se dá através de um artefato Python reutilizável chamado py-netgames-client. Disponibilizado via pip, existem diversas formas de obtê-lo, porém é recomendado que seja feito através de um ambiente Python virtual.

* Um esqueleto de projeto configurado para baixar o py-netgames-client via ambiente virtual Python, com instruções de uso, pode ser encontrado em [py_netgames_template](https://github.com/gabrielroza/py_netgames_template)


## Estrutura de classes

![screenshot](/imgs/py_netgames_client_public_classes.jpg)

Visando a simplificação da criação de jogos distribuídos, py-netgames-client expõe duas classes reutilizáveis que abstraem algumas das dificuldades inerentes a criação de softwares de distribuídos. Estas classes são:  

1. `PyNetgamesServerProxy`: Utilizada para iniciar e finalizar conexões, solicitar partidas e enviar jogadas. Representa o componente remoto do framework.  
 Métodos:
    -  `add_listener(listener: PyNetgamesServerListener)`: Adiciona uma implementação de `PyNetgamesServerListener` aos listeners da instância de `PyNetgamesServerProxy`. Listeners são notificados do recebimento de partidas e jogadas, além de confirmações dos métodos seguintes.
    -  `send_connect()`: Solicita uma conexão. A conexão é confirmada através do método `receive_connection_success` dos listeners registrados.
        * **Atenção**: Caso o método `send_connect()` seja chamado sem nenhum argumento, será possível conectar apenas com outras instâncias locais do jogo. Para conectar com outras máquinas, utilize um servidor remoto, como por exemplo: `send_connect(address="wss://py-netgames-server.fly.dev")`  	      
    -  `send_match(amount_of_players: int)`: Solicita uma partida para a quantidade de jogadores informados. A solicitação é confirmada através do método `receive_match` dos listeners registrados.
        * **Atenção**: Um jogo é identificado por um [UUID][UUID] gerado pelo py-netgames durante a instanciação de `PyNetgamesServerProxy`, em um arquivo chamado gameid.txt. **Diferentes instâncias de um mesmo jogo devem usar o mesmo id para se conectarem**. Caso diferentes instâncias estejam conectadas e solicitando partida, porém a mesma não é iniciada, certifique-se através dos logs que ambas as instâncias estão com o mesmo id. Exemplo de logs:
                `INFO:py_netgames_client:Found game_id at /tkinter_sample/gameid.txt with value 9e6daf0b-69a1-4524-9ac0-6fd140865425`  
                `INFO:py_netgames_client:Game identified by game_id: 9e6daf0b-69a1-4524-9ac0-6fd140865425. Different instances of the same game must use the same game_id id in order to have matches.`
    -  `send_move(match_id: UUID, payload: Dict[str, any])`: Envia uma jogada.`match_id` deve ser o identificador da partida recebida pelo listener através do método `receive_match`. `payload` é um dicionário que contém os dados do jogo em questão. Neste exemplo, `payload` contém as informações do tabuleiro de jogo da velha. É importante notar que este dicionário deve conter chaves do tipo `str` e valores de [tipos cuja qual serialização é possível](https://docs.python.org/3/library/json.html#json.JSONDecoder) : `dict`, `list`, `tuple`, `str`, `int`, `float`, `bool` e `None`.
    -  `send_disconnect()`: Solicita desconexão.
2. `PyNetgamesServerListener`: Classe abstrata que deve ser implementada e adicionada a um `PyNetgamesServerProxy` através do método `add_listener`. Em suma, é responsável pelo recebimento de partidas, jogadas e confirmações de ações. Métodos:
    - `receive_connection_success()`: Método chamado quando uma conexão solicitada através do método `send_connect` é confirmada.
    - `receive_match(match: MatchStartedMessage)`: Método chamado quando uma partida é confirmada, após solicitação via `send_match`. O parâmetro recebido é um objeto que contém os campos `match_id`, o identificador da partida, e `position`, um inteiro que indica a vez do jogador.
    - `receive_move(message: MoveMessage)`: Método chamado quando uma jogada é recebida, após uma partida estar em vigor (recebida via `receive_match`). O parâmetro recebido é um objeto que contém os campos `match_id`, o identificador da partida, e `position`, um inteiro que indica a vez do jogador.
    - `receive_error(error: Exception)`: Método chamado na eventualidade de um erro ocorrer na biblioteca. O tratamento recomendado é resetar o jogo para seu estado inicial.
    - `receive_disconnect`: Método chamado quando ocorre uma desconexão. O tratamento recomendado é resetar o jogo para seu estado inicial.
    - `receive_match_requested_success`: Método de sobrescrita opcional, chamado quando uma solicitação de partida realizada via `send_match` é confirmada.
    - `receive_move_sent_success`: Método de sobrescrita opcional, chamado quando um envio de jogada realizada via `send_move` é confirmado.

## Casos de uso

![screenshot](/imgs/py_netgames_use_cases.jpg)

### Add Listener

Iniciativa: Local

Trata do registro de uma subclasse de `PyNetgamesServerListener` no componente remoto do framework, uma instância de `PyNetgamesServerProxy`. É comum que esta subclasse de `PyNetgamesServerListener` seja também a classe que implementa a interface gráfica do jogo, dessa forma permitindo a atualização visual quando por exemplo uma jogada remota é recebida.

### Send Connect

Iniciativa: Local

Trata da conexão com o componente remoto (o servidor) do framework. Diferentes execuções de um mesmo jogo precisam estar conectadas no mesmo servidor para que seja possível a disputa de partidas. Dessa forma, é preciso atentar-se ao endereço de servidor que será informado a `PyNetgamesServerProxy`. Caso nenhum endereço seja informado, será possível a comunicação somente na mesma máquina. 

### Send Match

Iniciativa: Local

Trata da solicitação de uma partida para a quantidade de jogadores informada. Importante notar que cada jogo possui um identificador gerado pelo framework, em um arquivo gameid.txt. Diferentes execuções do mesmo jogo precisam ter o mesmo gameid.txt para que ocorra a conexão de partidas. Caso a execução daUma vez que o componente remoto do framework identifica que existem jogadores suficientes dada a quantidade solicitada, uma partida será iniciada (caso de uso Receive Match).

### Send Move

Iniciativa: Local

Trata do envio de um movimento para o componente remoto do framework. Importante destacar que o framework não realiza controle de "vez" dos jogadores, ficando isso a cargo da implementação do jogo com base na posição recebida no caso de uso Receive Match. Ao enviar o movimento, é necessário informar o id da partida, recebido no caso de uso Receive Match. O movimento enviado deve ser um dicionário composto por tipos serializáveis.

### Send Disconnect

Iniciativa: Local

Trata da solicitação de desconexão com o componente remoto do framework. Caso não haja conexão em vigor, nada ocorre. Caso partida em andamento, os demais jogadores também serão desconectados.

### Receive Connection

Iniciativa: Framework

Trata da confirmação de sucesso de uma conexão solicitada no caso de uso Send Connect. 

### Receive Match

Iniciativa: Framework

Trata do recebimento de uma partida, conforme solicitada no caso de uso Request Match. A mensagem recebida possui o identificador da partida (que deve ser utilizado para enviar movimentos no caso de uso Send Move) e a posição do jogador, que pode ser usada para controlar a vez do jogador.

### Receive Move

Iniciativa: Framework

Trata do recebimento de uma jogada, A mensagem recebida possui o identificador da partida (que deve ser utilizado para enviar movimentos no caso de uso Send Move) e a posição do jogador, que pode ser usada para controlar a vez do jogador.


### Receive Error

Iniciativa: Framework

Trata do recebimento de eventuais erros que ocorram no framework. O tratamento recomendado é resetar o jogo para um estado inicial.


### Receive Disconnect

Iniciativa: Framework

Trata do recebimento de uma desconexão, seja ela solicitada (caso de uso Send Disconnect) ou recebida por desconexão de outros jogadores. O tratamento recomendado é resetar o jogo para um estado inicial.

[UUID]: https://en.wikipedia.org/wiki/Universally_unique_identifier