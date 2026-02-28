import json

def read_query():
    try:
        with open("user_queries.json") as file:
            queries=json.load(file)
        return queries 
    except Exception as e:
        print("Error reading queries:",e)