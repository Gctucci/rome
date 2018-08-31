"""Defines all Dash app callback in one convenient place
"""
from components import base
import dash
import dash_core_components as dcc
import dash_html_components as html

class Callback(object):

    def __init__(self, func, inputs, output):
        self.func = func
        self.inputs = inputs
        self.output = output

    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        return result
    @property
    def dash_inputs(self):
        return [dash.dependencies.Input(*inpt) for inpt in self.inputs]
    @property
    def dash_output(self):
        return dash.dependencies.Output(*self.output)

def dash_callback(inputs, output):
    def decorator(func):
        return Callback(func, inputs, output)
    return decorator

@dash_callback([('url', 'pathname')], ('main-menu', 'children'))
def update_menu(pathname):
    """Updates button as active/non active based on user URL changes
    """
    if pathname == '/dash':
        return base.active_menu(active_button="dash")
    elif pathname == '/groups':
        return base.active_menu(active_button="groups")
    elif pathname == '/history':
        return base.active_menu(active_button="history")
    elif pathname == '/settings':
        return base.active_menu(active_button="settings")
    else:
        return base.active_menu()