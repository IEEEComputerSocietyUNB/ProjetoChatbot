# Guia de uso Watson

## Observações

### Instalação

```
pip install --upgrade watson-developer-cloud
```

### Autenticação

Para loggar no sistema é necessário uma conta. Pode-se usar este [link](https://console.bluemix.net/registration/?target=%2Fcatalog%2Fservices%2Fnatural-language-understanding%3FhideTours%3Dtrue%26cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmc%3DOSocial_Tumblr-_-Watson%2BCore_Watson%2BCore%2B-%2BPlatform-_-WW_WW-_-wdc-ref%26cm_mmca1%3D000000OF%26cm_mmca2%3D10000409&cm_mc_uid=34579651053815360869704&cm_mc_sid_50200000=81302361536086970412&cm_mc_sid_52640000=61577331536086970417)
e depois usando o painel de sua conta para acessar as credenciais. Estas devem ser usadas conforme:

```python
from watson_developer_cloud import NaturalLanguageUnderstandingV1
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='{version}',
    username='{username}',
    password='{password}',
    url='https://gateway-fra.watsonplatform.net/natural-language-understanding/api'
)
```

### Português

O Watson não disponibiliza algumas *features* para o português, como: análise de conceitos, emoções, relações ou papéis semânticos. Será focado agora no que a API pode produzir

## Keywords

Retorna as palavras chaves do texto em questão. Execute o programa **simple_keywords.py** para ver o output gerado:

```json
{
  "usage": {
    "text_characters": 211,
    "text_units": 1,
    "features": 1
  },
  "keywords": [
    {
      "relevance": 0.954154,
      "text": "pasta dough"
    },
    {
      "relevance": 0.884465,
      "text": "pasta sauce"
    }
  ],
  "language": "en"
}
```

Como o texto usado fala de Ravioli, as palavras-chave encontradas se referem justamente a isso.

## Categories

Pelas análises feitas, esta é a seção que melhor funciona para português.Retorna as categorias mais relevantes. Execute o programa **categories.py** para ver o output:

```json
{
  "usage": {
    "features": 1,
    "text_units": 1,
    "text_characters": 1099
  },
  "language": "pt",
  "categories": [
    {
      "score": 0.348674,
      "label": "/business and industrial"
    },
    {
      "score": 0.245297,
      "label": "/technology and computing"
    },
    {
      "score": 0.168891,
      "label": "/technology and computing/software"
    }
  ],
  "retrieved_url": "www.ibm.com/br-pt/"
}
```

Aqui foi passada a url do site em potuguês da ibm.

## Entities

Aqui, são analisadas as entidades de um texto(pessoas, companhias...) Para testar o código foi passada a *url* da página do herói nacional Guilherme Briggs na wikipédia. Execute o programa **entities.py** para ver o output:

```json
{
  "language": "pt",
  "retrieved_url": "pt.wikipedia.org/wiki/Guilherme_Briggs",
  "entities": [
    {
      "count": 8,
      "text": "Guilherme Briggs",
      "relevance": 0.954118,
      "sentiment": {
        "label": "positive",
        "score": 0.0591588
      },
      "type": "Person"
    }
  ],
  "usage": {
    "features": 1,
    "text_characters": 8188,
    "text_units": 1
  }
}
```

Além disso, foi "setada" a flag para analisar o sentimento em relação à entidade, que aqui é positiva.
