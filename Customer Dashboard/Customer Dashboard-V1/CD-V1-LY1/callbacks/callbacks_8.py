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

callback_manager_8 = CallbackManager()

@callback_manager_8.callback(Output("fig3", "figure"), [Input("bb1", "n_clicks")], [
                                                                                    
                                                                                    State("dd0", "value"),
                                                                                    State("dd1", "value"),
                                                                                    State("dd2", "value"),
                                                                                    State("dt1", "date"),
                                                                                    State("dt2", "date")
                                                                                  ])
def populate_figure_3(n_clicks, name, dba, svr, sdate, edate):
      
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

                    df0["overall_time"] = df0["overall_time"].div(1000).round(2)

                    bins = np.arange(0, 5, 0.25)

                    labels = [f'{a}' for a, b in zip(bins, bins[1:])]

                    df1 = pd.DataFrame(pd.cut(df0["overall_time"], 
                                              bins=bins, 
                                              right=False, 
                                              labels=labels).value_counts().sort_index()).reset_index()
                    
               
                
          
                    annot_1 = [dict(
                                x=xi,
                                y=yi,
                                text= str(yi),
                                xanchor='center',
                                yanchor='bottom',
                                showarrow=False,
                                font=dict(
                                        size = 10,
                                        color="#1f77b4"
                                        ), 
                            ) for xi, yi in zip(df1.index, df1["count"])]

                    return {
                         "data" : [
                                     go.Bar(
                                             x = df1["overall_time"],
                                             y = df1["count"]
                                           )
                                  ],

                         "layout" : go.Layout(
                                               title = dict(
                                                            text = "<b>Response Time Distribution</b>",
                                                            x = 0.5,
                                                            y = 0.95
                                                            ),
                                               xaxis = dict(
                                                            title_text = "<b>Time (Seconds)</b>",
                                                            type = "category",
                                                            showline=True,
                                                            showgrid = False,
                                                            tickangle = -40,
                                                            zeroline = False,
                                                            ticks = "outside",
                                                       
                                                           ),
                                               yaxis = dict(
                                                             title_text = "<b>Number of Transactions</b>",
                                                             showline=True,
                                                             showgrid = False,
                                                             zeroline = False,
                                                             ticks = "outside",
                                                       
                                                           ),
                                              annotations = annot_1,
                                              barcornerradius= 5,
                                              showlegend=False,
                                              
                                              
                                                
                                             )
                     }

      else:
           return {}
                