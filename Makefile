run:
	python manage.py runserver

migration:
	python manage.py makemigrations && python manage.py migrate

superuser:
	python manage.py createsuperuser

i-req:
	pip install -r requirements.txt

r-req:
	pip freeze > requirements.txt

fixture:
	python manage.py dumpdata > fixtures/db.json

l-fixture:
	python manage.py loaddata fixtures/db.json
