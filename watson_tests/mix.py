import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions, EntitiesOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    username='{user}',
    password='{pess}'
)


response_entities = natural_language_understanding.analyze(
  url='https://pt.wikipedia.org/wiki/Josef_Stalin',
  features=Features(
    entities=EntitiesOptions(
      sentiment=True,
      limit=2)))
#obtendo o nome das entidades
entitieA = response_entities["entities"][0]["text"]
entitieB = response_entities["entities"][1]["text"]

response = natural_language_understanding.analyze(
  url='https://pt.wikipedia.org/wiki/Josef_Stalin',
  features=Features(
    sentiment=SentimentOptions(
      #se as strings target não forem encontradas retorna erro
      targets=[entitieA, entitieB])))


print(json.dumps(response, indent=2))
