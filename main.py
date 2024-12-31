from app.logging.hen_logger import init_logger
from app.server import server

init_logger()


def start_server():
    server()


if __name__ == '__main__':
    print("Dog alarm")
    start_server()
