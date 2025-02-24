#!/bin/bash
set -e
set -x

cd /opt/starburger
git pull
if [ -e "PRG/bin/activate" ]; then
    echo "activating venv"
    source PRG/bin/activate
else
    echo "Creating venv..."
    python -m venv PRG
    source PRG/bin/activate
fi

pip install -r requirements.txt
npm ci --dev

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

systemctl reload nginx.service

systemctl restart burger-shop.service

echo "Finished"