from DHMZparser.parser import DHMZ_buoy_data
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

datafiles = Path("/home/domagoj/Documents/dev/vrgada_cres/data/dhmz/TTN1MLM").glob('*.mlm')

ts = []

for datafile in tqdm(datafiles):
    print(datafile)
    data = DHMZ_buoy_data(datafile)
    if data.depth == "-0.8 m" or data.depth == "-0.80 m" and data.origin == "60 min":
        print(data.station, data.month, data.year, data.depth, data.origin)
        ts.append(data.timeseries)

if ts != []:
    timeseries = pd.concat(ts).sort_index()


    plt.plot(timeseries[:])

    timeseries.to_csv(
        f"m_losinj_{data.origin.replace(' ', '_')}_{data.depth}.csv")
