app = bot/application.py
comm = bot/communication.py
app_test = tests/test_application.py
comm_test = tests/test_communication.py

default: test

test:
	green3 . -vv

run:
	python3 $(app)

install:
	pip3 install -r requirements.txt

style:
	pycodestyle bot/ tests/

cov:
	coverage run -m py.test $(app_test) $(comm_test)
	coverage report -m $(app) $(comm)
	coverage html $(app) $(comm)

full:
	@make test
	@make cov
	@make style

encrypt:
	travis encrypt-file bot/config.ini --add

travis:
	green3 .
	coverage run $(app_test)
	coverage run $(comm_test)

help:
	@echo "\n\t Makefile of Projeto Chatbot\n"
	@echo " make.............= Runs the tests using green3"
	@echo " make test........= Also run the tests using green3"
	@echo " make run.........= Run bot.py"
	@echo " make install.....= Install the requirements necessary for this project"
	@echo " make style.......= Cheks if your code is well formatted for this project"
	@echo " make cov.........= Checks how much of the program is covered by tests"
	@echo " make full........= Runs make test, cov and style"
	@echo "\n\t End of Makefile Help\n"
