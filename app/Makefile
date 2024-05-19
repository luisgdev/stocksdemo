run:
	~/python_venv/bin/poetry run python manage.py runserver

migrate:
	~/python_venv/bin/poetry run python manage.py makemigrations
	~/python_venv/bin/poetry run python manage.py migrate

createsuperuser:
	~/python_venv/bin/poetry run python manage.py createsuperuser

test:
	pytest ./tests/

check:
ifdef target
		@echo 'Info: `target` is $(target)'
		isort $(target)
		black $(target) -l 99
		pylint $(target)
else
		@echo 'Error: `target` directory or file, was not specified'
endif
