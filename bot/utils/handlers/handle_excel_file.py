import os

import pandas as pd
import sqlite3

import settings


def excel_to_sqlite():
    db = sqlite3.connect(settings.REPLACEMENTS_DATA_BASE_PATH)
    dfs = pd.read_excel(os.path.abspath('replacements.xlsx'), sheet_name=None)
    for table, df in dfs.items():
        df.to_sql(table, db, if_exists='replace')
