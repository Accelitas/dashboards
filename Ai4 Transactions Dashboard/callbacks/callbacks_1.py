#!/usr/bin/python
#-*-coding:utf-8-*-

try:
    from dash import Output, Input, State
    from callbacks_manager import CallbackManager
    from layouts import login_layout, app_layout
except ImportError as error:
    raise Exception(f"{error}") from None

callback_manager_1 = CallbackManager()

@callback_manager_1.callback(Output('page-content','children'),[Input('url','pathname')])
def router(url):
    if url=='/home':
        return app_layout()
    elif url=='/login':
        return login_layout()
    else:
        return login_layout()