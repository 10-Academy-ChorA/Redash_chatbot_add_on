from flask import request, jsonify
from redash.handlers.base import (
    BaseResource
)
import os
from openai import OpenAI
VARIABLE_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
  api_key=VARIABLE_KEY
)

class ChatResource(BaseResource):
    def post(self):
        try:
            value = request.get_json()
            question = value.get('question')
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
            answer = completion.choices[0].message.content
            response_data = {"answer": answer}
            return jsonify(response_data), 200
        except Exception as error:
            print(error)
            return jsonify({"error": "An error occurred"}), 500