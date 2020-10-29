

# Edx Commerce

![Backend lang](https://img.shields.io/badge/python-3.8-green)



[Brief video on Youtube](https://www.youtube.com/watch?v=k6wBjlU2R3Q&t=14s "video")

#### Description
This project aims to create an ebay like website where users are able to create auctions, place bids, make comments and have a feature of watchlist auctions.


## Table of content

- [**Getting Started**](#getting-started)
- [Built With](#built-with)
- [License](#license)
- [Motivation](#motivation)

## Getting Started
You can run this application by cloning the repository and running it with python.

### Requirements
- Python
- pipenv
- set your engine database/credentials on mail/settings.py

### Example for a simple local sqlite
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### Install python dependencies. Enter project folder and execute:
```console
pipenv install
```
### Activate python environment
```console
pipenv shell
```

### Migrate models to database
```console
python manage.py makemigrations commerce
python manage.py commerce
```

### Running the django application

```console
python manage.py
```

### Features
- Create auctions
- See active auctions
- See details about an specific auction
- Add auctions to an user's watchlist
- See a page only with the auctions added on user's watchlist
- See a page listing all categories of auctions

### Open the application on the browser, create your user and start using it.
http://localhost:8000/

## Built With

### [Django](https://www.djangoproject.com/ "Django")
A high-level Python Web framework.
### Python
### HTML
### CSS
### [Bootstrap](https://getbootstrap.com/ "Bootstrap")

## License

This project is licensed under the [MIT License](https://github.com/antfons/edx-commerce/blob/main/LICENSE)


## Motivation
I've made this project while learning web development with Python and JavaScript and it's part of EDX HarvardX CS50's Web Programming with Python and JavaScript. [Edx Web Programming](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/ "Edx Web Programming")
