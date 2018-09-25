import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions

# Programa simples que extrai as keywords de um texto

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    username='{user}',
    password='{pess}'
)

# Para limitar a quantidade de resultados, uso o limit=2 para retornar apenas 2 palavras-chave
response = natural_language_understanding.analyze(
    text='Ravioli are a type of dumpling composed of a filling sealed between '
        'two layers of thin pasta dough. Usually served either in broth or with '
        'a pasta sauce, they originated as a traditional food in Italian cuisine.',
    features=Features(
        keywords=KeywordsOptions(limit=2)
    )
)

print(json.dumps(response, indent=2))
