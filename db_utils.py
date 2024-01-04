import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine


class DBUtils:
    def connectDB(self):
        host=os.getenv('DB_HOST')
        port=os.getenv('DB_PORT')
        dbname=os.getenv('DB_NAME')
        user=os.getenv('DB_USER')
        password=os.getenv('DB_PASSWORD')
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
        return engine

    
