import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
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
                (
                    "Por que o robô atravessou a rua? " +
                    "Porque ele foi programado por uma galinha"
                ),
                "Como você para um robô de destruir o mundo? Você não para.",
            ],
        )

    def test_if_comm_answers_fellings(self):
        """
        Check if communication answers feelings appropriately
        """
        dialog_options = [
            "Qual você acredita ser a causa desse sentimento?",
            "Em quais situações você costuma se sentir assim?",
            "Esse sentimento é comum no seu círculo social?",
            "Desde quando você tem se sentido assim?",
        ]
        self.assertIn(
            self.comm.respond("Eu tenho me sentido bastante deprimido"),
            dialog_options
        )
        self.assertIn(
            self.comm.respond("Eu tenho me sentido com raiva"),
            dialog_options
        )
        self.assertIn(
            self.comm.respond("Eu tenho sentido dores inexplicáveis"),
            dialog_options
        )
        self.assertIn(
            self.comm.respond(
                "Eu tenho evitado situações que me deixam ansioso"
            ), dialog_options
        )
        self.assertIn(
            self.comm.respond(
                "Eu tenho sentido como se eu pudesse ouvir o que outras " +
                "pessoas pensam"
            ), dialog_options
        )
        self.assertIn(
            self.comm.respond(
                "Eu tenho me sentido como se eu não fosse eu mesmo"
            ), dialog_options
        )
        self.assertIn(
            self.comm.respond(
                "Eu tenho começado mais projetos do que costumo fazer"
            ), dialog_options
        )
        self.assertIn(
            self.comm.respond("Eu tenho pensado sobre machucar a mim mesmo"),
            dialog_options
        )
        self.assertIn(
            self.comm.respond(
                "Eu tenho tido problemas para dormir que afetam minha " +
                "qualidade de sono"
            ), dialog_options
        )
        self.assertIn(
            self.comm.respond("Eu tenho tido problemas de memória"),
            dialog_options
        )
        self.assertIn(
            self.comm.respond("Eu tenho repetido várias vezes"),
            dialog_options
        )
        self.assertIn(
            self.comm.respond("Eu tenho ingerido muitas vezes"),
            dialog_options
        )

    def test_if_comm_answers_triggers(self):
        """
        Check if communication answers dialog triggers appropriately
        """
        self.assertEqual(self.comm.respond("Que bom"), "Sim, muito bom mesmo!")
        self.assertEqual(
            self.comm.respond("Conte-me novidades"),
            "Nada de mais, alguns bits trocados aqui e ali, e você?",
        )
        self.assertEqual(self.comm.respond("Que bom"), "Sim, muito bom mesmo!")


if __name__ == "__main__":
    unittest.main()
