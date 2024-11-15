try:
    import os 
    import sys 
    import json 
    import logging 
    import warnings 
    import contextlib 
    from datetime import datetime, date
    from IPython.display import display 
    from flask import Flask, session
    import dash_bootstrap_components as dbc
    from dash import Dash, html, dcc, Output, Input, State, callback
    from auth.auth import authenticate_user, validate_login_session
except ImportError as error:
    raise Exception(f"{error}") from None 

def login_layout():
    return html.Div(
        [
            dcc.Location(id='login-url',pathname='/login', refresh=False),
            html.Br(),
            dbc.Container(
                [
                    dbc.Row(
                              dbc.Col(
                                      html.Img(
                                               src='assets/Accelitas Circle Logo.webp', 
                                               style = {'height' :'50px', 'width':'50px','margin-left':'95%'}
                                              )
                                     )
                           ),
                    
                    dbc.Row(
                              dbc.Col(
                            
                                        dbc.Card(
                                                    [   
                                                        
                                                        html.Br(),
                                                        html.H5('Accelitas Login',className='card-title'),
                                                        html.Br(),
                                                        dbc.Input(id='login-email',placeholder='Enter User'),
                                                        html.Br(),
                                                        dbc.Input(id='login-password',placeholder='Assigned password',type='password'),
                                                        html.Br(),
                                                        dbc.Button('Submit',id='login-button',color='success'),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Div(id='login-alert')
                                                    ],
                                                    body=True, className= "shadow-lg p-3 mb-5 bg-white rounded",style = {"margin-top": "15%"}
                                                ),
                            width=5
                          ),
                        justify='center'
                    )
                ]
            )
        ]
    )


@validate_login_session
def app_layout():
    return ( html.Div([   
        
                        dcc.Location(id='home-url',pathname='/home'),
                        
                        html.Br(),
                        
                        dbc.Row(
                            dbc.Col(
                                    html.Img(
                                                src='assets/Accelitas Circle Logo.webp', 
                                                style = {'height' :'50px', 'width':'50px','margin-left':'95%'},
                                               
                                            )
                                )       
                            ),

                        html.Br(),

                        html.Br(),

                        html.Br(),

                        html.Br(),

                        dbc.Row([ 

                                    dbc.Col(
                                            dcc.Dropdown(id = "dd0", 
                                                        options = [{"label": session.get("user"), "value" : session.get("user")}],
                                                        placeholder = "Customer Name"),
                                            style = {"font-size" : "0.75rem"}
                                            
                                            ), 
                                    dbc.Col(
                                            
                                            dcc.Dropdown(id = "dd1",
                                            placeholder = "Customer DBA"),   
                                            style = {"font-size" : "0.75rem"}
                                                        
                                            ),
                                    dbc.Col(
                                            dcc.Dropdown(id = "dd2",
                                            placeholder = "Accelitas Services"),
                                            style = {"font-size" : "0.75rem"}
                                            
                                            ),
                                    dbc.Col(
                                            dcc.DatePickerSingle(
                                                                id = "dt1",
                                                                placeholder = "Start Date",
                                                                display_format='MMMM Y, DD',
                                                                ), className="dash-bootstrap",
                                                                
                                            ),
                                    dbc.Col(
                                            dcc.DatePickerSingle(
                                                                id = "dt2",
                                                                placeholder = "End Date",
                                                                display_format='MMMM Y, DD'
                                                                ), style = {"margin-left": "0"},className="dash-bootstrap",
                                                                
                                            ),
                                    dbc.Col(
                                            dbc.Button("Submit", id = "bb1", color="primary", style = {"width":"100px", "margin-left" : "0"}, className="me-2")
                                            )
                                    
                            ], style = {"margin-left":"90px"}),

                        html.Br(),

                        html.Br(),

                        dbc.Row(
                                    dbc.Col( 
                                             dcc.Loading(dcc.Graph(id = "fig1", style = {"border-style":"groove"})), style = {"padding-left":"0px", "padding-right":"0px"}
                                           ), style = {"margin-left" : "10px", "margin-right" : "10px"}
                               ),
                                
                        dbc.Row([
                                    dbc.Col( 
                                            dcc.Loading(dcc.Graph(id = "fig2", style = {"border-style":"groove"})), width = 6, style = {"padding-left":"0px", "padding-right":"0px"}
                                            ),
                                    
                                    dbc.Col( 
                                            dcc.Loading(dcc.Graph(id = "fig3", style = {"border-style":"groove"})), width = 6, style = {"padding-left":"0px", "padding-right":"0px"}
                                                        )
                                            
                                ], style = {"margin-left" : "10px", "margin-right" : "10px"}
                               ),

                                                
                        dbc.Row([
                                    dbc.Col( 
                                            dcc.Loading(dcc.Graph(id = "fig4", style = {"border-style":"groove"})) ,width = 4, style = {"padding-left":"0px", "padding-right":"0px"}
                                           ),

                                    dbc.Col( 
                                            dcc.Loading(dcc.Graph(id = "fig5", style = {"border-style":"groove"})),width = 8, style = {"padding-left":"0px", "padding-right":"0px"}
                                                            
                                            )
                                            
                               ], style = {"margin-left" : "10px", "margin-right" : "10px"}
                               ),
                                            

                        html.Br(),

                        dbc.Row(
                                    dbc.Col(
                                            dbc.Button('Logout',id='logout-button',color='danger',size='sm'),
                                                        width=4, style = {"margin-left" : "93%"}
                                        )
            
                                    )

                                    
                        
                    ]))

