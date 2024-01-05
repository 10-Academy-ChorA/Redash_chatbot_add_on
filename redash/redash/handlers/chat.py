from flask import request, jsonify
from redash.handlers.base import (
    BaseResource
)
import os
from redashAPI import RedashAPIClient

from openai import OpenAI
VARIABLE_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
  api_key=VARIABLE_KEY
)
REDASH_API_KEY = os.environ.get('REDASH_API_KEY')


class ChatResource(BaseResource):
    def post(self):
        try:
            value = request.get_json()
            question = value.get('question')
            result = self.get_sql_query(question)
            is_sql  = self.check_if_valid_sql(result)
            if(is_sql):
                self.perform_redash_request(result)
            response_data = {"answer": result}
            return jsonify(response_data), 200
        except Exception as error:
            print(error)
            return jsonify({"error": "An error occurred"}), 500
        
    def get_sql_query(self,question):    
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                    "content": """You are a redash visualization assistant, skilled in SQL queries and data visualization. You are only required to give answers for query and data visualization questions. If asked about a topic outside these two, make sure to respond that you have no information regarding that question reply with I am only here to help you with your query and data visualization questions. When asked to write queries,the query MUST NOT make changes to the database.IT MUST ONLY BE A SELECT STATEMENT. MAKE SURE YOU ONLY RESPOND WITH THE SQL QUERY AND NOTHING ELSE.AND MAKE YOUR ANSWER SINGLE LINED. Below are the SQL tables you'll answer from. \n    \n    
      
                    CREATE TABLE youtube.cities_chart(
                            id integer,
                            city_name varchar,
                            date DATE,
                            views integer
                    );\n    \n 
                    CREATE TABLE youtube.cities_aggregate(
                            id integer,
                            city_name varchar,
                            geography varchar,
                            watch_time_in_hours float,
                            views integer,
                            average_view_duration interval
                    );\n    \n 
                    CREATE TABLE youtube.device_type_chart(
                            id integer,
                            name varchar,
                            date DATE,
                            views integer
                    ); \n    \n 
                    CREATE TABLE youtube.device_type_aggregate(
                        id integer,
                        name varchar,
                        watch_time_in_hours float,
                        views integer,
                        average_view_duration interval
                    );\n    \n """
                    },
                    {"role": "user", "content": question}
                ]
            )
        sql_answer = completion.choices[0].message.content
        return sql_answer
    
    def check_if_valid_sql(self,question):    
        completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                    "content": """You are a SQL MASTER. You know if the provided input is a valid SQL or not. If the provided input is NOT a valid input you return FALSE. If the provided input is a valid input you return TRUE. MAKE SURE YOUR ANSWER IS ONLY EITHER TRUE OR FALSE. NOTHING ELSE. NOT EVEN PUNCTUATION MARKS"""
                    },
                    {"role": "user", "content": question}
                ]
            )
        is_valid_sql = completion.choices[0].message.content
        return is_valid_sql
    
    def perform_redash_request(self,query_string):
        Redash = RedashAPIClient(REDASH_API_KEY, 'http://localhost:5000')
        res = Redash.get('data_sources')
        data_source_id = res.json()[0]['id']
        res = Redash.create_query(data_source_id, "Query", query_string)
        query_id = res.json()['id']
        res = Redash.create_visualization(query_id, "table", "Visualization", columns=[
    {"name": "column 1", "type": "string"}
])
        visualization_id  = res.json()['id']
        res = Redash.get('dashboards')
        dashboard_id = res.json()['results'][0]['id']
        Redash.add_widget(dashboard_id, vs_id=visualization_id,position={"col": 0,
            "row": 0,
            "sizeX": 3,
            "sizeY": 8})
