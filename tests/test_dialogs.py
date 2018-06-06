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
        self.assertEqual(self.comm.respond("Olá, tudo bom?"), "Tudo, e você?")

    def test_if_comm_answers_greetings2(self):
        """
        Check if communication answers greetings appropriately
        """
        self.assertEqual(self.comm.respond("Olá"), "Olá, tudo bom?")
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
