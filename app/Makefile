# Poetry executable path.
poetry = poetry
python_manage = python manage.py

run:
	$(poetry) run $(python_manage) makemigrations
	$(poetry) run $(python_manage) migrate
	$(poetry) run $(python_manage) runserver 0.0.0.0:5000

createsuperuser:
	$(poetry) run $(python_manage) createsuperuser

test:
	pytest ./tests/

check:
ifdef target
		isort $(target)
		black $(target) -l 99
		pylint $(target)
else
		@echo 'Error: `target` directory or file, was not specified'
endif
