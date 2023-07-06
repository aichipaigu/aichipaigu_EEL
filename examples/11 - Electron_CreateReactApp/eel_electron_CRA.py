"""Main Python application file for the EEL-CRA demo."""

import os
import platform
import random
import sys

import eel
# import threading
# from server_utils import is_port_in_use, start_server
from server_utils import MyServer
from resource_path import resource_path

# Use latest version of Eel from parent directory
sys.path.insert(1, '../../')


@eel.expose
def quit_app():
    """Quit the app."""
    print('Exiting python app') 
    os._exit(0)


@eel.expose  # Expose function to JavaScript
def say_hello_py(x):
    """Print message from JavaScript on app initialization, then call a JS function."""
    print('Hello from %s' % x) 
    eel.say_hello_js('Python {from within say_hello_py()}!')


@eel.expose
def expand_user(folder):
    """Return the full path to display in the UI."""
    return '{}/*'.format(os.path.expanduser(folder))


@eel.expose
def pick_file(folder):
    """Return a random file from the specified folder."""
    folder = os.path.expanduser(folder)
    if os.path.isdir(folder):
        listFiles = [_f for _f in os.listdir(folder) if not os.path.isdir(os.path.join(folder, _f))]
        if len(listFiles) == 0:
            return 'No Files found in {}'.format(folder)
        return random.choice(listFiles)
    else:
        return '{} is not a valid folder'.format(folder)


def start_eel(develop):
    """Start Eel with either production or development configuration."""
    global server  # Declare that we are using the global variable 'server'

    if develop:
        directory = 'src'
        page = {'port': 3000}
        mainJS_path = '.'
        os.environ['BROWSER'] = 'none'
        os.environ['ELECTRON_START_URL'] = 'http://localhost:3000'
    else:
        directory = 'build'
        page = 'index.html'
        mainJS_path = 'build/electron/main.js' # Use this if you don't want to use package.json app data inside of build
        # mainJS_path = 'build' # Use this if you want to use package.json app data inside of build   (run the `clean_json.py` file before building Eel, and include   --add-data 'build/package.json:build'   on build command )

    eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])

    # These will be queued until the first connection is made, but won't be repeated on a page reload
    say_hello_py('Python World!')
    eel.say_hello_js('Python World!')   # Call a JavaScript function (must be after `eel.init()`)

    # eel.show_log('https://github.com/samuelhwilliams/Eel/issues/363 (show_log)')

    eel_kwargs = dict(
        host='localhost',
        port=8080,
        size=(1280, 800),
    )

    ELECTRON_PORT = 8000
    react_build_path = "./build"
    server_url = "http://localhost:8000"

    cmd = [resource_path('Electron.app/Contents/MacOS/Electron'), resource_path(mainJS_path)]
    if not develop:
        cmd +=  "--start-url", server_url
        
    try:
        if not (develop):  # If in production mode, start local server for Electron/React
            server = MyServer()
            if not server.is_port_in_use(ELECTRON_PORT):
                server.start(react_build_path, ELECTRON_PORT)
        eel.start(page, mode='custom', cmdline_args=cmd, **eel_kwargs)
    except Exception as e:
        raise


if __name__ == '__main__':
    import sys

    # Pass any second argument to enable debugging
    start_eel(develop=len(sys.argv) == 2)
