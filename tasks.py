import os
import sys
import webbrowser
from invoke import task

# Name definitions
db_files = ['db.sqlite3', 'db.sqlite3-shm', 'db.sqlite3-wal']

config = 'bot/config_reader.py'
app = 'bot/application.py'
comm = 'bot/communication.py'
linter = 'linter/linter.py'

first_test = 'tests.test_dialogs.TestBotDialogs.test_if_comm_answers_greetings'
config_test = 'tests/test_config_reader.py'
app_test = 'tests/test_application.py'
comm_test = 'tests/test_communication.py'
dialog_test = 'tests/test_dialogs.py'
linter_test = 'tests/test_linter.py'


@task
def rmdb(c):
    """ Removes all test databases """
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)


@task(rmdb)
def test(c, vv=False):
    """ Runs all tests """
    detail = ""
    if vv:
        detail = '-vv'
    c.run(f'green3 {first_test}')
    c.run(f'green3 {app_test} {comm_test} {linter_test} {config_test} {detail}')


@task
def style(c):
    """ Cheks if your code is well formatted for this project """
    c.run('pycodestyle bot/. tests/. --ignore=E402,W504')


@task
def doc(c):
    """ Checks if your code is well documented """
    c.run('make --directory docs/ html')
    webbrowser.open('file://' + os.path.realpath('docs/_build/html/index.html'))
    c.run('pydocstyle bot/. tests/.')


@task(rmdb)
def run(c):
    """ Run bot.py """
    c.run('python ' + app)


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
    c.run('pip3 install -r requirements.txt')


@task
def encrypt(c):
    """ Encrypts key for Heroku (for admins only) """
    c.run('travis encrypt-file bot/config.ini --add')


@task(rmdb)
def cov(c):
    """ Checks how much of the program is covered by tests """
    c.run(f'coverage run -m py.test\
          {app_test} {comm_test} {linter_test} {config_test}')
    c.run(f'coverage report -m {app} {comm} {linter} {config}')
    c.run(f'coverage html {app} {comm} {linter} {config}')


@task()
def lint(c):
    """ Checks yaml file structure """
    c.run('yamllint bot')

@task()
def encrypt(c):
	""" Needed only when encrypting bot token to travis """
	c.run('travis encrypt-file bot/config.ini --add')
