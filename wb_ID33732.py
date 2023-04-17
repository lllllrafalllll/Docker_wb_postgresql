import main
from decouple import config

schema = 'wb_ID33732'

APP_TOKEN_ID33732 = config('APP_TOKEN_ID33732')


if __name__ == '__main__':
    main.main(APP_TOKEN_ID33732, schema)