import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    username='{user}',
    password='{pess}'
)

# Aqui, setei o arg sentiment=True para analisar o sentimento
# Atrelado a cada entidade
response = natural_language_understanding.analyze(
  url='pt.wikipedia.org/wiki/Guilherme_Briggs',
  features=Features(
    entities=EntitiesOptions(
      sentiment=True,
      limit=1)))

print(json.dumps(response, indent=2))
