from sqlalchemy.sql import text
import sqlalchemy
import pandas as pd

import os, sys
# Add parent directory to path to import modules from outside the current directory
rpath = os.path.abspath(os.path.join(os.getcwd(), '..'))
if rpath not in sys.path:
    sys.path.append(rpath)

from db_utils import DBUtils

class CitiesAggregateSchema:
    def __init__(self):
        self.engine = DBUtils().connectDB()
        self.table_name = 'cities_aggregate'

    def load_to_db(self, df: pd.DataFrame):
        sql_query = f"""
        CREATE SCHEMA IF NOT EXISTS youtube;
        DROP TABLE IF EXISTS youtube.{self.table_name};
        CREATE TABLE youtube.{self.table_name}(
            id integer,
            city_name varchar,
            geography varchar,
            watch_time_in_hours float,
            views integer,
            average_view_duration interval
        );
        """
        with self.engine.connect() as conn:
            conn.execute(text(sql_query))
    
        df.to_sql(self.table_name, self.engine, schema='youtube', if_exists='replace', index=False, dtype={
                         'id': sqlalchemy.types.Integer,
                         'city_name': sqlalchemy.types.VARCHAR,
                         'geography': sqlalchemy.types.VARCHAR,
                         'watch_time_in_hours': sqlalchemy.types.Float,
                         'views': sqlalchemy.types.Integer,
                         'average_view_duration': sqlalchemy.types.Interval,
                        })

    """Load data from the PostgreSQL database."""
    def read_from_db(self):
        df = pd.read_sql_table(self.table_name, self.engine, schema='youtube')
        return df
