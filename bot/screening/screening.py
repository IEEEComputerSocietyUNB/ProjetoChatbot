import json


# Interface of how the button should work 
def button(question, possible_answers):
    return(2)
#TODO: colocar as DSS ligadas ao next step
class Screening:
    """
    Contains all the Screening information
    """
    def load_jsons(self):
        with open('bot/screening/questions/initial_questions.json') as f:    
            self.initial_questions = json.load(f)
        with open('bot/screening/answers/initial_answers.json') as f:    
            self.initial_answers = json.load(f)
        with open('bot/screening/questions/next_steps.json') as f:    
            self.next_steps = json.load(f)

    def __init__(self):
        self.load_jsons()        
    def iterate_over_questions(self, disturbs, answers):
        """
        user_disturbs contains all disturbs detected
        """

        user_disturbs = []
        for disturb in disturbs:
            # Call button function
            user_choice = button(disturb['question'], answers)
            # If user has enough to be classified
            if(user_choice >= disturb['criterion']):
                user_disturbs.append(disturb['dimension'])
        
        if('Depressão' in user_disturbs and 'Ansiedade' in user_disturbs):        
            user_disturbs.remove('Depressão')
            user_disturbs.remove('Ansiedade')
            user_disturbs.append('Bipolaridade')

        if('Psicose' in user_disturbs and 'Dissociação' in user_disturbs):        
            user_disturbs.remove('Psicose')
            user_disturbs.remove('Dissociação')
            user_disturbs.append('Esquizofrenia')
            
        for disturb in user_disturbs:
            next_step = self.next_steps[disturb]
            if(next_step != ""):
                print(self.next_steps[disturb])

        
    
s = Screening()
s.iterate_over_questions(s.initial_questions, s.initial_answers)
