#!/usr/bin/python
#-*-coding:utf-8-*-

try:
      import pyodbc
      import pandas as pd
      import plotly.graph_objects as go 
      from database import connection_string_1
      from callbacks_manager import CallbackManager
      from dash import Output, Input, State, no_update     
except ImportError as error:
      raise Exception(f"{error}") from None

callback_manager_6 = CallbackManager()

@callback_manager_6.callback(Output("fig1", "figure"), [Input("bb1", "n_clicks")], [
                                                                                    
                                                                                    State("dd0", "value"),
                                                                                    State("dd1", "value"),
                                                                                    State("dd2", "value"),
                                                                                    State("dt1", "date"),
                                                                                    State("dt2", "date")
                                                                                  ])
def populate_figure_1(n_clicks, name, dba, svr, sdate, edate):
      
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

                    df1 = df0.loc[:,["date", "transaction_id", "overall_time"]]

                    df1["overall_time"] = df1["overall_time"].div(1000)

                    df2 = df1.groupby("date").agg({"transaction_id" : "count", "overall_time" : "mean"}).reset_index()

                    df2["overall_time"] = df2["overall_time"].round(2)

                    df2["date"] = pd.to_datetime(df2["date"])

                    df2["date"] = df2["date"].dt.strftime("%d-%m-%Y")

                    annot_1 = [dict(
                                x=xi,
                                y=yi,
                                yref = "y1",
                                text= str(yi),
                                xanchor='center',
                                yanchor='bottom',
                                showarrow=False,
                                font=dict(
                                        size = 10,
                                        weight = "bold",
                                        color="#1f77b4"
                                        ), 
                            ) for xi, yi in zip(df2["date"], df2["transaction_id"])]
                    
                    annot_2 = [dict(
                                        x=xi,
                                        y=yi,
                                        yref = "y2",
                                        text= str(yi),
                                        xanchor='center',
                                        yanchor='bottom',
                                        showarrow=False,
                                        font=dict(
                                                size = 10,
                                                color="#ff7f0e"
                                                ), 
                                ) for xi, yi in zip(df2["date"], df2["overall_time"])]


                    return {
                

                             "data" : [
                                        go.Bar(
                                                x = df2["date"],
                                                y = df2["transaction_id"],
                                                yaxis = "y1"
                                             ),

                                        go.Scatter(
                                                        x = df2["date"],
                                                        y = df2["overall_time"],
                                                        mode='lines+markers',
                                                        line_color = "#ff7f0e",
                                                        yaxis = "y2"
                                                 )
                                     ],

                            "layout" : go.Layout(
                                                 title = dict(
                                                                text = "<b>Volume By Date</b>",
                                                                x = 0.5,
                                                                y = 0.95
                                                             ),
                                                 xaxis = dict(
                                                                title_text = "<b>Date</b>",
                                                                tickangle = -40,
                                                                showline = True,
                                                                showgrid = False,
                                                                ticks = "outside",
                                                         ),
                                                 yaxis = dict(
                                                                title_text = "<b>Number of Transactions</b>",
                                                                showline = True,
                                                                showgrid = False,
                                                                ticks = "outside",
                                                          ),

                                                  yaxis2 = dict(
                                                                   title_text = "<b>Average Respone Time</b>",
                                                                   showline = True,
                                                                   showgrid = False,
                                                                   ticks = "outside",
                                                                   overlaying = "y",
                                                                   side = "right"
                                                               ),
                                                  annotations = annot_1 + annot_2,
                                                  barcornerradius= 5,
                                                  showlegend= False,
                                                 
                                                  
                                                       
                                                  )
                                        }
      else:
           return {}
                                        
                                      