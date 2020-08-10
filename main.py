import pandas as  pd
import matplotlib

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv', header=0)
print(df[df['Date'].contains('02-29')])

print(min(df['Date']))

