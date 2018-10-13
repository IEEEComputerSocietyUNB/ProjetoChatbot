import json


# Interface of how the button should work
def button(question, possible_answers):
    return(3)


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
        with open('bot/screening/questions/DASS-21A.json') as f:
            self.scales_dict['DASS-21A'] = json.load(f)
        with open('bot/screening/questions/DASS-21D.json') as f:
            self.scales_dict['DASS-21D'] = json.load(f)
        with open('bot/screening/questions/DASS-21S.json') as f:
            self.scales_dict['DASS-21S'] = json.load(f)

    def __init__(self):
        self.scales_dict = {}
        self.load_jsons()

    def initial_screen(self, disturbs, answers):
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

        next_steps = []
        for disturb in user_disturbs:
            next_steps += self.next_steps[disturb]
        # Returns the next steps(without duplicates)
        return(list(set(next_steps)))

    def call_next_steps(self, next_steps):
        print(next_steps)
        for step in next_steps:
            scale = self.scales_dict[step]
            button(scale['questions'], scale['answers'])


s = Screening()
ret = s.initial_screen(s.initial_questions, s.initial_answers)
s.call_next_steps(ret)
