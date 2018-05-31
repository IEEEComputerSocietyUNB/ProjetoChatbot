app = bot/application.py
comm = bot/communication.py
app_test = tests/test_application.py
first_test = tests.test_communication.TestBotDialogs.test_if_comm_answers_greetings
comm_test = tests/test_communication.py
db_file = db.sqlite3

default: full

rmdb:
	@if [ -a $(db_file) ]; then rm $(db_file); fi

run:
	@make rmdb
	python3 $(app)

install:
	@make rmdb
	pip3 install -r requirements.txt

style:
	@make rmdb
	pycodestyle bot/ tests/

cov:
	@make rmdb
	coverage run -m py.test $(app_test) $(comm_test)
	coverage report -m $(app) $(comm)
	coverage html $(app) $(comm)

full:
	@# check everything on local machine
	@make rmdb
	@make travis
	@make cov
	@make style

encrypt:
	@# needed only when encrypting bot token to travis, no need for production
	travis encrypt-file bot/config.ini --add

travis:
	@# what will run on travis
	@make rmdb
	green3 $(first_test)
	green3 .
	coverage run -m py.test $(app_test) $(comm_test)

help:
	@echo "\n\t Makefile of Projeto Chatbot\n"
	@echo " make.............= Runs the tests using green3"
	@echo " make travis......= Also run the tests using green3"
	@echo " make run.........= Run bot.py"
	@echo " make install.....= Install the requirements necessary for this project"
	@echo " make style.......= Cheks if your code is well formatted for this project"
	@echo " make cov.........= Checks how much of the program is covered by tests"
	@echo " make full........= Checks test, codecoverage and style"
	@echo "\n\t End of Makefile Help\n"
