# DEPRECATED

import pandas as pd
import os

CSV_PATH = "{}.csv"
rdir = "../raw_data"

for filename in os.listdir(rdir):
    file = os.path.join(rdir, filename)
    if os.path.isfile(file) and file.endswith("xlsx") and not file.startswith("~"):
        print(file)
        read_file = pd.read_excel(file, engine='openpyxl')
        print(CSV_PATH.format(os.path.splitext(file)[0]))
        read_file.to_csv(CSV_PATH.format(os.path.splitext(file)[0]), index=None, header=True)