from invoke import task
import os

@task
def build(c):
    print("Building!")

@task
def rmdb(c):
    """ Removes test database """
    if os.path.exists("db.sqlite3"):
        print('hey')
        os.remove("db.sqlite3")