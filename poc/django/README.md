# Web development with Python and Django

## Setup

* Install django
`pip install django`

* Check the version of django installed
`python3 -m django --version`

* Create a web project
`django-admin startproject djangopoc`

## Collect all static files (css, js ...)

* `cd djangopoc`
* `python3 manage.py collectstatic`


## Start the web server

`python3 manage.py runserver`

## Launch the web page

Click on the development server url in `runserver` output

## Create a web-site

* Start an app (A project can have any number of apps)
`python3 manage.py startapp djangoapp1`

* Create HTTP Response object in `view.py` (Under the app directory)

* Create `urls.py` file in app directory

* Map functions in `views.py` to `urls.py` (Under the app directory)

* Map the urls in `djangoapp1` to urls of `djangopoc` project

## Write HTML code

* Create directory within app directory called`templates`

* Create a directory within `templates` with the same name as app (`djangoapp1`)

* Create the HTML file inside this directory

## Link the HTML page to the web-site

* Open `apps.py` under `djangoapp1` app directory

* Copy the class name `Djangoapp1Config`

* Open `settings.py` under `djangopoc` project directory

* Add the created app in `settings.py` - in INSTALLED_APPS section add `djangoapp1.app.Djangoapp1Config'`

* Navigate to `views.py`, use render function instead of HTTPResponse
