from invoke import task
import os

# Name definitions
first_test = "tests.test_dialogs.TestBotDialogs.test_if_comm_answers_greetings"
db_files = ["db.sqlite3", "db.sqlite3-shm", "db.sqlite3-wal"]
app = "bot/application.py"
app_test = "tests/test_application.py"
comm_test = "tests/test_communication.py"
app_test = "tests/test_application.py"
dialog_test = "tests/test_dialogs.py"
comm = "bot/communication.py"

@task
def rmdb(c):
    """ Removes test database """
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)

@task(rmdb)
def test(c):
    """ Runs all tests """
    c.run("green3 " + first_test)
    c.run("green3 .")

@task
def style(c):
    """ Cheks if your code is well formatted for this project """
    c.run("pycodestyle bot/. tests/. --ignore=E402,W504")

@task
def doc(c):
    c.run("pydocstyle bot/. tests/.")

@task(rmdb)
def run(c):
    """ Run bot.py """
    c.run("python " + app)

@task(pre =[rmdb, style, test], post=[rmdb])
def travis(c):
    """ Also run the tests using green3 """
    style()
    test()
    cov()
    pass

@task
def install(c):
    """ Install the requirements necessary for this project """
    c.run("pip3 install -r requirements.txt")

@task
def encrypt(c):
    c.run("travis encrypt-file bot/config.ini --add")

@task(rmdb)
def cov(c):
    """ Checks how much of the program is covered by tests """
    c.run(f"coverage run -m py.test {app_test} {comm_test} {dialog_test}")
    c.run(f"coverage report -m {app} {comm}")
    c.run(f"coverage html {app} {comm}")

@task(rmdb, test, cov, style)
def full(c):
    """ Checks test, codecoverage and style """
    pass
