import pandas as pd 
import numpy as np

xls = pd.ExcelFile(r"C:\Users\manue\Desktop\Mestrado\2º Semestre\1º Term\Hedge Funds\9E467100.xlsx")
data = pd.read_excel(xls,"Sheet1")
data.set_index(data['Date'], drop = True, inplace = True)
data.drop(columns = 'Date', inplace = True)

index = data.iloc(axis = 1)[:3]
bonds = data.iloc(axis = 1)[3:6]
commodities = data.iloc(axis = 1)[6:9]

#volatility of 20% as threshold 

info_sr_index = {}
for security in index:
    day = 0
    info_sr_index[security] = {}
    while day <= 120:
        ma = pd.DataFrame()
        ma['ma'] = data[security].rolling(day).mean()
        ma['std'] = data[security].rolling(day).std()
        ma.dropna(inplace = True)
        index.iloc(axis = 0, inplace = True)[day:]
        ma['signal']=[]
        for i in ma.interrows():
            if ma.loc["std":i]*(260**0.5)<0.20:
                if ma.loc['ma':i]>index.loc[security:i+day]:
                    ma.loc["signal":i]=0
                else:
                    ma.loc["signal":i]=1
            else:
                if ma.loc["ma":i]+ma.loc["std":i]>index.loc[security:i+day]:
                    ma.loc["signal":i]=-1
                else:
                    ma.loc["signal":i]=1         
        ma['returns'] = index[security].pct_change().dropna()
        ma['log_returns'] = np.log(1+index[security].pct_change()).dropna()
        ma['strategy returns'] = ma['returns'] * ma['signal']
        avg = ma['strategy returns'].mean()
        std = ma['strategy returns'].std()
        sr = avg / std
        info_sr_index[security][day] = sr
        day += 10
