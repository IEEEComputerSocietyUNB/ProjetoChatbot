default: test

test:
	green3 . -vvv

run:
	python3 bot/bot.py

install:
	pip3 install -r requirements.txt

style:
	pycodestyle bot/ tests/

cov:
	coverage run -m py.test tests/test.py
	coverage report -m bot/bot.py
	coverage html bot/bot.py

full:
	make test
	make cov
	make style
  
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
