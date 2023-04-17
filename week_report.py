import requests
import json
import datetime
from datetime import datetime
import pandas as pd
import psycopg2
import scd
import main



def sales_report_by_implementation(key, dateFrom, dateTo, limit=0,  rrdid=0):
  header = {'Authorization': key}
  params = {'dateFrom': dateFrom,
            'dateTo': dateTo,
            'limit': limit,
            'rrdid': rrdid}
  post = f'https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod'
  resp = requests.get(post, headers=header, params=params)
  wb = json.loads(resp.text)
  df = pd.DataFrame(wb)
  return df


def main_report(APP_TOKEN, schema):
  main.delete('reportDetailByPeriod', schema)
  df = pd.DataFrame()
  rrdid = 0
  while True:
    print("Запуск")
    df1 = sales_report_by_implementation(APP_TOKEN, '2023-03-01', '2023-04-04', 100000, rrdid)
    df = pd.concat([df, df1])
    if df1.shape[0] < 100000:
      break
    rrdid = df['rrd_id'].max()
  main.tgt_table(df, 'reportDetailByPeriod', schema)


if __name__ == '__main__':
  main_report(APP_TOKEN=0, schema=0)