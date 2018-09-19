from invoke import task
import os

# Name definitions
db_files = ["db.sqlite3", "db.sqlite3-shm", "db.sqlite3-wal"]

app = "bot/application.py"
comm = "bot/communication.py"
linter = "linter/linter.py"

first_test = "tests.test_dialogs.TestBotDialogs.test_if_comm_answers_greetings"
app_test = "tests/test_application.py"
comm_test = "tests/test_communication.py"
dialog_test = "tests/test_dialogs.py"
linter_test = "tests/test_linter.py"


@task
def rmdb(c):
    """ Removes all test databases """
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)


@task(rmdb)
def test(c):
    """ Runs all tests """
    c.run("green3 " + first_test)
    c.run(f"green3 {app_test} {comm_test} {linter_test} -vv")


@task
def style(c):
    """ Cheks if your code is well formatted for this project """
    c.run("pycodestyle bot/. tests/. --ignore=E402,W504")


@task
def doc(c):
    """ Checks if your code is well documented """
    c.run("pydocstyle bot/. tests/.")


@task(rmdb)
def run(c):
    """ Run bot.py """
    c.run("python " + app)


@task()
def travis(c):
    """ Runs the tests checked by Travis """
    style(c)
    lint(c)
    test(c)
    cov(c)


@task
def install(c):
    """ Installs the requirements necessary for this project """
    c.run("pip3 install -r requirements.txt")


@task
def encrypt(c):
    """ Encrypts key for Heroku (for admins only) """
    c.run("travis encrypt-file bot/config.ini --add")


@task(rmdb)
def cov(c):
    """ Checks how much of the program is covered by tests """
    c.run(f"coverage run -m py.test {app_test} {comm_test} {linter_test}")
    c.run(f"coverage report -m {app} {comm} {linter}")
    c.run(f"coverage html {app} {comm} {linter}")


@task()
def lint(c):
    """ Checks yaml file structure """
    c.run("yamllint bot")
