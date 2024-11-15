#!/usr/bin/python
#-*-coding:utf-8-*-

try:
    from flask import Flask, session
    import dash_bootstrap_components as dbc
    from auth.auth import authenticate_user
    from layouts import login_layout, app_layout
    from callbacks_manager import CallbackManager
    from dash import Output, Input, State, no_update    
except ImportError as error:
    raise Exception(f"{error}") from None


callback_manager_3 = CallbackManager()


@callback_manager_3.callback(
    Output('home-url','pathname'),
    [Input('logout-button','n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None or n_clicks==0:
        return no_update
    session['authed'] = False
    session.pop('user')
    return '/login'