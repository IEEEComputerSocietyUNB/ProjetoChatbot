import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, CategoriesOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    username='{user}',
    password='{pess}'
)

# Pode-se passar um url como fonte de texto
# O parametro clean remove anuncios e afins
# e o parametro language é automático então
# apenas é necessário quando precisa-se
# explicitar a linguagem usada.
response = natural_language_understanding.analyze(
  url='www.ibm.com/br-pt/',
  clean=True,
  language='pt',
  features=Features(
    categories=CategoriesOptions()))

print(json.dumps(response, indent=2))
