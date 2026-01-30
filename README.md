Description
-----------

OpenClinic is an easy to use, open source, medical records system.


Requirements
------------

Python 3.10+


Quick start
-----------

```bash
# Install dependencies
$ pip install -e ".[development]"

# Run database migrations
$ python3 manage.py migrate --settings=openclinic.settings.development

# Start development server
$ python3 manage.py runserver --settings=openclinic.settings.development

# Alternative using Makefile
$ make install-all
$ make migrate
$ make dev
```

Contributors
------------

https://github.com/jact/openclinic-in-django/graphs/contributors


License
-------

http://www.gnu.org/licenses/gpl-3.0.en.html
