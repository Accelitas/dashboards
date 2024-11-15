#!/usr/bin/python
#-*-coding:utf-8-*-

try:
      import pyodbc
      import warnings
      import pandas as pd
      from dash import Output, Input, State, no_update
      from callbacks_manager import CallbackManager
      from database import connection_string_2
except ImportError as error:
      raise Exception(f"{error}") from None

warnings.simplefilter(action = "ignore", category = FutureWarning)

callback_manager_4 = CallbackManager()

@callback_manager_4.callback(Output("dd1", "options"), [Input("dd0", "value")])
def populate_customer_dba(value):

    with pyodbc.connect(connection_string_2) as connect:

            with connect.cursor() as cursor:

                cursor.execute("""
                                 
                                     SELECT 
                                            DISTINCT customer_dba
                                     FROM 
                                            customers   
                                     WHERE 
                                           customer_name = COALESCE(NULLIF(?, ''), customer_name)
             
                                    
                               """, (value)
                             )
                
                df = pd.DataFrame([{name: row[i] for i, name in enumerate([col[0] for col in cursor.description])} for row in cursor.fetchall()])
                
            #     return [{"label" : k , "value" : v } for k, v in zip(df["customer_dba"], df["customer_dba"])]
            
                df["duplicate_customer_dba"] = df.loc[:,"customer_dba"]

                df.loc[len(df)] = "ALL"

                df.loc[:, "duplicate_customer_dba"].iloc[-1] = " "

                return [{"label" : k , "value" : v } for k, v in zip(df["customer_dba"], df["duplicate_customer_dba"])]

                

