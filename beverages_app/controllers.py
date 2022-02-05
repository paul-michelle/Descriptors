import logging
from settings import (
    LOGS_LEVEL,
    LOGS_FILENAME,
    BASE_ENCODING,
    DB_CONNECTION
)

logging.basicConfig(
    filename=LOGS_FILENAME,
    encoding=BASE_ENCODING,
    level=LOGS_LEVEL
)


def log_signal_handshake():
    logging.info('Signal received')


if __name__ == '__main__':
    from models import SoftDrink
    from framework.tools.dispatcher import pre_init

    pre_init.connect(log_signal_handshake, SoftDrink)


    def generate_drinks(model):
        while True:
            yield model()


    drinks = []
    for drink in generate_drinks(SoftDrink):
        if len(drinks) == 10:
            break
        drink.producer = 'Producer'
        drink.trademark = 'Trademark'
        drinks.append(drink)

    results = DB_CONNECTION.execute(
        'SELECT * FROM softdrinks_table;'
    ).fetchall()
    print(results)
