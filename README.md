# TaskPlus

## Instalation 

1. install requirements:

```bash
pip install -r requirements.py
```

2. Make migrations and migrate:

```bash
python manage.py makemigrations

python manage.py migrate
```

3. Run Redis (you can run it in any way ):

```bash
docker run -d -p 5679:6379 --name my-redis redis
```

4. Run Celery worker:

```bash
celery -A TaskPlus worker --loglevel=info
```

5. Run server :

```bash
pythn manage.py runserver
```
