# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from components import base, auth
from flask import send_from_directory
from authlib.flask.client import OAuth
from flask import Flask, redirect
import os

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dash')
oauth = OAuth(app)
#auth_dash = auth.BasicAuth(app)


@app.server.route('/static/<path:path>')
def static_file(path):
    """Serves all static files in /static/ over HTTP
    """
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

def get_styles_by_name(file_format=".css", folder="static"):
    """Loads all file_format that are cointained in the /static/ directory,
    as Dash stylesheets
    """
    paths = []
    folder_path = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(folder_path, folder)
    for file in os.listdir(folder):
        if file.endswith(file_format):
            f = os.path.join(folder, file)
            paths.append(file)
    return paths

def load_core_callbacks():
    from callbacks import core
    import inspect
    # Get all core functions
    all_functions = inspect.getmembers(core)
    for fn in all_functions:
        # Ignore dash callback decorator
        if fn[0] != "dash_callback" and isinstance(fn[1], core.Callback):
            app.callback(fn[1].dash_output, fn[1].dash_inputs)(fn[1])

def load_semantic_ui():
    app.css.append_css({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.3.2/semantic.min.css"})
    app.scripts.append_script({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"})
    app.scripts.append_script({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.3.2/semantic.min.js"})

def start_app():
    # Load semantic ui css
    load_semantic_ui()
    # Gets all .css custom styles for dash
    app_styles = get_styles_by_name(".css")
    for stylesheet in app_styles:
        app.css.append_css({"external_url": "/static/{}".format(stylesheet)})
    # Initiates the base layout for dash
    app.layout = base.main_layout()
    # Load core callbacks
    load_core_callbacks()
    app.run_server(port=3000)

if __name__ == '__main__':
    start_app()
