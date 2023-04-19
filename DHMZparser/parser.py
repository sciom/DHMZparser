import numpy as np

import pandas as pd
from pprint import pprint

class DHMZ_buoy_data():
    def __init__(self, datafile):
        self.datafile = datafile
        self.station = ""
        self.description = ""
        self.month = ""
        self.year = ""
        self.depth = ""
        self.origin = ""
        self.original = None
        self.dataframe = None
        self.timeseries = None
        self.read_data()

        self.to_timeseries()

    def read_data(self):
        with open(self.datafile, 'r') as f:
            data = f.readlines()
        
        # parsing metadata

        for i in data:
            if "POSTAJA" in i:
                self.station = i.split("POSTAJA")[1].strip()
            if "MJESEC" in i:
                self.month = i.split("MJESEC")[1].strip().split(" ")[0]
            if "GODINA" in i:
                self.year = i.split("GODINA")[1].strip()
            if "NIVO:" in i:
                self.depth = i.split("NIVO:")[1].strip()
        
        months = {
            "SIJECANJ": 31,
            "VELJACA": 29, # prijestupni
            "OZUJAK": 31,
            "TRAVANJ": 30,
            "SVIBANJ": 31,
            "LIPANJ": 30,
            "SRPANJ": 31,
            "KOLOVOZ": 31,
            "RUJAN": 30,
            "LISTOPAD": 31,
            "STUDENI": 30,
            "PROSINAC": 31
        }

        table = []

        days = range(1, months[self.month]+1)
        rows = {}
        for i in days:
            rows[f"{i}"] = ""

        for row in data:
            for i in days:
                i_str = str(i)
                if len(i_str) == 1:
                    i_str = f"|  {i} | "
                else:
                    i_str = f"| {i} | "
                if i_str in row:
                    # print(row.strip())
                    rows[f"{i}"] += row.strip()[6:]
                    rows[f"{i}"]  = rows[f"{i}"].replace("||", "|")
                    # rows[f"{i}"]  = rows[f"{i}"][:-1]

        # print(rows["1"])
        # numerize data

        for i in rows:
            rows[i] = rows[i].split("|") 

            p = []
            for v in rows[i]:
                try:
                    p.append(float(v))
                except:
                    p.append(np.nan)
            
            p.pop(-1)


            rows[i] = p
        
        # for i in rows:
        #     # print(len(rows[i]))
        #     if len(rows[i]) > months[self.month]+1:
        #         print(i)
        #         print(rows[i])
        # create dataframe

        df = pd.DataFrame(rows)
        df = df.T

        df = df.rename(columns={
            0: "1",
            1: "2",
            2: "3",
            3: "4",
            4: "5",
            5: "6",
            6: "7",
            7: "8",
            8: "9",
            9: "10",
            10: "11",
            11: "12",
            12: "13",
            13: "14",
            14: "15",
            15: "16",
            16: "17",
            17: "18",
            18: "19",
            19: "20",
            20: "21",
            21: "22",
            22: "23",
            23: "24",
            24: "mean", # Srednjak
            25: "std", # Standardna devijacija
            26: "max 1", # Maksimum
            27: "min 1", # Minimum
            28: "max 2", # Maksimum izvornih podataka
            29: "t max", # Vrijeme maksimuma
            30: "min 2", # Minimum izvornih podataka
            31: "t min", # Vrijeme minimuma
            32: "none nbr", # Broj nepostojećih podataka
        })

            
        self.dataframe = df

        self.original = data

    def to_timeseries(self):
        months = {
            "SIJECANJ": "1",
            "VELJACA": "2",
            "OZUJAK": "3",
            "TRAVANJ": "4",
            "SVIBANJ": "5",
            "LIPANJ": "6",
            "SRPANJ": "7",
            "KOLOVOZ": "8",
            "RUJAN": "9",
            "LISTOPAD": "10",
            "STUDENI": "11",
            "PROSINAC": "12"
        }
        self.timeseries = self.dataframe.drop(columns=["mean", "std", "max 1", "min 1", "max 2", "t max", "min 2", "t min", "none nbr"])
        self.timeseries = self.timeseries.stack(dropna=False)
        self.timeseries = self.timeseries.reset_index()
        self.timeseries = self.timeseries.rename(columns={
            "level_0": "day",
            "level_1": "hour",
            0: "temperature"
        })
        self.timeseries["day"] = self.timeseries["day"].astype(int)
        self.timeseries["hour"] = self.timeseries["hour"].astype(int)-1
        self.timeseries["temperature"] = self.timeseries["temperature"].astype(float)
        self.timeseries["date"] = pd.to_datetime(self.timeseries["day"].astype(str) + "-" + months[self.month] + "-" + self.year + " " + self.timeseries["hour"].astype(str) + ":00:00")
        self.timeseries = self.timeseries.set_index("date")
        self.timeseries = self.timeseries.drop(columns=["day", "hour"])
        self.timeseries = self.timeseries.sort_index()
    
    def to_csv(self, filename):
        self.timeseries.to_csv(filename)
        
    def to_json(self, filename):
        self.timeseries.to_json(filename)
    
    def to_xml(self, filename):
        self.timeseries.to_xml(filename)

    