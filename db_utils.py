import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine,MetaData


class DBUtils:
    def __init__(self):
        # Load environment variables
        host=os.getenv('DB_HOST')
        port=os.getenv('DB_PORT')
        dbname=os.getenv('DB_NAME')
        user=os.getenv('DB_USER')
        password=os.getenv('DB_PASSWORD')
        # Create the SQLAlchemy engine
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
        self.engine = engine

    def connectDB(self):
        return self.engine
    # the below doesn't work for what I intended it to
    # def get_all_tables_definition(self):
    #     # Create a MetaData object
    #     metadata = MetaData(bind=self.engine)
    #     MetaData.reflect(metadata,schema='youtube')

    #     #  Initialize an empty string to store the SQL statements
    #     create_table_sql = ""
    #     for table_name, _ in metadata.tables.items():
    #         print(table_name)
    #         table = metadata.tables[table_name]
    #         print(table.columns)
    #         create_table_sql += f"CREATE TABLE {table_name} (\n"
    #         for column in table.columns:
    #             create_table_sql += f"\t{column.compile(dialect=self.engine.dialect)},\n"
    #         create_table_sql += ");\n\n"



# if(__name__ == "__main__"):
#     db = DBUtils()
#     print(db.get_all_tables_definition())