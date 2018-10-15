import json
import pprint
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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

    def dass_screen(self, dass):
        dass_dict = self.scales_dict
        questions_answers = []
        answer = dass_dict[dass]['answers']
        for question in dass_dict[dass]['questions']:
            dic = {}
            dic['question'] = question
            dic['answer'] = answer
            questions_answers.append(dic)

        return questions_answers

    def initial_screen(self):
        """
        user_disturbs contains all questions/answers
        """
        disturbs = self.initial_questions
        answers = self.initial_answers
        questions_answers = []
        for disturb in disturbs:
            dic = {}
            dic['question'] = disturb['question']
            dic['answer'] = answers
            questions_answers.append(dic)

        return questions_answers

    def evaluate_initial_screen(self, answers):
        user_disturbs = []

        if(len(answers) != len(self.initial_questions)):
            raise ValueError('Array of different size of questions')

        count = 0
        for disturb in self.initial_questions:
            if(answers[count] >= disturb['criterion']):
                user_disturbs.append(disturb['dimension'])
            count += 1

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

    def build_question(self, question_index):
        # Uma forma
        count = 1
        formated_question = json_dict_list[question_index]["question"] + \
            "\nEcolha umas das opções a seguir:"
        possible_answers = json_dict_list[question_index]["answers"]
        for answer in possible_answers:
            formated_question = formated_question + \
                "\n**{}**-{}".format(count, answer)
            count += 1
        return formated_question
        # Outra forma
        # return json_dict_list[question_index]["question"]

    def build_button_markup(self, question_index):
        print(json_dict_list[question_index]["question"])

        count = 1
        inline_buttons = []
        possible_answers = json_dict_list[question_index]["answers"]

        # Uma forma
        for answer in possible_answers:
            query_data = "{}{}".format(question_index, count)
            my_button = InlineKeyboardButton(count, callback_data=query_data)
            inline_buttons.append(my_button)
            count += 1
        return InlineKeyboardMarkup([[inline_buttons]])

        # Outra forma
        for answer in possible_answers:
            query_data = "s{}{}".format(question_index, count)
            my_button = InlineKeyboardButton(answer, callback_data=query_data)
            inline_buttons.append(count)
            count += 1
        return InlineKeyboardMarkup([[inline_buttons]])

    def button_clicked(self, bot, update):
        query = update.callback_query
        query_str = query.data
        question_index = int(query_str[0])
        answer_index = int(query_str[1])

        question = json_dict_list[question_index]["question"]
        answer = json_dict_list[question_index]["answers"][answer_index]
        return 0
