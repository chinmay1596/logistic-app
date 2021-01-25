find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

python manage.py  makemigrations account
python manage.py migrate account

python manage.py makemigrations customer
python manage.py migrate customer

python manage.py makemigrations employee
python manage.py migrate employee

python manage.py makemigrations warehouse
python manage.py migrate warehouse

python manage.py makemigrations orders
python manage.py migrate orders

python manage.py makemigrations fleet
python manage.py migrate fleet

python manage.py makemigrations analytics
python manage.py migrate analytics

python manage.py makemigrations notification
python manage.py migrate notification

python manage.py makemigrations
python manage.py migrate

python manage.py create_groups
python manage.py create_super_admin
