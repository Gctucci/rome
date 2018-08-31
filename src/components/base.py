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


def chart_page(inner_elems=[]):
    return html.Div(
        [html.Div(inner, className="card") for inner in inner_elems],
        className="ui four stackable cards"
        )

def dev_stats(num_offline=0, num_online=0):
    return html.Div([
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div([html.I(className="battery full green icon")], className="ui circular inline image"),
                                num_online
                            ],
                            className="value"),
                        html.Div("Online Devices", className="label")
                    ],
                    className="statistic"
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div([html.I(className="battery empty red icon")], className="ui circular inline image"),
                                num_offline
                            ],
                            className="value"),
                        html.Div("Offline Devices", className="label")
                    ],
                    className="statistic"
                )
            ],
            className="ui statistics"
        )
    ], className="ui center aligned")

def org_header():
    #TODO: Create env variable to hold Organization Name
    return html.H2("TESTING", className="ui center aligned header")

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
        className="ui top pointing menu"
    )

def main_layout():
    return html.Div(
        [
            # Page URL location
            dcc.Location(id='url', refresh=False),
            # Main user menu
            main_menu(),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    # Show org header
                                    org_header(),
                                    # Show device statistics
                                    html.Div([dev_stats()], className="ui ten column centered grid"),
                                    html.Div(className="spacer"),
                                    # Page content - whatever it is
                                    html.Div(
                                        [
                                            html.Div(
                                                chart_page(["bla" for i in range(9)]),
                                                className="ten wide column")
                                        ],
                                        className="ui ten column centered grid",
                                        id='page-content'),
                                ]
                                ,
                                className="column"
                            )
                        ],
                        className="row"
                    )
                ],
                className="ui fluid grid"
            ),
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds
                n_intervals=0
            )
        ],
        className="ui stackable fluid container"
    )