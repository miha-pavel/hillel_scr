# hillel_scr

Studying python scraper.

This project supposed to run on `python3`


## Location
This site locate [GitHub Pages](https://github.com/miha-pavel/hillel_scr)


## Colone repository
```
git clone https://github.com/miha-pavel/hillel_scr.git
```


## Before first launch
```
1. python3 -m venv env
2. . env/bin/activate
3. pip install -r requirements.txt
```


## Run Django project
```
python manage.py runserver
```

Or use makefile guide


## Makefile guide
* ```make run``` - will run Django developer server at 8000 port
* ```make test``` - will test the project with --keepdb option
* ```make pep8``` - will check the code with pylint
* ```make check``` - will check
* ```make sh_p``` - will run django shell_plus
* ```make migrate``` - will run django "./manage.py migrate" command
* ```make celery``` - will run celery
* ```make celery_beat``` - will run celerybeat
* ```make rabbit``` - will run rabbitmq brocker
* ```make dc``` - will run docker-compose


## Default super user
* Username: admin
* Email address: admin@admin.com
* Password: admin


### Домашнее задание 21
Добавлено: 19.03.2020 21:50
Дописать парсер
1. Спарсить все детали по каждой выкансии. (6)
2. Сохранить результат в базу данных sqlite3. (2)
3. Сохранить в json файл. (2)