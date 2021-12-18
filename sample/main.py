from client.cliente.proxy import Proxy

from send_receive.move_listener import MoveListener

if __name__ == '__main__':
    listeners = [MoveListener()]
    Proxy(listeners)