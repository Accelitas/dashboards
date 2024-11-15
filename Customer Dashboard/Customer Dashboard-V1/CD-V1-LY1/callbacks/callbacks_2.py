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


callback_manager_2 = CallbackManager()


@callback_manager_2.callback(
    [Output('url','pathname'),
     Output('login-alert','children')],
    [Input('login-button','n_clicks')],
    [State('login-email','value'),
     State('login-password','value')])
def login_auth(n_clicks,email,pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None or n_clicks==0:
        return no_update,no_update
    credentials = {'user':email,"password":pw}
    authed, user = authenticate_user(credentials)
    if authed is True:
        session["authed"] = True
        session['user'] = user
        return '/home',''
    return no_update,dbc.Alert('Incorrect credentials.',color='danger',dismissable=True)