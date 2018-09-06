from invoke import task
import os

# Name definitions
first_test = "tests.test_dialogs.TestBotDialogs.test_if_comm_answers_greetings"
db_file = "db.sqlite3"
app = "bot/application.py"
app_test = "tests/test_application.py"
comm_test = "tests/test_communication.py"

@task
def rmdb(c):
    """ Removes test database """
    if os.path.exists(db_file):
        os.remove(db_file)

@task(rmdb)
def test(c):
    """ Runs all tests """
    c.run("green3 " + first_test)
    c.run("green3 .")

@task
def style(c):
    c.run("pycodestyle bot/. tests/. --ignore=E402,W504")

@task
def doc(c):
    c.run("pydocstyle bot/. tests/.")

@task(rmdb)
def run(c):
    c.run("python3.6 " + app)

@task(pre = [rmdb, style, test], post=[rmdb])
def travis(c):
    """ What will run on travis """
    print('hey')