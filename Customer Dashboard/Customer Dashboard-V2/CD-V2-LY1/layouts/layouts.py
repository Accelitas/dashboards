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
        [   dcc.Location(id='login-url',pathname='/login', refresh=False),
            html.Br(),
            dbc.Container(
                [
                    dbc.Row(
                              dbc.Col(
                                      html.Img(
                                               src='assets/header.png', 
                                               style = {'height' :'30px', 'width':'200px','float':'right'}
                                              )
                                     )
                           ),

                    html.Br(),

                    html.Br(),

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
                     
                        dbc.Container([
                                        dbc.Row(
                                            dbc.Col(
                                                    
                                                    html.Img(
                                                            src='assets/header.png', 
                                                            style = {'height' :'30px', 
                                                                    'width':'200px',
                                                                    'float':"right"
                                                                    }
                                                            ),
                                                    )       
                                            ),

                                        
                                        dbc.Row(
                                            dbc.Col(
                                                    
                                                     html.Div(f"Welcome! {session.get('user')}.",
                                                               style = {"float":"right",
                                                                        "font-size":"12px",
                                                                       }
                                                              )  
                                                   )       
                                            ),

                                        html.Br(),

                                        html.Br(),

                                        dbc.Row([ 

                                                  dbc.Col(
                                                           dcc.Dropdown(id = "dd0", 
                                                                        options = [{"label": session.get("user"), "value" : session.get("user")}],
                                                                        value = session.get("user")
                                                                        # placeholder = "Customer Name"
                                                                       ),
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
                                                                                display_format='MMMM DD, Y',
                                                                                ), className="dash-bootstrap",
                                                                              
                                                         ),
                                                  dbc.Col(
                                                           dcc.DatePickerSingle(
                                                                                id = "dt2",
                                                                                placeholder = "End Date",
                                                                                display_format='MMMM DD, Y'
                                                                                ),className="dash-bootstrap",
                                                                              
                                                         ),
                                                  dbc.Col(
                                                           dbc.Button("Submit", id = "bb1", color="primary", style = {"width":"100px"}, className="me-2")
                                                         )
                                                   
                                            ], style = {"margin":"0 auto 0 25px"}),

                                        html.Br(),

                                        html.Br(),

                                        dbc.Tabs([ 
                                                   
                                                   dbc.Tab(
                                                             
                                                             dbc.Row(
                                                                      dbc.Col( 
                                                                              dbc.Card(
                                                                                       dcc.Loading(dcc.Graph(id = "fig1")), body=True, className= "shadow-lg p-3 mb-5 bg-white rounded",
                                                                                      )
                                                                              )
                                                                     ), label = " ", labelClassName = "fa fa-bar-chart", label_style={  "font-size" : "20px"}, tab_style={"marginLeft": "auto"}
                                                           ),

                                                   dbc.Tab(
                                                             
                                                             dbc.Row(
                                                                      dbc.Col( 
                                                                              dbc.Card(
                                                                                       dcc.Loading(dcc.Graph(id = "fig2")), body=True, className= "shadow-lg p-3 mb-5 bg-white rounded",
                                                                                      )
                                                                              )
                                                                     ), label = " ", labelClassName = "fa fa-bar-chart", label_style={  "font-size" : "20px"}
                                                           ),

                                                   dbc.Tab(
                                                             
                                                             dbc.Row(
                                                                      dbc.Col( 
                                                                              dbc.Card(
                                                                                       dcc.Loading(dcc.Graph(id = "fig3")), body=True, className= "shadow-lg p-3 mb-5 bg-white rounded",
                                                                                      )
                                                                              )
                                                                     ), label = " ", labelClassName = "fa fa-bar-chart", label_style={  "font-size" : "20px"}
                                                           ),

                                                  dbc.Tab(
                                                             
                                                             dbc.Row(
                                                                      dbc.Col( 
                                                                              dbc.Card(
                                                                                       dcc.Loading(dcc.Graph(id = "fig4")), body=True, className= "shadow-lg p-3 mb-5 bg-white rounded",
                                                                                      )
                                                                              )
                                                                     ), label = " ", labelClassName = "fa fa-pie-chart", label_style={  "font-size" : "20px"}
                                                           ),

                                                  dbc.Tab(
                                                             
                                                             dbc.Row(
                                                                      dbc.Col( 
                                                                              dbc.Card(
                                                                                       dcc.Loading(dcc.Graph(id = "fig5")), body=True, className= "shadow-lg p-3 mb-5 bg-white rounded",
                                                                                      )
                                                                              )
                                                                     ), label = " ", labelClassName = "fa fa-bar-chart", label_style={  "font-size" : "20px"}
                                                           )

                                                
                                                ]),

                                        html.Br(),

                                        dbc.Row(
                                                 dbc.Col(html.Div(
                                                                    dbc.Button('Logout',
                                                                                id='logout-button',
                                                                                color='danger',size='sm',
                                                                                ), style = {"float":"right"}
                                                                 ),
                                                                    width=12,
                                                                    
                                                        )
                            
                                                )

                                    ])
                        
                    ]))

