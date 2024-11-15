#!/usr/bin/python
#-*-coding:utf-8-*-

try:
      import pyodbc
      import numpy as np
      import pandas as pd
      from flask import session
      import plotly.graph_objects as go 
      from database import connection_string_1
      from callbacks_manager import CallbackManager
      from dash import Output, Input, State, no_update 
except ImportError as error:
      raise Exception(f"{error}") from None

callback_manager_9 = CallbackManager()

@callback_manager_9.callback(Output("fig4", "figure"), [Input("bb1", "n_clicks")], [
                                                                                    
                                                                                    State("dd0", "value"),
                                                                                    State("dd1", "value"),
                                                                                    State("dd2", "value"),
                                                                                    State("dt1", "date"),
                                                                                    State("dt2", "date")
                                                                                  ])
def populate_figure_4(n_clicks, name, dba, svr, sdate, edate):
      
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

                    value_counts_df0 = df0["status_message"].value_counts(normalize=True).mul(100).round(2).reset_index()

                    value_counts_df1 = df0["status_message"].value_counts().reset_index()
                
                    df2 = pd.merge(value_counts_df0, value_counts_df1, on = "status_message", how = "inner")

                    return {
                             
                             "data" : [
                                        go.Pie(
                                                labels = df2["status_message"],
                                                values = df2["proportion"],
                                                hole=.5
                                              )
                                      ],

                             "layout" : go.Layout(
                                                   title = dict(
                                                                text = "<b>Transaction Status</b>",
                                                                x = 0.5,
                                                                y = 0.95
                                                                ),
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
                                            customer_name = COALESCE(NULLIF(?, ''), customer_name)
                                            AND date BETWEEN DATEADD(day, -15, CONVERT(date, GETDATE())) AND CONVERT(date, GETDATE())
                                            AND credential_type = 'production'
                
                                        
                                """, (session.get("user"))              
                                        
                                
                                )
                    
                    df0 = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])

                    df0.drop_duplicates(subset = ["transaction_id"])

                    value_counts_df0 = df0["status_message"].value_counts(normalize=True).mul(100).round(2).reset_index()

                    value_counts_df1 = df0["status_message"].value_counts().reset_index()
                
                    df2 = pd.merge(value_counts_df0, value_counts_df1, on = "status_message", how = "inner")

                    return {
                             
                             "data" : [
                                        go.Pie(
                                                labels = df2["status_message"],
                                                values = df2["proportion"],
                                                hole=.5
                                              )
                                      ],

                             "layout" : go.Layout(
                                                   title = dict(
                                                                text = "<b>Transaction Status</b>",
                                                                x = 0.5,
                                                                y = 0.95
                                                                ),
                                                   hovermode=False
                                                   
                                                    
                                  
                             )                    
                    }
    
   
                

