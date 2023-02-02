import pandas as pd 
import numpy as np

xls = pd.ExcelFile(r"C:\Users\João Saraiva\Google Drive\MSc in Finance\S2\3. Hedge Funds\Assignment 1\9E467100.xlsx")
data = pd.read_excel(xls,"Sheet1")
data.set_index(data['Date'], drop = True, inplace = True)
data.drop(columns = 'Date', inplace = True)

index = data.iloc(axis = 1)[:3]
bonds = data.iloc(axis = 1)[3:6]
commodities = data.iloc(axis = 1)[6:9]

info_sr_index = {}
index.iloc(axis = 0)[5:]
for security in index:
    day = 1
    info_sr_index[security] = {}
    while day <= 120:
        ma = pd.DataFrame()
        ma['ma'] = data[security].rolling(day).mean()
        ma.dropna(inplace = True)
        index.iloc(axis = 0, inplace = True)[day:]
        ma['signal'] = np.where(index[security] > ma['ma'], 1, -1)
        ma['returns'] = index[security].pct_change().dropna()
        ma['strategy returns'] = ma['returns'] * ma['signal']
        avg = ma['strategy returns'].mean()
        std = ma['strategy returns'].std()
        sr = avg / std
        info_sr_index[security][day] = sr
        day += 1
 

    
ma.set_index(data.index, drop = False, inplace = True)
ma.dropna(inplace = True)

signals = pd.DataFrame()



eth['21-day'] = eth['Close'].rolling(21).mean() 
eth['signal'] = np.where(eth['9-day'] > eth['21-day'], 1, 0)
eth['signal'] = np.where(eth['9-day'] < eth['21-day'], -1, eth['signal'])
eth['eth return'] = eth['Adj Close'].pct_change().dropna()
eth['system return'] = eth['signal'] * eth['eth return']
eth['entry'] = eth.signal.diff()
eth['entry'][0] = 1

