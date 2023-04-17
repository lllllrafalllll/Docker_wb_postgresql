import psycopg2
from main import query, values
import pandas as pd
from decouple import config

#Подлючение к базе
conn_src = psycopg2.connect(database = "app_db",
host = "212.23.221.222",
user = "admin",
password = config('password'),
port = "5432")
conn_src.autocommit = False

cursor_src = conn_src.cursor()


#Получаем максимальную дату из meta
def max_meta(table_stg, table_schema):
    cursor_src.execute( f""" select max_update_dt from {table_schema}.meta
      where schema_name='{table_schema}' and table_name = '{table_stg}' """)
    last_terminals_date = cursor_src.fetchone()[0]
    print('Получаем максимальную дату из meta')
    return last_terminals_date







def main():
   df = pd.read_csv('cost_price.csv', sep=';', encoding="windows-1251")

   cursor_src.executemany(f""" INSERT INTO wb_1166200.stg_costprice(
                                  {query(df)}
                              ) VALUES( {values(df)} ) """, df.values.tolist() )
   conn_src.commit()
   cursor_src.close()
   conn_src.close()

if __name__ == '__main__':
    main()