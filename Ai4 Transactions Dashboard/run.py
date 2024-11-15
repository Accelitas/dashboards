#!/usr/bin/python
#-*- coding:utf-8 -*-

from __future__ import (
                        absolute_import
                       )
try:
    import dash_bootstrap_components as dbc
    from dash import (
                      Dash, 
                      Output, 
                      Input, 
                      State, 
                      dcc, 
                      html, 
                      callback, 
                      no_update
                     )

    from auth import authenticate_user
    from layouts import login_layout, app_layout
    from callbacks import (
                           callback_manager_1, 
                           callback_manager_2, 
                           callback_manager_3, 
                           callback_manager_4, 
                           callback_manager_5,
                           callback_manager_6,
                           callback_manager_7,
                           callback_manager_8,
                           callback_manager_9,
                           callback_manager_10
                          )

    from werkzeug.serving import run_simple 
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    from flask import Flask, redirect, session, copy_current_request_context

except ImportError as error:
    raise Exception(f"{error}") from None 


server = Flask(__name__)

app = Dash(__name__, 
           url_base_pathname="/", 
           external_stylesheets=[
                                  dbc.themes.BOOTSTRAP, 
                                  "https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/css/bootstrap.min.css",
                                  "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
                                ]
          )

app.config.suppress_callback_exceptions = True

app.title = 'Accelitas Customer Dashboard'

app.css.config.serve_locally = True

server = app.server

server.config['SECRET_KEY'] = 'k1LUZ1fZShowB6opoyUIEJkJvS8RBF6MMgmNcDGNmgGYr' 

callback_manager_1.attach_to_app(app)

callback_manager_2.attach_to_app(app)

callback_manager_3.attach_to_app(app)

callback_manager_4.attach_to_app(app)

callback_manager_5.attach_to_app(app)

callback_manager_6.attach_to_app(app)

callback_manager_7.attach_to_app(app)

callback_manager_8.attach_to_app(app)

callback_manager_9.attach_to_app(app)

callback_manager_10.attach_to_app(app)

@server.route('/')
def render_dashboard():
    return redirect("/dash1")

application = DispatcherMiddleware(server, { "/dash1" : app.server})

app.layout = html.Div(
                      [
                       dcc.Location(id='url',refresh=False),
                       html.Div(
                                login_layout(),
                                id='page-content'
                               ),
                       ]
                      )

if __name__ == "__main__":
    run_simple('0.0.0.0', 
               8080, 
               application, 
               use_reloader = False, 
               use_debugger = False)