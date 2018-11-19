import json
import pprint
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

SOCIODEMOGRAFICO, DASS_21A, DASS_21D, DASS_21S = range(4)


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
            self.scales_dict['DASS_21A'] = json.load(f)
        with open('bot/screening/questions/DASS-21D.json') as f:
            self.scales_dict['DASS_21D'] = json.load(f)
        with open('bot/screening/questions/DASS-21S.json') as f:
            self.scales_dict['DASS_21S'] = json.load(f)
        return 0

    def __init__(self):
        self.scales_dict = {}
        self.initial_dict = {}
        self.user_answers = {
                        str(SOCIODEMOGRAFICO) : {
                            "needed" : True,
                            "given_answer": []
                        },
                        str(DASS_21A) : {
                            "needed" : False,
                            "given_answer" : []
                        },
                        str(DASS_21D) : {
                            "needed" : False,
                            "given_answer" : []
                        },
                        str(DASS_21S) : {
                            "needed" : False,
                            "given_answer" : []
                        }
        }
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

    def initial_screen(self, bot, update):
        """
        user_disturbs contains all questions/answers
        """
        self.call_next_question(
            bot, update.message.chat_id, SOCIODEMOGRAFICO, 0)
        return 0

    def get_equivalent_range(self, string):
        if string == 'SOCIODEMOGRAFICO':
            return 0
        elif string == 'DASS_21A':
            return 1
        elif string == 'DASS_21D':
            return 2
        elif string == 'DASS_21S':
            return 3
        else:
            return -1

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

        next_steps = list(set(next_steps))

        self.user_answers[str(SOCIODEMOGRAFICO)]['needed'] = False
        for step in next_steps:
            step_id = self.get_equivalent_string(step)
            print(step_id)
            print(f"step {str(step_id)}")
            self.user_answers[str(step_id)]['needed'] = True

    def call_next_steps(self, next_steps):
        scales = []
        for step in next_steps:
            scales += self.scales_dict[step]
        self.scales_to_answer = scales

    def call_next_question(self, bot, chat_id, stage, question_index):
        answers = []
        question = None
        # Jumping for next stage, question_index must be 0
        print(f"stage:{stage}\nq_index:{question_index}")
        while(self.user_answers[str(stage)]["needed"] is not True):
            stage += 1

        if(stage == SOCIODEMOGRAFICO):
            question = self.initial_questions[question_index]["question"]
            answers = self.initial_questions[question_index]["answer"]
        elif(stage == DASS_21A):
            tuples_qa = self.dass_screen("DASS_21A")
            question = tuples_qa[question_index]["question"]
            answers = tuples_qa[question_index]["answer"]
        elif(stage == DASS_21D):
            tuples_qa = self.dass_screen("DASS_21D")
            question = tuples_qa[question_index]["question"]
            answers = tuples_qa[question_index]["answer"]
        elif(stage == DASS_21S):
            tuples_qa = self.dass_screen("DASS_21S")
            question = tuples_qa[question_index]["question"]
            answers = tuples_qa[question_index]["answer"]

        keyboard_markup = self.build_button_markup(
            stage, question_index, answers)
        bot.send_message(chat_id=chat_id,
                         text=question, reply_markup=keyboard_markup)

        return 0

    def build_button_markup(self, stage, question_index, answers):
        i = 0
        inline_buttons = []
        possible_answers = self.initial_questions[question_index]["answer"]

        # Uma forma
        while(i < len(possible_answers)):
            list_temp = []

            query_data = f"{stage}{question_index}{i}"
            my_button = InlineKeyboardButton(possible_answers[i],
                                             callback_data=query_data)
            list_temp.append(my_button)

            i = i + 1
            if (i < len(possible_answers)):
                query_data = f"{stage}{question_index}{i}"
                my_button = InlineKeyboardButton(possible_answers[i],
                                                 callback_data=query_data)
                list_temp.append(my_button)

            inline_buttons.append(list_temp)
            i = i + 1
        return InlineKeyboardMarkup(inline_buttons)

    def button_clicked(self, bot, update):
        query = update.callback_query
        query_str = query.data
        stage = int(query_str[0])
        question_index = int(query_str[1])
        answer_index = int(query_str[2])
        tam = 0
        # saving answer
        if(stage == SOCIODEMOGRAFICO):
            self.user_answers[str(SOCIODEMOGRAFICO)]["given_answer"]. \
                append(answer_index)
            tam = len(self.initial_questions)
        elif(stage == DASS_21A):
            self.user_answers[str(DASS_21A)]["given_answer"]. \
                append(answer_index)
            tam = len(self.dass_screen("DASS_21A")[question_index]["answer"])
        elif(stage == DASS_21D):
            self.user_answers[str(DASS_21D)]["given_answer"]. \
                append(answer_index)
            tam = len(self.dass_screen("DASS_21D")[question_index]["answer"])
        elif(stage == DASS_21S):
            self.user_answers[str(DASS_21S)]["given_answer"]. \
                append(answer_index)
            tam = len(self.dass_screen("DASS_21S")[question_index]["answer"])

        #Going for next stage
        print(f"tam:{tam}")
        print(f"question_index+1{question_index+1}")
        if(tam == question_index+1):
            # recebe o stage atual e acessa as resposta em
            # self.user_answers[stage]["given_answer"], avalia quais
            # questionarios precisam ser respondidos, e modifica
            # self.user_answers[stage]["needed"] para True
            if(stage == SOCIODEMOGRAFICO):
                self.evaluate_initial_screen(
                    self.user_answers[str(stage)]["given_answer"]
                )
            print("AHUAUA")
            self.call_next_question(bot, query.message.chat_id, stage+1, 0)
        else:
            print("QQQQQ")
            self.call_next_question(bot, query.message.chat_id, stage, question_index+1)

        return 0
