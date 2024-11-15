#!/usr/bin/python
#-*- coding:utf-8 -*-

try: 
    import os
    
    import pyodbc
    import pandas as pd
    
    from flask import session
    from functools import wraps
    from database import connection_string_2
    from dotenv import load_dotenv, find_dotenv

    import dash_bootstrap_components as dbc
    from dash import Dash, html, dcc, Output, Input, State, callback
except ImportError as error:
    raise Exception(f"{error}") from None


def authenticate_user(credentials):

    
    authed = (credentials["user"] == "Dan") and (credentials["password"] == "Dan")

    return authed
   
def validate_login_session(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        if session.get('authed',None)==True:
            return f(*args,**kwargs)
        return html.Div(
                         html.Div([
                                   html.Br(),
                                   dbc.Container([
                                                   dbc.Row(
                                                   dbc.Col(
                                                           html.Img(
                                                                    src='assets/header.png', 
                                                                    style = {'height' :'30px', 
                                                                             'width':'200px',
                                                                             'float':"right"
                                                                            }
                                                                    )
                                                          )
                                                          ),

                                                   dbc.Row(
                                                           dbc.Col(
                                                                   [
                                                                    dbc.Card(
                                                                             [
                                                                              html.H2('401 - Unauthorized',className='card-title'),
                                                                              html.Br(),
                                                                              html.A(dcc.Link('Login',href='/login'))
                                                                             ],
                                                                              body=True, className= "shadow-lg p-3 mb-5 bg-white rounded"
                                                                             )
                                                                    ],
                                                                     width=5
                                                                    ),
                                                                    justify='center', style = {"margin-top" : "15%"})
                                                    ])
                                  ])
                         )
    return wrapper