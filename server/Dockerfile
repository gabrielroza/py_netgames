FROM python:3.8-alpine

RUN pip3 install py-netgames-server

EXPOSE 8765

CMD ["python3", "-m", "py_netgames_server", "--debug", "--host", "0.0.0.0"]