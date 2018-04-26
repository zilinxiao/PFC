import numpy as np
import pandas as pd
def f1():
    s1 = pd.Series(np.linspace(0,10,6))
    s1.to_csv("s1.csv")
    df1 = pd.DataFrame([pd.Series(np.linspace(e,5+e,6))  for e in np.arange(10)])
    df1.to_csv('df1.csv')
    with  pd.HDFStore("hf.hdf5",complib="blosc",complevel=9) as hf:
        hf['series/s1'] = s1
        hf['dataframes/df2'] = df1
    print
def f2():
    print(pd.read_csv('s1.csv'))
    df = pd.read_csv('df1.csv')
    print(df)
    print(df.head(4))
    print(df[1:3])
    with pd.HDFStore("hf.hdf5",complib='blosc',complevel=9) as hf:
        df1 = hf['dataframes/df1']
        print(df1.tail(4))
        print(np.sin(df1))
f1()
f2()