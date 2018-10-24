import bot.dialogflow.entity_management as EM
import bot.dialogflow.entity_type_management as ETM
import bot.dialogflow.intent_management as IM
import bot.dialogflow.detect_intent_texts as DIT
import bot.dialogflow.session_entity_type_management as SETM
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= str(os.getcwd()) +"\\bot\\dialogflow\\credentials.json"
GCLOUD_PROJECT = "rabot-free-test"

class Dialog:

    def create(self):
        print('Create Dialog')

        #createSession(GCLOUD_PROJECT, '1', entity_values, entity_type_display_name, entity_override_mode)
        try:
            self.createIntent(GCLOUD_PROJECT, 'intent-sentimento-depressao', 'Estou depressivo teste', 'resposta teste')
            self.createEntityType(GCLOUD_PROJECT, 'Tema', 1)
            self.createEntities(GCLOUD_PROJECT, entity_type_id, 'depressão', ['depressivo', 'depressiva'])
            pass
        except Exception as e:
            pass  

        entity_type_id = ETM._get_entity_type_ids(GCLOUD_PROJECT, 'Tema')[0]
        ETM.list_entity_types(GCLOUD_PROJECT)
        EM.list_entities(GCLOUD_PROJECT, entity_type_id)     
        IM.list_intents(GCLOUD_PROJECT)         

    def response(self, message): 
        #self.detectIntent(GCLOUD_PROJECT, session_id, message, 'pt-BR')
        print('response: ' + message)

    def detectIntent(project_id, session_id, texts, language_code):
        DIT.detect_intent_texts(project_id, session_id, texts, language_code)

    def createEntityType(self, project_id, display_name, kind):
        ETM.create_entity_type(project_id, display_name, kind)

    def createEntities(self, project_id, entity_type_id, entity_value, synonyms):
        EM.create_entity(project_id, entity_type_id, entity_value, synonyms)

    def createIntent(project_id, display_name, training_phrases_parts, message_texts):
        IM.create_intent(project_id, display_name, training_phrases_parts, message_texts)

    def createSession(project_id, session_id, entity_values, entity_type_display_name, entity_override_mode):
        SETM.create_session_entity_type(project_id, session_id, entity_values, entity_type_display_name, entity_override_mode)




