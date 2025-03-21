# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить dev-версию сайта

Для запуска сайта нужно запустить **одновременно** бэкенд и фронтенд, в двух терминалах.

### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/devmanorg/star-burger.git
```

Перейдите в каталог проекта:
```sh
cd star-burger
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Определите переменную окружения `SECRET_KEY`. Создать файл `.env` в каталоге `star_burger/` и положите туда такой код:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Если вы увидели пустую белую страницу, то не пугайтесь, выдохните. Просто фронтенд пока ещё не собран. Переходите к следующему разделу README.

### Собрать фронтенд

**Откройте новый терминал**. Для работы сайта в dev-режиме необходима одновременная работа сразу двух программ `runserver` и `parcel`. Каждая требует себе отдельного терминала. Чтобы не выключать `runserver` откройте для фронтенда новый терминал и все нижеследующие инструкции выполняйте там.

[Установите Node.js](https://nodejs.org/en/), если у вас его ещё нет.

Проверьте, что Node.js и его пакетный менеджер корректно установлены. Если всё исправно, то терминал выведет их версии:

```sh
nodejs --version
# v16.16.0
# Если ошибка, попробуйте node:
node --version
# v16.16.0

npm --version
# 8.11.0
```

Версия `nodejs` должна быть не младше `10.0` и не старше `16.16`. Лучше ставьте `16.16.0`, её мы тестировали. Версия `npm` не важна. Как обновить Node.js читайте в статье: [How to Update Node.js](https://phoenixnap.com/kb/update-node-js-version).

Перейдите в каталог проекта и установите пакеты Node.js:

```sh
cd star-burger
npm ci --dev
```

Команда `npm ci` создаст каталог `node_modules` и установит туда пакеты Node.js. Получится аналог виртуального окружения как для Python, но для Node.js.

Помимо прочего будет установлен [Parcel](https://parceljs.org/) — это упаковщик веб-приложений, похожий на [Webpack](https://webpack.js.org/). В отличии от Webpack он прост в использовании и совсем не требует настроек.

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Если вы на Windows, то вам нужна та же команда, только с другими слешами в путях:

```sh
.\node_modules\.bin\parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```

Дождитесь завершения первичной сборки. Это вполне может занять 10 и более секунд. О готовности вы узнаете по сообщению в консоли:

```
✨  Built in 10.89s
```

Parcel будет следить за файлами в каталоге `bundles-src`. Сначала он прочитает содержимое `index.js` и узнает какие другие файлы он импортирует. Затем Parcel перейдёт в каждый из этих подключенных файлов и узнает что импортируют они. И так далее, пока не закончатся файлы. В итоге Parcel получит полный список зависимостей. Дальше он соберёт все эти сотни мелких файлов в большие бандлы `bundles/index.js` и `bundles/index.css`. Они полностью самодостаточны, и потому пригодны для запуска в браузере. Именно эти бандлы сервер отправит клиенту.

Теперь если зайти на страницу  [http://127.0.0.1:8000/](http://127.0.0.1:8000/), то вместо пустой страницы вы увидите:

![](https://dvmn.org/filer/canonical/1594651900/687/)

Каталог `bundles` в репозитории особенный — туда Parcel складывает результаты своей работы. Эта директория предназначена исключительно для результатов сборки фронтенда и потому исключёна из репозитория с помощью `.gitignore`.

**Сбросьте кэш браузера <kbd>Ctrl-F5</kbd>.** Браузер при любой возможности старается кэшировать файлы статики: CSS, картинки и js-код. Порой это приводит к странному поведению сайта, когда код уже давно изменился, но браузер этого не замечает и продолжает использовать старую закэшированную версию. В норме Parcel решает эту проблему самостоятельно. Он следит за пересборкой фронтенда и предупреждает JS-код в браузере о необходимости подтянуть свежий код. Но если вдруг что-то у вас идёт не так, то начните ремонт со сброса браузерного кэша, жмите <kbd>Ctrl-F5</kbd>.


## Как запустить prod-версию сайта

Для запуска prod-версии скопируйте код на сервер (лучше использовать каталог /opt/. а также создать виртуальное окружение аналогичным образом, как указано для dev-версии. [Результат реализации запуска prod-версии](https://microsq.store/)

### Установите Postgres
Рекомендуется использовать Postgres при деплое проекта. Вы можете скачать его с [официального сайта](https://www.psycopg.org).
Пример настройки базы данных можно посмотреть [здесь](https://help.reg.ru/support/servery-vps/oblachnyye-servery/ustanovka-programmnogo-obespecheniya/rukovodstvo-po-postgresql#1).


Помимо этого потребуется создать файл `.env` в каталоге `star_burger/` со следующими настройками бэкэнда:

- `DEBUG` — дебаг-режим. Поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `YANDEX_API_KEY` — [API ключ Яндекс-геокодера](https://dvmn.org/encyclopedia/api-docs/yandex-geocoder-api/)
- `ROLLBAR_TOKEN` - ключ от сервиса [Rollbar](https://rollbar.com)
- `ENVIRONMENT` - название окружения в [Rollbar](https://rollbar.com)
- DATABASE_URL= 'настройки базы данных Postgres вида 'postgresql://USER:PASSWORD@HOSTt:/NAME' ' ([ о том, как их настроить в .env](https://github.com/jazzband/dj-database-url#url-schema))

### Установите Gunicorn
pip install gunicorn
Cоздайте файл /etc/systemd/system/burger-shop.service вида
```
[Unit]
Description=burger_shop
After=postgresql.service
Requires=postgresql.service

[Service]
Type=simple
WorkingDirectory=/opt/starburger/
ExecStart=/opt/starburger/PRG/bin/gunicorn -w 3 -b 127.0.0.1:8080 star_burger.wsgi
Restart=always
                                                            
[Install]
WantedBy=multi-user.target
```
### Установите NGINX
```                                                                                                                                                             
apt install nginx
```
Создайте файл /etc/nginx/sites-enabled/star-burger вида
```
server {
    listen 80 default;
    location / {
        include '/etc/nginx/proxy_params';
        proxy_pass http://217.12.37.183:8000/;  # ! Замените адрес на свой
    }
    location /media/ {
        alias /opt/starburger/media/;# ! Заменить путь к media на свой
    }
    location /staticfiles/ {
        alias /opt/starburger/staticfiles/;# ! Заменить путь к static на свой
    }

}
```
Для запуска/перезапуска/остановки и т.д. серверов следует пользоваться [набором команд](https://4te.me/post/shpargalka-systemd/).
Этот же набор команд пригодится при создании дополнительных файлов сервиса и таймеров (см. далее).

### Создайте дополнительные файлы
В каталоге `/etc/systemd/system/` создайте дополнительные файлы:
#### Сервис для обновления сертификатов
файл `certbot-renewal.service`(пример)
```
[Unit]
Description=Certbot Renewal

[Service]
ExecStart=/usr/bin/certbot renew --force-renewal --post-hook "systemctl reload nginx.service"
```

Для автоматизации обновления сертификатов создайте файл `certbot-renewal.timer`(пример)
```
[Unit]
Description=Timer for Certbot Renewal

[Timer]
OnBootSec=300
OnUnitActiveSec=1w

[Install]
WantedBy=multi-user.target
```
#### Сервис для удаления устаревших сессий clearsessions.service
```
[Unit]
Description=clearsessions

[Service]
Type=simple
WorkingDirectory=/opt/starburger/
ExecStart=/opt/starburger/PRG/bin/python3 manage.py clearsessions

Restart=on-abort

[Install]
WantedBy=multi-user.target
```

И соотвествующий таймер clearsessions.timer
```
[Unit]
Description=Timer for Clearsessions

[Timer]
OnCalendar=weekly
Persistent=true
AccuracySec=30s

[Install]
WantedBy=multi-user.target
```
Для создания файлов сервиса и работы с ними можно прочитать материалы [здесь](https://dvmn.org/encyclopedia/deploy/systemd/) и [здесь](https://dvmn.org/encyclopedia/deploy/renewing-certbot-certificates-for-nginx-using-a-systemd-timer/)
### Автоматизация проекта
В каталоге с проектом находится баш-скрипт `deploy.sh`. Его выполнение позволит обновить проект с git-хаба, установить зависимости, осуществить миграции базы данных, собрать статику, перезапустить сервера nginx и gunicorn.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
