# smarttv_manager
Django project for managing smart TV content.

Create a virtualenv (see <http://www.jeffknupp.com/blog/2013/12/18/starting-a-django-16-project-the-right-way/>)

and run ```pip install -r requirements.txt```

If this errors out:

Windows users will need to first install Visual C++ tools for Python27:

<https://www.microsoft.com/en-us/download/details.aspx?id=44266>

If this fails, first run ```pip install --install-option="--without-c-extensions" rjsmin```
and ```pip install --install-option="--without-c-extensions" rcssmin```,
followed by ```pip install -r requirements.txt```

Next, run ```python manage.py migrate``` and ```python manage.py createsuperuser``` to create the database.  
Now, run the project using ```python manage.py runserver 8000``` to start the project on port 8000.

Wagtail will be at <http://localhost:8000/cms/>.
