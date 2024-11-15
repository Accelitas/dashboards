#!/usr/bin/python
#-*-coding:utf-8-*-

try:
      import pyodbc
      import numpy as np
      import pandas as pd
      import plotly.graph_objects as go 
      from database import connection_string_1
      from callbacks_manager import CallbackManager
      from dash import Output, Input, State, no_update 
except ImportError as error:
      raise Exception(f"{error}") from None

callback_manager_10 = CallbackManager()

@callback_manager_10.callback(Output("fig5", "figure"), [Input("bb1", "n_clicks")], [
                                                                                    
                                                                                    State("dd0", "value"),
                                                                                    State("dd1", "value"),
                                                                                    State("dd2", "value"),
                                                                                    State("dt1", "date"),
                                                                                    State("dt2", "date")
                                                                                  ])
def populate_figure_5(n_clicks, name, dba, svr, sdate, edate):
      
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
                
                                        
                                """, (name, dba, svr, sdate, edate)              
                                        
                                
                                )
                    
                    df0 = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

                    df0.drop_duplicates(subset = ["transaction_id"])

                    df1 = df0[["transaction_id", "reason_code"]].copy()

                    df2 = df0[["transaction_id", "reason_code2"]].copy()

                    df3 = df0[["transaction_id", "reason_code3"]].copy()

                    df4 = df0[["transaction_id", "reason_code4"]].copy()

                    df5 = df0[["transaction_id", "reason_code5"]].copy()

                    df2 = df2.rename(columns={"reason_code2": "reason_code"})

                    df3 = df3.rename(columns={"reason_code3": "reason_code"})

                    df4 = df4.rename(columns={"reason_code4": "reason_code"})

                    df5 = df5.rename(columns={"reason_code5": "reason_code"})

                    df6 = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)

                    df7 = df6.dropna()

                    reason_code_counts = df7["reason_code"].value_counts()

                    reason_code_counts_percentage = df7["reason_code"].value_counts(normalize=True).mul(100).round(2)

                    df8 = pd.merge(reason_code_counts, reason_code_counts_percentage , how = "inner", left_on = "reason_code", right_on = "reason_code").sort_index(ascending = False).reset_index()

                    df9 = df8.drop(df8.index[-1])

                    annot_1 = [dict(
                                x=xi,
                                y=yi,
                                text= str(yi),
                                yref = "y1",
                                xanchor='center',
                                yanchor='bottom',
                                showarrow=False,
                                font=dict(
                                        size = 10,
                                        color="#1f77b4"
                                        ), 
                            ) for xi, yi in zip(df9.index, df9["count"])]
                
                    annot_2 = [dict(
                                x=xi,
                                y=yi,
                                yref = "y2",
                                text= f"{str(yi)}%",
                                xanchor='center',
                                yanchor='top',
                                showarrow=False,
                                font=dict(
                                        size = 10,
                                        color="#ff7f0e"
                                        ), 
                            ) for xi, yi in zip(df9.index, df9["proportion"])]
                    
                    return {
                         
                             "data" : [
                                         go.Bar(
                                                x = df9["reason_code"],
                                                y = df9["count"],
                                                yaxis = "y1"
                                               ),
                                          go.Scatter(
                                                     x = df9["reason_code"],
                                                     y = df9["proportion"],
                                                     mode='lines+markers',
                                                     line_color= "#ff7f0e",
                                                     yaxis = "y2"
                                                    )
                                      ],
                             "layout" : go.Layout(
                                                    title = dict(
                                                                text = "<b>Transaction Distribution By Reason Code</b>",
                                                                x = 0.5,
                                                                y = 0.95
                                                               ),
                                                    xaxis = dict(
                                                                 title_text = "<b>Reason Codes</b>",
                                                                 type = "category",
                                                                 showline=True,
                                                                 showgrid = False,
                                                                 tickangle = -40,
                                                                 zeroline = False,
                                                                 ticks = "outside",
                                                               
                                                                ),
                                                    yaxis = dict(
                                                                 title_text = "<b>Volume</b>",
                                                                 showline=True,
                                                                 showgrid = False,
                                                                 zeroline = False,
                                                                 ticks = "outside",
                                                               
                                                                ),
                                                    yaxis2 = dict(
                                                                  title_text = "<b>% Reason Codes</b>",
                                                                  showline=True,
                                                                  showgrid = False,
                                                                  zeroline = False,
                                                                  ticks = "outside",
                                                                  ticksuffix = "%",
                                                                  overlaying = "y",
                                                                  side = "right"
                                                                 ),
                                                    annotations = annot_1 + annot_2,
                                                    bargap=0.70,
                                                    bargroupgap=0.0,
                                                    barcornerradius= 5,
                                                    showlegend=False,
                                                    paper_bgcolor = "#f9faf7"
                                                    
                                                    
                                                   
                                               )
                    }
                
      else:
           return {}