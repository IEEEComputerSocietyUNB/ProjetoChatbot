import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        # my_reply_markup = InlineKeyboardMarkup(keyboard)
        # update.message.reply_text('Explore more topics:', reply_markup=my_reply_markup, parse_mode=telegram.ParseMode.HTML)

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
    
    def build_question(self, question_index):
        #Uma forma
        count = 1
        formated_question = json_dict_list[question_index]["question"] + "\nEcolha umas das opções a seguir:"
        possible_answers = json_dict_list[question_index]["answers"]
        for answer in possible_answers:
            formated_question = formated_question + "\n**{}**-{}".format(count, answer)
            count += 1
        return formated_question
        #Outra forma
        # return json_dict_list[question_index]["question"]


    def build_button_markup(self, question_index):
        print(json_dict_list[question_index]["question"])

        count = 1
        inline_buttons = []
        possible_answers = json_dict_list[question_index]["answers"]

        #Uma forma
        for answer in possible_answers:
            query_data = "{}{}".format(question_index, count)
            my_button = InlineKeyboardButton(count, callback_data=query_data)
            inline_buttons.append(my_button)
            count += 1
        return InlineKeyboardMarkup([[inline_buttons]])

        #Outra forma
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

s = Screening()
ret = s.initial_screen(s.initial_questions, s.initial_answers)
s.call_next_steps(ret)
