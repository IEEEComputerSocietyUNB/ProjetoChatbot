import unittest
import sys
import os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.realpath(__file__))
    )
)
from bot.communication import Communication


class TestBotDialogs(unittest.TestCase):
    """
    Tests on dialogs are needed to verify that the bot has no weird dialog.
    Important due to seriousness of emotional triggers.
    """

    def setUp(self):
        self.comm = Communication()

    def tearDown(self):
        self.comm = None

    def test_if_comm_answers_greetings(self):
        """
        Check if communication answers greetings appropriately
        """
        self.assertEqual(self.comm.respond("oi"), "Olá, tudo bom?")

    def test_if_comm_answers_greetings2(self):
        """
        Check if communication answers greetings appropriately
        """
        self.assertEqual(self.comm.respond("Olá, tudo bom?"), "Tudo, e você?")
        self.assertEqual(self.comm.respond("Tudo, e você?"), "Também")
        self.assertEqual(self.comm.respond("Ok"), "Quais as novidades?")

    def test_if_comm_answers_jokes(self):
        """
        Check if communication answers jokes appropriately
        """
        self.assertIn(
            self.comm.respond("Conte-me uma piada"),
            [
                "Por que o robô foi ao médico? Porque ele tinha vírus!",
                "Como um robô pirata se chama? Argh2D2.",
                ("Por que o robô atravessou a rua? " +
                    "Porque ele foi programado por uma galinha"),
                "Como você para um robô de destruir o mundo? Você não para."
            ]
        )

    def test_if_comm_answers_fellings(self):
        """
        Check if communication answers feelings appropriately
        """
        self.assertIn(
            self.comm.respond("Eu tenho me sentido bastante deprimido"),
            [
                "Qual você acredita ser a causa desse sentimento?",
                "Em quais situações você costuma se sentir assim?",
                "Esse sentimento é comum no seu círculo social?",
                 "Desde quando você tem se sentido assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho me sentido com raiva"),
            [
                "Qual você acredita ser a causa desse sentimento?",
                "Em quais situações você costuma se sentir assim?",
                "Esse sentimento é comum no seu círculo social?",
                 "Desde quando você tem se sentido assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho sentido dores inexplicáveis),
            [
                "Qual você acredita ser a causa desse sentimento?",
                "Em quais situações você costuma se sentir assim?",
                "Esse sentimento é comum no seu círculo social?",
                 "Desde quando você tem se sentido assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho evitado situações que me deixam ansioso),
            [
                "Qual você acredita ser a causa desse comportamento?",
                "Em quais situações você costuma se comportar assim?",
                "Esse comportamento é comum no seu círculo social?",
                 "Desde quando você tem se comportado assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho sentido como se eu pudesse ouvir o que outras pessoas pensam),
            [
                "Qual você acredita ser a causa desse sentimento?",
                "Em quais situações você costuma se sentir assim?",
                "Esse sentimento é comum no seu círculo social?",
                 "Desde quando você tem se sentido assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho me sentido como se eu não fosse eu mesmo"),
            [
                "Qual você acredita ser a causa desse sentimento?",
                "Em quais situações você costuma se sentir assim?",
                "Esse sentimento é comum no seu círculo social?",
                 "Desde quando você tem se sentido assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho começado mais projetos do que costumo fazer"),
            [
                "Qual você acredita ser a causa desse comportamento?",
                "Em quais situações você costuma se comportar assim?",
                "Esse comportamento é comum no seu círculo social?",
                 "Desde quando você tem se comportado assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho pensado sobre machucar a mim mesmo"),
            [
                "Qual você acredita ser a causa desse pensamento?",
                "Em quais situações você costuma pensar assim?",
                "Esse pensamento é comum no seu círculo social?",
                 "Desde quando você tem pensa assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho tido problemas para dormir que afetam minha qualidade de sono"),
            [
                "Qual você acredita ser a causa desse problema?",
                "Esse problema é comum no seu círculo social?",
                 "Desde quando você tem esse problema?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho tido problemas de memória"),
            [
                "Qual você acredita ser a causa desse problema?",
                "Esse problema é comum no seu círculo social?",
                 "Desde quando você tem esse problema?",
                 "Em quais situações você costuma ter esse problema?",
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho repetido várias vezes"),
            [
                "Qual você acredita ser a causa desse comportamento?",
                "Em quais situações você costuma se comportar assim?",
                "Esse comportamento é comum no seu círculo social?",
                 "Desde quando você tem se comportado assim?"
            ]
        )
        self.assertIn(
            self.comm.respond("Eu tenho ingerido muitas vezes"),
            [
                "Qual você acredita ser a causa desse comportamento?",
                "Em quais situações você costuma se comportar assim?",
                "Esse comportamento é comum no seu círculo social?",
                 "Desde quando você tem se comportado assim?"
            ]
        )
    def test_if_comm_answers_triggers(self):
        """
        Check if communication answers dialog triggers appropriately
        """
        self.assertEqual(self.comm.respond("Que bom"), "Sim, muito bom mesmo!")
        self.assertEqual(self.comm.respond(
            "Conte-me novidades"),
            "Nada de mais, alguns bits trocados aqui e ali, e você?"
        )
        self.assertEqual(self.comm.respond("Que bom"), "Sim, muito bom mesmo!")


if __name__ == '__main__':
    unittest.main()
