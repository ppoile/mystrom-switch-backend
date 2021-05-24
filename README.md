# Mystrom Backend

## Setup

```sh
apt install python3-venv
python3 -m venv venv
. ./venv/bin/activate
pip install --requirement pip-requirements
```

## Run development server

```sh
FLASK_APP=hello.py FLASK_ENV=development flask run --host=0.0.0.0
```

## Host development

```sh
mkdir -p ~/tmp/raspi-fs
sshfs <raspi-ip>: ~/tmp/raspi-fs
```

## Install service mystrom-backend

```sh
sudo ./install.sh
```
