from sqlalchemy.sql import text
import sqlalchemy
import pandas as pd

import os, sys
# Add parent directory to path to import modules from outside the current directory
rpath = os.path.abspath(os.path.join(os.getcwd(), '..'))
if rpath not in sys.path:
    sys.path.append(rpath)

from db_utils import DBUtils

class DeviceTypeChartSchema:
    def __init__(self):
        self.engine = DBUtils().connectDB()
        self.table_name = 'device_type_chart'

    def load_to_db(self, df: pd.DataFrame):
        sql_query = f"""
        CREATE SCHEMA IF NOT EXISTS youtube;
        DROP TABLE IF EXISTS youtube.{self.table_name};
        CREATE TABLE youtube.{self.table_name}(
            id integer,
            name varchar,
            date DATE,
            views integer
        );
        """
        with self.engine.connect() as conn:
            conn.execute(text(sql_query))
    
        df.to_sql(self.table_name, self.engine, schema='youtube', if_exists='replace', index=False, dtype={
                         'id': sqlalchemy.types.Integer,
                         'name': sqlalchemy.types.VARCHAR,
                         'date': sqlalchemy.types.DATE,
                         'views': sqlalchemy.types.Integer,
                        })

    """Load data from the PostgreSQL database."""
    def read_from_db(self):
        df = pd.read_sql_table(self.table_name, self.engine, schema='youtube')
        return df
