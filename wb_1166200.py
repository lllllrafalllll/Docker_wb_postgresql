import main
from decouple import config

schema = 'wb_1166200'

APP_TOKEN_1166200 = config('APP_TOKEN_1166200')


if __name__ == '__main__':
    main.main(APP_TOKEN_1166200, schema)