import sys
import pandas as pd


month = int(sys.argv[1])


if month in range(1, 12):
    print(f"Month is {month}")
else:
    print("Incorrect month, should be from 1 to 12")


df = pd.DataFrame({'Day':  [1,2], 'Passengers': [3,4]})
df['month'] = month

print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet ")


