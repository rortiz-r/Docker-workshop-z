import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Read env variables

config = load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PSS = os.getenv('DB_PSS')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')


print(DB_USER, DB_PSS, DB_PORT, DB_NAME, DB_HOST)

# Database url creation
database_url = f'postgresql+psycopg://{DB_USER}:{DB_PSS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = prefix + 'yellow_tripdata_2021-01.csv.gz'


def get_process_csv():
    
    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64"
    }

    parse_dates = [
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime"
    ]

    taxi_data_chunks = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000
    )

    return taxi_data_chunks



def insert_data(engine, chunks):

    # Loading data in chuncks
    total = 0
    for (i, chunk) in enumerate(chunks):
        # Create table
        if i == 0:
            chunk.head(0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


        # Insert chunk
        chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

        total+= len(chunk)
        print(f'Inserted chunk {i} with a size of {len(chunk)}  data inserted till this moment: {total}')

    print(f'Inserted data {total}')
    


def run():
    
    engine = create_engine(database_url)

    chunks = get_process_csv()
    
    insert_data(engine, chunks)



if __name__ == '__main__':

    run()
