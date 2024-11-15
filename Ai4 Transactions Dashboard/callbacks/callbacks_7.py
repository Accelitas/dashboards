#!/usr/bin/python
#-*-coding:utf-8-*-

try:
      import pyodbc
      import pandas as pd
      import numpy as np
      from flask import session
      import plotly.graph_objects as go 
      from database import connection_string_1
      from callbacks_manager import CallbackManager
      from dash import Output, Input, State, no_update  
except ImportError as error:
      raise Exception(f"{error}") from None

pd.set_option('future.no_silent_downcasting', True)

callback_manager_7 = CallbackManager()

@callback_manager_7.callback(Output("fig2", "figure"), [Input("bb1", "n_clicks")], [
                                                                                    
                                                                                    State("dd0", "value"),
                                                                                    State("dd1", "value"),
                                                                                    State("dd2", "value"),
                                                                                    State("dt1", "date"),
                                                                                    State("dt2", "date")
                                                                                  ])
def populate_figure_2(n_clicks, name, dba, svr, sdate, edate):
      
      if n_clicks is not None and n_clicks > 0:

        with pyodbc.connect(connection_string_1) as connect:

                with connect.cursor() as cursor:

                    cursor.execute("""
                                    
                                        SELECT 
                                                *
                                        FROM 
                                            transactions   
                                        WHERE 
                                            customer_name = COALESCE(NULLIF(?, ''), customer_name)
                                            AND customer_dba = COALESCE(NULLIF(?, ''), customer_dba)
                                            AND service = COALESCE(NULLIF(?, ''), service)
                                            AND date BETWEEN ? AND ?
                                            AND credential_type = 'production'
                                            AND platform_origin = 'Ai4'
                
                                        
                                """, (name, dba, svr, sdate, edate)              
                                        
                                
                                )
                    
                    df0 = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

                    df0.drop_duplicates(subset = ["transaction_id"])

                    service_columns = {
                                    "Ai Lift" : ["signal_2", "signal_1", "signal"],
                                    "AI Verify BD+" : ["signal_2", "signal_1", "signal"],
                                    "Ai Validate BAV FCRA" : ["signal_2", "signal_1", "signal"],
                                    "Ai Validate BAV" : ["signal_2", "signal_1", "signal"],
                                    "Ai Validate BD" :["score_act","score_acct"],
                                    "AI Verify BD" : ["score_act","score_acct"],
                                    "Ai Screen Conversion" : ["score_conv", "score_acct"],
                                    "Ai Screen FPD + Conversion" : ["score_fpd", "score_conv", "score_acct"],
                                    "Ai Screen FPD" :["score_fpd", "score_acct"]

                                  }

                    if svr in service_columns:

                        df1 = df0.loc[df0["service"] == svr, service_columns[svr]]

                        df1["first_non_null"] = df1.apply(lambda x : next((val for val in x if pd.notna(val)), None), axis = 1)

                        # display(df1)

                        # bins = range(-1, 1010, 50)

                        # labels = [f'{a} - {b-1}' for a, b in zip(bins, bins[1:])]

                        bins = [-1] + list(range(0, 1050, 50))

                        labels = ['-1'] + [f'{a}-{b-1}' for a, b in zip(bins[1:-1], bins[2:-1])] + ['950-1000']

                        df2 = pd.DataFrame(pd.cut(df1['first_non_null'], 
                                        bins=bins, 
                                        right=False, 
                                        labels=labels).value_counts(normalize=True).mul(100).round(0).sort_index()).reset_index()
                        
                        df2["proportion"] = df2["proportion"].astype(int)
                    
                        # display(df2)

                        annot_1 = [dict(
                                    x=xi,
                                    y=yi,
                                    text= f"{str(yi)}%",
                                    xanchor='center',
                                    yanchor='bottom',
                                    showarrow=False,
                                    font=dict(
                                            size = 10,
                                            color="#1f77b4"
                                            ),
                                    ) for xi, yi in zip(df2["first_non_null"],df2["proportion"])]


                        return {
                                 
                                  "data" : [
                                             go.Bar(
                                                     x = df2["first_non_null"],
                                                     y = df2["proportion"]
                                                   )
                                           ],

                                  "layout" : go.Layout(
                                                        title = dict(
                                                                      text = "<b>Score Distribution</b>",
                                                                      x = 0.5,
                                                                      y = 0.95
                                                                    ),
                                                        
                                                        xaxis = dict(
                                                                      title_text = "<b>Score Bins</b>",
                                                                      showline = True,
                                                                      showgrid = False,
                                                                      tickangle = -40,
                                                                      zeroline = False,
                                                                      ticks = "outside",
                                                                   ),
                                                        yaxis = dict(
                                                                      title_text = "<b>Percentage</b>",
                                                                      showline = True,
                                                                      showgrid = False,
                                                                      zeroline = False,
                                                                      ticks = "outside",
                                                                      ticksuffix = "%"
                                                                    ),
                                                        annotations = annot_1,
                                                        barcornerradius= 5,
                                                        showlegend= False,
                                                        hovermode=False
                                                       
                                                        
                                                            )
                                   }
      else:
           
           with pyodbc.connect(connection_string_1) as connect:

                with connect.cursor() as cursor:

                    cursor.execute("""
                                    
                                        SELECT 
                                                *
                                        FROM 
                                            transactions   
                                        WHERE 
                                            
                                            date BETWEEN DATEADD(day, -15, CONVERT(date, GETDATE())) AND CONVERT(date, GETDATE())
                                            AND credential_type = 'production'
                                            AND platform_origin = 'Ai4'
                
                                        
                                """          
                                        
                                
                                )
                    
                    df0 = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

                    df0.drop_duplicates(subset = ["transaction_id"])

                    service_map = {
                                        'Ai Lift': ['signal_2', 'signal_1', 'signal'],
                                        'AI Verify BD+': ['signal_2', 'signal_1', 'signal'],
                                        'Ai Validate BAV FCRA': ['signal_2', 'signal_1', 'signal'],
                                        'Ai Validate BAV': ['signal_2', 'signal_1', 'signal'],
                                        'Ai Validate BD': ['score_act', 'score_acct'],
                                        'AI Verify BD': ['score_act', 'score_acct'],
                                        'Ai Screen Conversion': ['score_conv', 'score_acct'],
                                        'Ai Screen FPD + Conversion': ['score_fpd', 'score_conv', 'score_acct'],
                                        'Ai Screen FPD': ['score_fpd', 'score_acct']
                                  }

                    conditions = [df0['service'] == service for service in service_map.keys()]
                
                    choices = [df0[list(columns)].bfill(axis=1).iloc[:, 0] for columns in service_map.values()]

                    df1 = df0.copy()

                    df1['first_non_null'] = np.select(conditions, choices)

                    # display(df1)

                #     bins = range(-1, 1010, 50)

                #     labels = [f'{a} - {b-1}' for a, b in zip(bins, bins[1:])]

                    bins = [-1] + list(range(0, 1050, 50))

                    labels = ['-1'] + [f'{a}-{b-1}' for a, b in zip(bins[1:-1], bins[2:-1])] + ['950-1000']

                    df2 = pd.DataFrame(pd.cut(df1['first_non_null'], 
                                               bins=bins, 
                                               right=False, 
                                               labels=labels).value_counts(normalize=True).mul(100).round(0).sort_index()).reset_index()
                
                    df2["proportion"] = df2["proportion"].astype(int)
                
                    # display(df2)

                    annot_1 = [dict(
                                x=xi,
                                y=yi,
                                text= f"{str(yi)}%",
                                xanchor='center',
                                yanchor='bottom',
                                showarrow=False,
                                font=dict(
                                        size = 10,
                                        color="#1f77b4"
                                        ),
                                ) for xi, yi in zip(df2["first_non_null"],df2["proportion"])]


                    return {
                                
                                "data" : [
                                        go.Bar(
                                                x = df2["first_non_null"],
                                                y = df2["proportion"]
                                                )
                                        ],

                                "layout" : go.Layout(
                                                title = dict(
                                                                text = "<b>Score Distribution</b>",
                                                                x = 0.5,
                                                                y = 0.95
                                                                ),
                                                
                                                xaxis = dict(
                                                                title_text = "<b>Score Bins</b>",
                                                                showline = True,
                                                                showgrid = False,
                                                                tickangle = -40,
                                                                zeroline = False,
                                                                ticks = "outside",
                                                                ),
                                                yaxis = dict(
                                                                title_text = "<b>Percentage</b>",
                                                                showline = True,
                                                                showgrid = False,
                                                                zeroline = False,
                                                                ticks = "outside",
                                                                ticksuffix = "%"
                                                                ),
                                                annotations = annot_1,
                                                barcornerradius= 5,
                                                showlegend= False,
                                                hovermode=False
                                                
                                                
                                                        )
                                }
           
           
           
           