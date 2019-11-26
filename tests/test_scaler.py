import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

#scaler = StandardScaler()
scaler = MinMaxScaler(feature_range=(0.1, 1))

asks_df = pd.DataFrame()
bids_df = pd.DataFrame()

asks_df['vol'] = ['181.71', '225.90', '812.78', '15.30']
bids_df['vol'] = ['45.83', '18.53', '22.45', '19.88']

asks_df['vol_scaled'] = scaler.fit_transform(asks_df['vol'].values.reshape(-1, 1))
bids_df['vol_scaled'] = scaler.fit_transform(bids_df['vol'].values.reshape(-1, 1))

asks_df = asks_df.rename(columns={"vol": "cex_vol"})
bids_df = bids_df.rename(columns={"vol": "cex_vol"})

print(asks_df)
print(bids_df)

print(f'scaler fit: {scaler.fit(asks_df)}')
print(f'scaler transform: {scaler.transform(asks_df)}')

# https://stackoverflow.com/questions/51841506/data-standardization-vs-normalization-vs-robust-scaler