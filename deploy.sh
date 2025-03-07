#!/bin/bash
set -e

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

python manage.py makemigrations --dry-run --check
python manage.py migrate
python manage.py collectstatic --noinput

systemctl reload nginx.service

systemctl restart burger-shop.service


export $(cat /opt/starburger/.env  | grep ROLLBAR_TOKEN | tr -d \')
export $(cat /opt/starburger/.env  | grep ENVIRONMENT)


GIT_REVISION=$(git rev-parse --short HEAD)

curl -H "X-Rollbar-Access-Token: ${ROLLBAR_TOKEN}" -H "Content-Type: application/json" -H 'accept: application/json' -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "${ENVIRONMENT}", "revision": "${GIT_REVISION}", "comment": "deployment", "status": "succeeded"}'

echo "Finished"
