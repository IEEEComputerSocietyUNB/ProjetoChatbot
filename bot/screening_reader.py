import json
from pprint import pprint

with open('bot/screening/screening_questions.json') as f:
    data = json.load(f)

#TODO: terminar o Json
    
print(data[1]["Dimensão"])