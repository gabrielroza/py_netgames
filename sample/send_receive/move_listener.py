from client.cliente.listener import Listener


class MoveListener(Listener):

    def receive_move(self, payload: any):
        print(payload)
