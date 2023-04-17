import week_report
import main
from decouple import config

schema = 'wb_1166200'

APP_TOKEN_1166200 = config('APP_TOKEN_1166200')


if __name__ == '__main__':
    week_report.main_report(APP_TOKEN_1166200, schema)
    main.fact_week(schema)
