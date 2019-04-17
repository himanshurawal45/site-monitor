# Simple Site Monitor

This program constantly monitors some websites and sends out emails if anything is down.

## Installation Instructions

You need Python3 and pipenv to run this.

```sh
pip3 install pipenv
cd cloned/repo/path

pipenv shell
pipenv install
```

## Running instructions

On line #31, populate the dict like this:

```python
clients = {
    "http://website1.com": "some_email@mail.com",
    "http://website2.com": "some_email@mail.com",
}
```

Add `MONITOR_GMAIL_USERNAME` and `MONITOR_GMAIL_PASSWORD` as environment variables.

Finally:

```shell
python ./monitor.py
```