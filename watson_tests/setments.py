import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, SentimentOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    username='{user}',
    password='{pess}'
)


response = natural_language_understanding.analyze(
  url='https://pt.wikipedia.org/wiki/Mahatma_Gandhi',
  features=Features(
    sentiment=SentimentOptions(
        # - A API analizará os sentimentos para cada uma das strings do array 'targets'.
        # - Um score positivo estam associados a sentimento positivo e scores negativo à
        #   sentimentos negativos.
        # - labels indica se o sentimento geral é positivo negativo ou neutro
        # - Existe um limite de 50000 caracteres para análise do Watson
        # - o score do documento todo NÃO muda de acordo com strings passadas como target
      targets=['direitos', 'governo'])))


print(json.dumps(response, indent=2))
