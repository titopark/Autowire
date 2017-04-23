Autowire
========

Autowire is light & simple dependency injection library for Python.

You can use dependency injection & resource management without any classes and any magics.

Since python already support nice context manager ([PEP343](https://www.python.org/dev/peps/pep-0343/)),
we don't have to any extra interfaces for setting-up & tearing-down resource.


Requirements
------------

Python 3+ (Tested in Python3.6)


Basic Resource Management
-------------------------


``` python
from contextlib import contextmanager

from autowire import Context, Resource

hello = Resource('hello', __name__)

@hello.impl
@contextmanager
def with_hello_message(context):
    print("Setup hello message")
    try:
        yield "Hello, World!"
    finally:
        print("Teardown hello message")

context = Context()

with context.resolve(hello) as message:
    print(message)

# Output:
# Setup hello message
# Hello, World!
# Teardown hello message

```

The parameter of `impl` can be any function that takes `Context` as parameter 
and returns `ContextManager`. (`(Context) -> ContextManager`)


Basic Dependency Inejection
---------------------------

``` python
number = Resource('number', __name__)
double = Resource('double', __name__)

@double.autowired(number)
@contextlib.contextmanager
def get_double(number):
    yield number * 2

context = Context()

# You can provide resource only in specfic context
@context.provide(number)
@contextlib.contextmanager
def get_one(context):
    yield 1

with context.resolve(double) as value:
    print(value)
    # Output: 2

another_context = Context()

# Since another_context doesn't provide number resource,
# It raises ResourceNotProvidedError
with another_context.resolve(double) as value:
    pass

```

Use cases
---------

For instance, if want to run your application in multiple environment
like development / production, You can change configuration by providing
different values to each contexts.

Suppose that we have resources like that.

``` python
# in resources.py
import contextlib
from autowire import Resource

from db_engine import DatabaseEngine

env = Resource('env', __name__)
db_config = Resource('db_config', __name__)
db_connection = Resource('db_connection', __name__)

@db_config.from_func(env)
def get_db_config(env):
    path = os.path.join('path/to/config', env, 'db.json')
    with open(path) as f:
        config = json.load(f)
    return config

@db_connection.autowired(db_config)
@contextlib.contextmanager
def open_db_connection(db_config):
    conn = DatabaseEngine(db_config['HOST'], db_config['PORT'])
    try:
        yield conn
    finally:
        conn.close()

```

We can change running environment by providing `env` resource

``` python
# app.py
import os
from autowire import Context

from .resources import env, db_connection

def run(db_connection):
    ...

app_context = Context()

@app_context.provide_from_func(env)
def get_env():
    # Get env from envvar
    return os.environ['APP_ENV']

# APP_ENV will be injected to env resource.
with app_context.resolve(db_connection) as conn:
    run(conn)

```


Run Test
--------

``` bash
$ python setup.py test
```
