import requests
import json
import datetime
from datetime import datetime
import pandas as pd
import psycopg2
import scd
from decouple import config


reports = ['orders', 'stocks', 'sales', 'incomes']


fact_tables = [scd.orders_fact, scd.stocks_fact, scd.sales_fact, scd.fact_incomes]


date_now = datetime.now().strftime('%Y-%m-%d')


#Подлючение к базе
conn_src = psycopg2.connect(database = "app_db",
host = "212.23.221.222",
user = "admin",
password = config('password'),
port = "5432")
conn_src.autocommit = False

cursor_src = conn_src.cursor()



def query(data):
    cols = list(data.columns)
    return ' ,'.join(cols)

def values(data):
    cols = list(data.columns)
    return ' ,'.join(['%s' for _ in range(len(cols))])

def comm():
    conn_src.commit()



def delete(name, table_schema):
    print(f"Таблица {name} очищена")
    cursor_src.execute(f"""delete from  {table_schema}.stg_{name}""")



def tgt_table(df, name, schema='wb_ID33732'):
    print(f"Таблица {name} загружена в stg")
    cursor_src.executemany(f""" INSERT INTO {schema}.stg_{name}(
                                      {query(df)}
                                  ) VALUES( {values(df)} ) """, df.values.tolist())
    comm()



def data_acquisition(request_type, key, dateFrom, flag=0):
  header = {'Authorization': key}
  params = {'dateFrom': dateFrom,
            'flag': flag}
  post = f'https://statistics-api.wildberries.ru/api/v1/supplier/{request_type}'
  resp = requests.get(post, headers=header, params=params)
  wb = json.loads(resp.text)
  df = pd.DataFrame(wb)
  return df



def fact_week(schema):
    print('start fact_week')
    cursor_src.execute(scd.fact_report_week(schema))
    comm()
    print('end fact_week')


def fact(table):
    print("Загрузка fact таблиц")
    cursor_src.execute(table)
    comm()
    print("Fact таблицы загруженый")





def main(APP_TOKEN, schema):
    print("Cron job has run at %s" % datetime.now())
    for report, fact_table in zip(reports, fact_tables):
        delete(report, schema)
        df=data_acquisition(report, APP_TOKEN, date_now, flag=0)
        tgt_table(df, report, schema)
        fact(fact_table(schema))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(APP_TOKEN=0, schema=0)
    conn_src.commit()
    cursor_src.close()
    conn_src.close()

