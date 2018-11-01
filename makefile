app = bot/application.py
comm = bot/communication.py
linter = linter/linter.py
all_apps = $(app) $(comm) $(linter)
first_test = tests.test_communication.TestBotCommunication.test_if_comm_answers
app_test = tests/test_application.py
comm_test = tests/test_communication.py
dialog_test = tests/test_dialogs.py
linter_test = tests/test_linter.py
all_tests = $(app_test) $(comm_test) $(dialog_test) $(linter_test)
db_file = db.sqlite3
emotions_db_file = emotions.sqlite3

.PHONY: test rmdb travis run cov style doc full encrypt install help yaml

default: full

test:
	@make style
	@make yaml
	@make rmdb
	green3 $(first_test)
	green3 .

rmdb:
	@if [ -a $(db_file) ]; then rm $(db_file); fi
	#@if [ -a $(emotions_db_file) ]; then rm $(emotions_db_file); fi

travis:
	@# what will run on travis
	@make rmdb
	green3 $(first_test)
	green3 $(app_test) $(comm_test) $(linter_test)
	coverage run -m py.test $(app_test) $(comm_test) $(linter_test)

full:
	@# check everything on local machine
	@make test
	@make cov

rmdb:
	@if [ -a $(db_file) ]; then rm $(db_file); fi

run:
	@make rmdb
	python3 $(app)

cov:
	@make rmdb
	coverage run -m py.test $(all_tests)
	coverage report -m $(all_apps)
	coverage html $(all_apps)

style:
	@pycodestyle bot/. tests/. --ignore=E402,W504

doc:
	pydocstyle bot/. tests/.

linter:
	@yamllint bot/
	@echo "All yaml files ok."

encrypt:
	@# needed only when encrypting bot token to travis, no need for production
	travis encrypt-file bot/config.ini --add

install:
	pip3 install -r requirements.txt

html:
	@open -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome htmlcov/index.html

help:
	@echo "\n\t Makefile of Projeto Chatbot\n"
	@echo " make.............= Runs the tests using green3"
	@echo " make travis......= Also run the tests using green3"
	@echo " make run.........= Run bot.py"
	@echo " make cov.........= Checks how much of the program is covered by tests"
	@echo " make style.......= Cheks if your code is well formatted for this project"
	@echo " make full........= Checks test, codecoverage and style"
	@echo " make install.....= Install the requirements necessary for this project"
	@echo "\n\t End of Makefile Help\n"
