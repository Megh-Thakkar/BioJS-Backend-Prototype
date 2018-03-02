# BioJS Prototype Backend
This is a prototype backend for BioJS.io, it involves the implementation of some basic features already present as well newer functionality that would ease data management and user experience

# Run the project
## Prerequisites
Clone the repository and create and then activate a virtual environment.
`cd` into the base directory and run:
```
$ pip install -r requirements.txt
```
## Synchronize the database
In the base directory, run:
```
$ python manage.py migrate
```

## Run the back-end
In the same directory, run:
```
$ python manage.py runserver
```

## Run the front-end
Open the following URL in Chromium/Chrome browser:
```
http://127.0.0.1:8000
```

I would like to thank gurayyarar for the AdminBSB Template.  
Enjoy!
