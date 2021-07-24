import random

import eel

eel.init('web')                     # Give folder containing web files

@eel.expose
def py_random():
    return random.random()

@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

def say_hello_jinja(x):
    print('Hello from %s' % x)
    return ""

eel.start('templates/hello.html', size=(300, 200), jinja_templates='templates', jinja_global={"say_hello_jinja": say_hello_jinja})    # Start
