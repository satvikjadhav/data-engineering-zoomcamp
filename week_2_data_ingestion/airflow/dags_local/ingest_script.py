import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def ingest_callable(user, password, host, port, db, table_name, csv_name):
    # user = user
    # password = password
    # host = host 
    # port = port 
    # db = db
    # table_name = table_name
    # csv_name = 'output.csv'

    print(table_name, csv_name)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    print("connection established")

    # df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # df = next(df_iter)

    df = pd.read_csv(csv_name)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')


    # while True: 
    #     t_start = time()

    #     try:
    #         df = next(df_iter)
    #     except StopIteration:
    #         print("completed")
    #         break

    #     df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    #     df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    #     df.to_sql(name=table_name, con=engine, if_exists='append')

    #     t_end = time()

    #     print('inserted another chunk, took %.3f second' % (t_end - t_start))
