import json
from googletrans import Translator
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
    import Features, CategoriesOptions, EmotionOptions

translator = Translator()


class Watson:
    def __init__(self, username, password):
        self.user = NaturalLanguageUnderstandingV1(
            version='2018-03-16',
            username=username,
            password=password
        )

    def get_translation(self, text, src='pt', dest='en'):
        return(translator.translate(text, src=src, dest=dest).text)

    def get_categorie(self, text):
        """
        Returns a tuple containing the top categorie and its equivalent score
        """
        text = self.get_translation(text)
        print(text)
        response = self.user.analyze(
            text=text,
            clean=True,
            language='en',
            features=Features(
                categories=CategoriesOptions()
            )
        )
        # Get top 1 categorie
        top_score = (response['categories'][0]['score'])
        top_label = (response['categories'][0]['label'])

        # Print the leaf from category tree
        leaf_category = top_label[top_label.rindex('/') + 1:]

        return(top_score, leaf_category)

    def get_emotion(self, text):
        """
        Returns a tuple containing the top emotion
        and its equivalent relevancy score
        """
        text = self.get_translation(text)
        response = self.user.analyze(
            text=text,
            clean=True,
            language='en',
            features=Features(
                emotion=EmotionOptions()
            )
        )
        emotions_dict = response['emotion']['document']['emotion']
        # Get emotion with highest score rate
        maximum = max(emotions_dict, key=emotions_dict.get)
        # Returns the analised emotion in portuguese
        translated_emotion = self.get_translation(maximum, src='en', dest='pt')

        return(translated_emotion, emotions_dict[maximum] * 100.0)
