"""Defines all Dash app callback in one convenient place
"""
from .server import app, dash, dcc, html, base

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dash':
        # Redirects to main devices page
        pass
    elif pathname == '/groups':
        # Redirects to app group charts base
        pass
    elif pathname == '/history':
        # Redirects to app history page
        pass
    elif pathname == '/settings':
        # Redirects to app settings page
        pass
    elif pathname == '/logout':
        # Logout using Auth0
        pass
    else:
        # Redirects to not found page
        return base.blank('404 - Page not Found')

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [
                  dash.dependencies.Input('interval-component', 'n_intervals'),
                  dash.dependencies.Input('url', 'pathname')
              ])
def update_charts(n, pathname):
    # Updates all charts with new Redis data
    if pathname == "/dash" or pathname == "/groups":
        pass

@app.callback(dash.dependencies.Output('main-menu', 'children'),
            [dash.dependencies.Input('url', 'pathname')])
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