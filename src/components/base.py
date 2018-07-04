import dash_core_components as dcc
import dash_html_components as html


def base_search():
    return html.Div([
        dcc.Input(id='base-search-input', type='text', placeholder="Search..."),
        html.I(
            className='search link icon',
            id='base-search-button'
        )
    ], className='ui transparent icon input')

def base_card(inner_elems=[]):
    return html.Div(
        [html.Div(inner, className="card") for inner in inner_elems],
        className="ui four stackable cards"
        )

def chart_page(inner_elems=[]):
    return html.Div(
        [html.Div(base_card([inner]), className="column") for inner in inner_elems],
        className="ui two column stackable grid container"
        )


def active_menu(logo_src="/static/logo.png", active_button="dash"):
    compare_route = lambda x,y: "active item" if x == y else "item"
    return [
            html.Div(
                [html.Img(src=logo_src, className="ui mini image")],
                className="item"
            ),
            dcc.Link("Dashboard", href="/dash", className=compare_route(active_button, "dash")),
            dcc.Link("Groups", href="/groups", className=compare_route(active_button, "groups")),
            dcc.Link("History", href="/history", className=compare_route(active_button, "history")),
            html.Div(
                [
                    html.Div([base_search()], className="item"),
                    dcc.Link('Settings', href="/settings", className=compare_route(active_button, "settings")),
                    dcc.Link('Logout', href="/logout", className="item")
                ],
                className="right menu"
            )
        ]
def main_menu(logo_src="/static/logo.png"):
    return html.Div(
        active_menu(logo_src),
        id="main-menu",
        className="ui top fixed pointing menu"
    )

def blank(msg):
    return html.Div([
        html.H2(msg, className="ui center aligned header")
    ])

def main_layout():
    return html.Div(
        [
            # Page URL location
            dcc.Location(id='url', refresh=False),
            # Main user menu
            main_menu(),
            # Page content - whatever it is
            html.Div(id='page-content'),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
        ]
    )