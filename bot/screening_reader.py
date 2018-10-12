import json
from pprint import pprint


with open('screening/screening_questions.json') as f:    
    data = json.load(f)

#TODO: terminar o Json

for i in data:
    print(i["Dimensão"])
    print(i["Pergunta"])
    print(i["Critério Triagem"])