import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, CategoriesOptions, EntitiesOptions


class Watson:
    def __init__(self, username, password):
        self.user = NaturalLanguageUnderstandingV1(
            version='2018-03-16',
            username=username,
            password=password
        )

    def get_analysis(self, text):
        """
        Returns a dictionary containing categories and entities
        """
        response = self.user.analyze(
            text=text,
            clean=True,
            language='pt',
            features=Features(
                categories=CategoriesOptions(),
                entities=EntitiesOptions()
            )
        )

        return(response)
