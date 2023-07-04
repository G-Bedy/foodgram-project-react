# Проект Foodgram

![example workflow](https://github.com/G-Bedy/foodgram-project-react/actions/workflows/main.yml/badge.svg)  

Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.

## Информация для ревьюера

- Сайт работает по адресу: [http://158.160.113.160/recipes](http://158.160.113.160/recipes)

### Админка

- почта: 123@gmail.ru
- пароль: 123


### Технологии:
- Python
- Django
- Django Rest Framework
- Docker
- Gunicorn
- NGINX
- PostgreSQL
- Yandex Cloud
- Continuous Integratio
- Continuous Deployment


## Подготовка и запуск проекта
### Установка проекта на локальном компьютере
***- Клонируйте репозиторий:***
```
git clone https://github.com/G-Bedy/foodgram-project-react.git
```

***- Для запуска локально, создайте файл `.env` в директории `/infra/` с содержанием:***
```
DEBUG=False
SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
ALLOWED_HOSTS=*,или,ваши,хосты,через,запятые,без,пробелов
CSRF_TRUSTED_ORIGINS=https://<ваш_IP_адрес>
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль_к_базе_данных_на_ваш_выбор
DB_HOST=db
DB_PORT=5432
```
***- Установите и активируйте виртуальное окружение:***
- для Linux
```
python3 -m venv venv
```
- для Windows
```
python3 -m venv venv
source venv/bin/activate
source venv/Scripts/activate
```
- активируйте виртуальное окружение
```
. venv/bin/activate
```

***- Установите зависимости из файла requirements.txt:***
```
pip install -r requirements.txt
```

***- Примените миграции:***
```
python3 manage.py migrate
```
***- Создайте суперюзера:***
```
python3 manage.py createsuperuser
```
***- Dыполните команду для запуска локально:***
```
python3 manage.py runserver
```

### Запуск проекта на сервере

***- Зайдите на сервер***
```
ssh username@server_address  # username - имя пользователя на сервере
                             # server_address - публичный IP сервера
```

***- Установите на сервере Docker, Docker Compose:***
```
sudo apt install curl                                   # установка утилиты для скачивания файлов
curl -fsSL https://get.docker.com -o get-docker.sh      # скачать скрипт для установки
sh get-docker.sh                                        # запуск скрипта
sudo apt-get install docker-compose-plugin              # последняя версия docker compose
```

***- Создайте и откройте файл env:***

```
sudo nano .env
```
***- Заполните файл .env данными:***
```
DEBUG=False
SECRET_KEY=любой_секретный_ключ_на_ваш_выбор
ALLOWED_HOSTS=*,или,ваши,хосты,через,запятые,без,пробелов
CSRF_TRUSTED_ORIGINS=https://158.160.98.138
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль_к_базе_данных_на_ваш_выбор
DB_HOST=db
DB_PORT=5432
```

***- Скопируйте на сервер файлы docker-compose.yml, nginx.conf из папки infra (команды выполнять находясь в папке infra):***
```
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                # IP - публичный IP сервера
```

- ***- Создайте и запустите контейнеры Docker, выполнить команду на сервере:***
```
sudo docker-compose up -d
```

***- После успешной сборки выполните миграции:***
```
sudo docker exec -it foodgram-back python manage.py migrate
```

***- Создайте суперпользователя:***
```
sudo docker exec -it foodgram-back python manage.py createsuperuser
```

***- Соберите статику:***
```
sudo docker exec -it foodgram-back python manage.py collectstatic --noinput
```

***- Наполните базу данных содержимым из файла ingredients.json:***
```
sudo docker exec -it foodgram-back python manage.py load_data 
```
***- После сообщения "Данные загружены" сайт будет доступен по адресу вашего сервера***



***- Для работы с GitHub Actions в репозитории в разделе Secrets > Actions создайте переменные окружения:***
```
SECRET_KEY              # секретный ключ Django проекта
DOCKER_PASSWORD         # пароль от Docker Hub
DOCKER_USERNAME         # логин Docker Hub
HOST                    # публичный IP сервера
USER                    # имя пользователя на сервере
PASSPHRASE              # *если ssh-ключ защищен паролем
SSH_KEY                 # приватный ssh-ключ
TELEGRAM_TO             # ID телеграм-аккаунта для посылки сообщения
TELEGRAM_TOKEN          # токен бота, посылающего сообщение

DB_ENGINE               # django.db.backends.postgresql
DB_NAME                 # postgres
POSTGRES_USER           # postgres
POSTGRES_PASSWORD       # postgres
DB_HOST                 # db
DB_PORT                 # 5432 (порт по умолчанию)
```