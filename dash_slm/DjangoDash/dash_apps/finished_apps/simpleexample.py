from django.shortcuts import render

# Create your views here.
import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flask import Flask
from sqlalchemy import create_engine, text
import urllib
import pyodbc
from datetime import datetime
import time
import datetime
import sqlite3 as db
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dash_table
from dash.exceptions import PreventUpdate
from django_plotly_dash import DjangoDash


# https://pypi.org/project/dash-bootstrap-templates/ #for more information
dbc_css = ["https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"]
app = DjangoDash('SimpleExample',external_stylesheets=dbc_css)

# app.config.suppress_callback_exceptions=True
# app = dash.Dash(__name__, server = server, external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
# desired_column = f"select TimeStamp, {tag_name} from {table}"
# location_tags = pd.read_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\location_tags.csv')
# location_tags = pd.read_csv('.\\assets\\location_tags.csv')
# location_tags = pd.read_csv('dash_slm\\DjangoDash\\dash_apps\\finished_apps\\assets\\location_tags.csv')
location_tags = pd.read_csv(r'C:\Users\ghddu\Desktop\Eddie\Eddie\django_dash\dash_slm\DjangoDash\dash_apps\finished_apps\assets\location_tags.csv')
# location_tags['Nav_GPS1_Latitude'] = location_tags['Nav_GPS1_Latitude'].astype(float)
# location_tags['Nav_GPS1_Longitude'] = location_tags['Nav_GPS1_Longitude'].astype(float)

route_map = px.line_mapbox(location_tags, lat="Nav_GPS1_Latitude", lon="Nav_GPS1_Longitude", zoom=3, height=300)
route_map.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41,
    margin={"r":0,"t":0,"l":0,"b":0})

sheets = ['LDC1', 'LDC2, HDC1', 'HDC2', 'LNGVAP', 'FVAP', 'BOGHTR', 'WUHTR', 'GWHSTM', 'SCLR']
# RCA_mastersheet_path = 'C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\SHI Rules Master sheet_03302023_rev10_for_dash.xlsx'
# RCA_mastersheet_path = '.\\assets\\SHI Rules Master sheet_03302023_rev10_for_dash.xlsx'
RCA_mastersheet_path = r'C:\Users\ghddu\Desktop\Eddie\Eddie\django_dash\dash_slm\DjangoDash\dash_apps\finished_apps\assets\SHI Rules Master sheet_03302023_rev10_for_dash.xlsx'


LD1_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='LDC1')
LD2_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='LDC2')
HD1_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='HDC1')
HD2_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='HDC2')
LNGV_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='LNGVAP')
FV_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='FVAP')
BOGH_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='BOGHTR')
WUH_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='WUHTR')
GWHS_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='GWHSTM')
SC_RCA_mastersheet = pd.read_excel(RCA_mastersheet_path, sheet_name='SCLR')

#creating index column for selecting rows in dash table

LD1_RCA_mastersheet['id'] = LD1_RCA_mastersheet.index
LD2_RCA_mastersheet['id'] = LD2_RCA_mastersheet.index
HD1_RCA_mastersheet['id'] = HD1_RCA_mastersheet.index
HD2_RCA_mastersheet['id'] = HD2_RCA_mastersheet.index
LNGV_RCA_mastersheet['id'] = LNGV_RCA_mastersheet.index
FV_RCA_mastersheet['id'] = FV_RCA_mastersheet.index
BOGH_RCA_mastersheet['id'] = BOGH_RCA_mastersheet.index
WUH_RCA_mastersheet['id'] = WUH_RCA_mastersheet.index
GWHS_RCA_mastersheet['id'] = GWHS_RCA_mastersheet.index
SC_RCA_mastersheet['id'] = SC_RCA_mastersheet.index

FV_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='FV_sim_inputs')
LNGV_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='LNGV_sim_inputs')
BOGH_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='BOGH_sim_inputs')
WUH_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='WUH_sim_inputs')
GWHS_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='GWHS_sim_inputs')
LD1_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='LD1_sim_inputs')
LD2_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='LD2_sim_inputs')
HD1_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='HD1_sim_inputs')
HD2_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='HD2_sim_inputs')
SC_sim_inputs = pd.read_excel(RCA_mastersheet_path, sheet_name='SC_sim_inputs')

# desired_column = text("select * from Input_history order by Nav_GPS1_UTC asc")
# quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-DS34DTB\SQLEXPRESS;DATABASE=S-Project;UID=user1;PWD=1234')

# quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-O74IH9F\SPARTA;DATABASE=S-Project;UID=sa;PWD=1234')
# quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LPPLVAI\SQLEXPRESS2019;DATABASE=S-Project;UID=sa;PWD=Welcome1')
# quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=EMERSON\SQLEXPRESS01;DATABASE=S-Project;UID=user1;PWD=1234')

# engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
# conn = engine.connect()
# data = pd.read_sql(desired_column, conn)

logo_path = 'assets/SHI_logo.jpg'
# print(len(output_columns))

#sim_image paths
FV_sim_image_path = 'assets/FV_sim_image.jpg'
LNGV_sim_image_path = 'assets/LNGV_sim_image.jpg'
BOGH_sim_image_path = 'assets/BOGH_sim_image.jpg'
WUH_sim_image_path = 'assets/WUH_sim_image.jpg'
GWHS_sim_image_path = 'assets/GWHS_sim_image.jpg'
LD1_sim_image_path = 'assets/LD1_sim_image.jpg'
LD2_sim_image_path = 'assets/LD2_sim_image.jpg'
HD1_sim_image_path = 'assets/HD1_sim_image.jpg'
HD2_sim_image_path = 'assets/HD2_sim_image.jpg'
SC_sim_image_path = 'assets/SC_sim_image.png'

# CSS ------------------------------------------------------>

main_tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
main_tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    # 'backgroundColor': '#119DFF',
    'backgroundColor': '#004473',
    # 'backgroundColor': 'grey',
    'color': 'white',
    'padding': '6px'
}
tab_style = {
    "background": "#323130",
    'text-transform': 'uppercase',
    'color': 'white',
    'border': 'grey',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    "background": "grey",
    'text-transform': 'uppercase',
    'color': 'white',
    'font-size': '11px',
    'font-weight': 600,
    'align-items': 'center',
    'justify-content': 'center',
    'border-radius': '4px',
    'padding':'6px',
    'border-style': 'solid',
    'border-color': 'grey',
    'fontWeight': 'bold'
}
subtab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '11px',
    'fontWeight': 'bold'
}
subtab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    # 'backgroundColor': '#119DFF',
    'backgroundColor': 'grey',
    'font-size': '11px',
    # 'backgroundColor': 'grey',
    'color': 'white',
    'padding': '6px'
}

# CSS <-------------------------------------------------------


app.layout = dbc.Container([
    dbc.Row([
            # dbc.Col([], width = 1),
            dbc.Col(html.Img(src=logo_path, height = 60),width = 4), 
            html.Br(),
            dbc.Col(html.H2('Ship Life Cycle Management (SLM)'), align="center")
    ],align='center'),
        html.Br(),
    dcc.Tabs(id = 'tabs', value = 'Tab3', children = [
         
        dcc.Tab( label = 'Forcing Vaporizer', id = 'Assets_subtab1', value = 'FV_Template', style = tab_style, selected_style = tab_selected_style, children = [
            html.Div([
                dcc.Tabs(id='FV_subtabs', value = 'FV_Template', children = [
        
                    dcc.Tab( label = 'Template', id = 'FV_template', value = 'FV_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
                        html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.H2(''),
                                html.Br(),
                                html.Br(),
                                html.H2('DWSIM Simulation Flowsheet'),
                                html.Img(src=FV_sim_image_path, height = 500)], width = 6),
                            dbc.Col([
                                html.H2(''),
                                html.Br(),
                                html.Br(),
                                html.H2('DWSIM Model Inputs'),
                                html.Div([
                                dash_table.DataTable(
                                    id='FV_standard_keys',
                                    data=SC_sim_inputs.to_dict('records'),
                                    filter_action = 'native', editable = True,
                                    columns=[{'id': c, 'name': c} for c in FV_sim_inputs.columns],
                                    style_cell_conditional=[{
                                            'if': {'column_id': c},
                                            'textAlign': 'left'
                                        } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                                    style_data={
                                        'color': 'black',
                                        'backgroundColor': 'white'
                                    },
                                    style_data_conditional=[{
                                            'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(220, 220, 220)',
                                    }],
                                    style_header={
                                        'backgroundColor': 'rgb(210, 210, 210)',
                                        'color': 'black',
                                        'fontWeight': 'bold'
                                    },
                                    fill_width=True
                                    )
                                ])
                            ], width = {'size': 4, 'offset': 2})
                        ]),
        
            # html.Br(),
                        dbc.Row([
                            html.Div([
                            html.H2(''),
                            html.Br(),
                            html.H2('RCA Template'),
                            #below is the case of 'Horizontal Scrolling via Fixed Columns
                            dash_table.DataTable(
                            id='FV_RCA_table',
                            row_selectable = 'multi',
                            data=FV_RCA_mastersheet.to_dict('records'),
                            filter_action = 'native', editable = True,
                            columns=[{'id': c, 'name': c} for c in FV_RCA_mastersheet.columns if c != "id"],
                            style_cell_conditional=[{
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                            style_data={
                                'color': 'black',
                                'backgroundColor': 'white',
                                # 'whiteSpace': 'normal',
                                # 'height': 'auto',
                            },
                            style_data_conditional=[{
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                            }],
                            style_header={
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'fontWeight': 'bold'
                            },
                            # style_cell={
                            #     'overflow': 'hidden',
                            #     'textOverflow': 'ellipsis',
                            #     'maxWidth': 0
                            # }
                            fixed_columns={
                                'headers': True, 'data': 2
                            },
                            style_table={
                                'minWidth': '110%'
                            }),
                            html.Button(id="FV_save_button",n_clicks=0,children="Save"),
                            html.Div(id="FV_save",children="Press button to save changes")
                            ])
                        ]),
                        ])
                    ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='FV_div', style={'float': 'left', 'width': '400'})
            ])
        ]),
        dcc.Tab( label = 'LNG Vaporizer', id = 'Assets_subtab2', value = 'LNGV_Template', style = tab_style, selected_style = tab_selected_style, children = []),
        dcc.Tab( label = 'BOG Heater', id = 'Assets_subtab3', value = 'BOGH_Template', style = tab_style, selected_style = tab_selected_style, children = [
            html.Div([
                dcc.Tabs(id='BOGH_subtabs', value = 'BOGH_Template', children = [
                
                dcc.Tab( label = 'Template', id = 'BOGH_template', value = 'BOGH_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
        html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Simulation Flowsheet'),
                    html.Img(src=BOGH_sim_image_path, height = 500)], width = 6),
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Model Inputs'),
                    html.Div([
                    dash_table.DataTable(
                        id='BOGH_standard_keys',
                        data=SC_sim_inputs.to_dict('records'),
                        filter_action = 'native', editable = True,
                        columns=[{'id': c, 'name': c} for c in BOGH_sim_inputs.columns],
                        style_cell_conditional=[{
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                        }],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        fill_width=True
                        )
                    ])
                ], width = {'size': 4, 'offset': 2})
            ]),
        
            # html.Br(),
            dbc.Row([
                html.Div([
                html.H2(''),
                html.Br(),
                html.H2('RCA Template'),
                #below is the case of 'Horizontal Scrolling via Fixed Columns
                dash_table.DataTable(
                id='BOGH_RCA_table',
                row_selectable = 'multi',
                data=BOGH_RCA_mastersheet.to_dict('records'),
                filter_action = 'native', editable = True,
                columns=[{'id': c, 'name': c} for c in BOGH_RCA_mastersheet.columns if c != "id"],
                style_cell_conditional=[{
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    # 'whiteSpace': 'normal',
                    # 'height': 'auto',
                },
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                # style_cell={
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipsis',
                #     'maxWidth': 0
                # }
                fixed_columns={
                    'headers': True, 'data': 2
                },
                style_table={
                    'minWidth': '110%'
                }),
                html.Button(id="BOGH_save_button",n_clicks=0,children="Save"),
                html.Div(id="BOGH_save",children="Press button to save changes")
                ])
            ]),
        ])
                ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='BOGH_div', style={'float': 'left', 'width': '400'})
            ])
        ]),
        dcc.Tab( label = 'Warmup Heater', id = 'Assets_subtab4', value = 'WUH_Template', style = tab_style, selected_style = tab_selected_style, children = [
            html.Div([
                dcc.Tabs(id='WUH_subtabs', value = 'WUH_Template', children = [
                
                dcc.Tab( label = 'Template', id = 'WUH_template', value = 'WUH_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
                    html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Simulation Flowsheet'),
                    html.Img(src=WUH_sim_image_path, height = 500)], width = 6),
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Model Inputs'),
                    html.Div([
                    dash_table.DataTable(
                        id='WUH_standard_keys',
                        data=WUH_sim_inputs.to_dict('records'),
                        filter_action = 'native', editable = True,
                        columns=[{'id': c, 'name': c} for c in WUH_sim_inputs.columns],
                        style_cell_conditional=[{
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                        }],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        fill_width=True
                        )
                    ])
                ], width = {'size': 4, 'offset': 2})
            ]),
        
            # html.Br(),
            dbc.Row([
                html.Div([
                html.H2(''),
                html.Br(),
                html.H2('RCA Template'),
                #below is the case of 'Horizontal Scrolling via Fixed Columns
                dash_table.DataTable(
                id='WUH_RCA_table',
                row_selectable = 'multi',
                data=WUH_RCA_mastersheet.to_dict('records'),
                filter_action = 'native', editable = True,
                columns=[{'id': c, 'name': c} for c in WUH_RCA_mastersheet.columns if c != "id"],
                style_cell_conditional=[{
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    # 'whiteSpace': 'normal',
                    # 'height': 'auto',
                },
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                # style_cell={
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipsis',
                #     'maxWidth': 0
                # }
                fixed_columns={
                    'headers': True, 'data': 2
                },
                style_table={
                    'minWidth': '110%'
                }),
                html.Button(id="WUH_save_button",n_clicks=0,children="Save"),
                html.Div(id="WUH_save",children="Press button to save changes")
                ])
            ]),
        ])
                ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='WUH_div', style={'float': 'left', 'width': '400'})
            ])
        ]),
        dcc.Tab( label = 'Glycol water heater (steam)', id = 'Assets_subtab5', value = 'GWHS_Template', style = tab_style, selected_style = tab_selected_style, children = [
            html.Div([
                dcc.Tabs(id='GWHS_subtabs', value = 'GWHS_Template', children = [
                
                dcc.Tab( label = 'Template', id = 'GWHS_template', value = 'GWHS_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
                    html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Simulation Flowsheet'),
                    html.Img(src=GWHS_sim_image_path, height = 500)], width = 6),
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Model Inputs'),
                    html.Div([
                    dash_table.DataTable(
                        id='GWHS_standard_keys',
                        data=GWHS_sim_inputs.to_dict('records'),
                        filter_action = 'native', editable = True,
                        columns=[{'id': c, 'name': c} for c in GWHS_sim_inputs.columns],
                        style_cell_conditional=[{
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                        }],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        fill_width=True
                        )
                    ])
                ], width = {'size': 4, 'offset': 2})
            ]),
        
            # html.Br(),
            dbc.Row([
                html.Div([
                html.H2(''),
                html.Br(),
                html.H2('RCA Template'),
                #below is the case of 'Horizontal Scrolling via Fixed Columns
                dash_table.DataTable(
                id='GWHS_RCA_table',
                row_selectable = 'multi',
                data=GWHS_RCA_mastersheet.to_dict('records'),
                filter_action = 'native', editable = True,
                columns=[{'id': c, 'name': c} for c in GWHS_RCA_mastersheet.columns if c != "id"],
                style_cell_conditional=[{
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    # 'whiteSpace': 'normal',
                    # 'height': 'auto',
                },
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                # style_cell={
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipsis',
                #     'maxWidth': 0
                # }
                fixed_columns={
                    'headers': True, 'data': 2
                },
                style_table={
                    'minWidth': '110%'
                }),
                html.Button(id="GWHS_save_button",n_clicks=0,children="Save"),
                html.Div(id="GWHS_save",children="Press button to save changes")
                ])
            ]),
        ])
                ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='GWHS_div', style={'float': 'left', 'width': '400'})
            ])
        ]),
        dcc.Tab( label = 'LD Compressor 1', id = 'Assets_subtab6', value = 'LD1_Template', style = tab_style, selected_style = tab_selected_style, children = [
            html.Div([
                dcc.Tabs(id='LD1_subtabs', value = 'LD1_Template', children = [
                
                dcc.Tab( label = 'Template', id = 'LD1_template', value = 'LD1_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
                    html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Simulation Flowsheet'),
                    html.Img(src=LD1_sim_image_path, height = 500)], width = 6),
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Model Inputs'),
                    html.Div([
                    dash_table.DataTable(
                        id='LD1_standard_keys',
                        data=LD1_sim_inputs.to_dict('records'),
                        filter_action = 'native', editable = True,
                        columns=[{'id': c, 'name': c} for c in LD1_sim_inputs.columns],
                        style_cell_conditional=[{
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                        }],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        fill_width=True
                        )
                    ])
                ], width = {'size': 4, 'offset': 2})
            ]),
        
            # html.Br(),
            dbc.Row([
                html.Div([
                html.H2(''),
                html.Br(),
                html.H2('RCA Template'),
                #below is the case of 'Horizontal Scrolling via Fixed Columns
                dash_table.DataTable(
                id='LD1_RCA_table',
                row_selectable = 'multi',
                data=LD1_RCA_mastersheet.to_dict('records'),
                filter_action = 'native', editable = True,
                columns=[{'id': c, 'name': c} for c in LD1_RCA_mastersheet.columns if c != "id"],
                style_cell_conditional=[{
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    # 'whiteSpace': 'normal',
                    # 'height': 'auto',
                },
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                # style_cell={
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipsis',
                #     'maxWidth': 0
                # }
                fixed_columns={
                    'headers': True, 'data': 2
                },
                style_table={
                    'minWidth': '110%'
                }),
                html.Button(id="LD1_save_button",n_clicks=0,children="Save"),
                html.Div(id="LD1_save",children="Press button to save changes")
                ])
            ]),
        ])
                ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='LD1_div', style={'float': 'left', 'width': '400'})
            ])
        ]),
        dcc.Tab( label = 'LD Compressor 2', id = 'Assets_subtab7', value = 'LD2_Template', style = tab_style, selected_style = tab_selected_style, children = [
            html.Div([
                dcc.Tabs(id='LD2_subtabs', value = 'LD2_Template', children = [
                
                dcc.Tab( label = 'Template', id = 'LD2_template', value = 'LD2_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
                    html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Simulation Flowsheet'),
                    html.Img(src=LD2_sim_image_path, height = 500)], width = 6),
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Model Inputs'),
                    html.Div([
                    dash_table.DataTable(
                        id='LD2_standard_keys',
                        data=LD2_sim_inputs.to_dict('records'),
                        filter_action = 'native', editable = True,
                        columns=[{'id': c, 'name': c} for c in LD2_sim_inputs.columns],
                        style_cell_conditional=[{
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                        }],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        fill_width=True
                        )
                    ])
                ], width = {'size': 4, 'offset': 2})
            ]),
        
            # html.Br(),
            dbc.Row([
                html.Div([
                html.H2(''),
                html.Br(),
                html.H2('RCA Template'),
                #below is the case of 'Horizontal Scrolling via Fixed Columns
                dash_table.DataTable(
                id='LD2_RCA_table',
                row_selectable = 'multi',
                data=LD2_RCA_mastersheet.to_dict('records'),
                filter_action = 'native', editable = True,
                columns=[{'id': c, 'name': c} for c in LD2_RCA_mastersheet.columns if c != "id"],
                style_cell_conditional=[{
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    # 'whiteSpace': 'normal',
                    # 'height': 'auto',
                },
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                # style_cell={
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipsis',
                #     'maxWidth': 0
                # }
                fixed_columns={
                    'headers': True, 'data': 2
                },
                style_table={
                    'minWidth': '110%'
                }),
                html.Button(id="LD2_save_button",n_clicks=0,children="Save"),
                html.Div(id="LD2_save",children="Press button to save changes")
                ])
            ]),
        ])

                ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='LD2_div', style={'float': 'left', 'width': '400'})
            ])
        ]),
        dcc.Tab( label = 'HD Compressor 1', id = 'Assets_subtab8', value = 'HD1_Template', style = tab_style, selected_style = tab_selected_style, children = [
            html.Div([
                dcc.Tabs(id='HD1_subtabs', value = 'HD1_Template', children = [
                
                dcc.Tab( label = 'Template', id = 'HD1_template', value = 'HD1_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
                    html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Simulation Flowsheet'),
                    html.Img(src=HD1_sim_image_path, height = 500)], width = 6),
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Model Inputs'),
                    html.Div([
                    dash_table.DataTable(
                        id='HD1_standard_keys',
                        data=HD1_sim_inputs.to_dict('records'),
                        filter_action = 'native', editable = True,
                        columns=[{'id': c, 'name': c} for c in HD1_sim_inputs.columns],
                        style_cell_conditional=[{
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                        }],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        fill_width=True
                        )
                    ])
                ], width = {'size': 4, 'offset': 2})
            ]),
        
            # html.Br(),
            dbc.Row([
                html.Div([
                html.H2(''),
                html.Br(),
                html.H2('RCA Template'),
                #below is the case of 'Horizontal Scrolling via Fixed Columns
                dash_table.DataTable(
                id='HD1_RCA_table',
                row_selectable = 'multi',
                data=HD1_RCA_mastersheet.to_dict('records'),
                filter_action = 'native', editable = True,
                columns=[{'id': c, 'name': c} for c in HD1_RCA_mastersheet.columns if c != "id"],
                style_cell_conditional=[{
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    # 'whiteSpace': 'normal',
                    # 'height': 'auto',
                },
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                # style_cell={
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipsis',
                #     'maxWidth': 0
                # }
                fixed_columns={
                    'headers': True, 'data': 2
                },
                style_table={
                    'minWidth': '110%'
                }),
                html.Button(id="HD1_save_button",n_clicks=0,children="Save"),
                html.Div(id="HD1_save",children="Press button to save changes")
                ])
            ]),
        ])
                ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='HD1_div', style={'float': 'left', 'width': '400'})
            ])
        ]),
        dcc.Tab( label = 'HD Compressor 2', id = 'Assets_subtab9', value = 'Assets_Subtab9', style = tab_style, selected_style = tab_selected_style, children = []),
        dcc.Tab( label = 'Subcooler', id = 'Assets_subtab10', value = 'Subcooler_Template', style = tab_style, selected_style = tab_selected_style,  children = [
            # dbc.Row([dbc.Col(html.P("Working Hours"), width=3), dbc.Col(html.P("Performance Health"), width=3)]), 
            html.Div([
                dcc.Tabs(id='Subcooler_subtabs', value = 'Subcooler_Template', children = [
                
                dcc.Tab( label = 'Template', id = 'Subcooler_template', value = 'Subcooler_Template', style = subtab_style, selected_style = subtab_selected_style, children = [
                    html.Div([
            dbc.Row([
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Simulation Flowsheet'),
                    html.Img(src=SC_sim_image_path, height = 500)], width = 6),
                dbc.Col([
                    html.H2(''),
                    html.Br(),
                    html.Br(),
                    html.H2('DWSIM Model Inputs'),
                    html.Div([
                    dash_table.DataTable(
                        id='SC_standard_keys',
                        data=SC_sim_inputs.to_dict('records'),
                        filter_action = 'native', editable = True,
                        export_format = 'csv',
                        columns=[{'id': c, 'name': c} for c in SC_sim_inputs.columns],
                        style_cell_conditional=[{
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Property', 'Standard_Key (Ship Big Server)']],
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },
                        style_data_conditional=[{
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(220, 220, 220)',
                        }],
                        style_header={
                            'backgroundColor': 'rgb(210, 210, 210)',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },
                        fill_width=True
                        )
                    ])
                ], width = {'size': 4, 'offset': 2})
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id = 'standard_key_trend')
    
                ]),


            ]),
            # html.Br(),
            dbc.Row([
                html.Div([
                html.H2(''),
                html.Br(),
                html.H2('RCA Template'),
                #below is the case of 'Horizontal Scrolling via Fixed Columns
                dash_table.DataTable(
                id='SC_RCA_table',
                row_selectable = 'multi',
                data=SC_RCA_mastersheet.to_dict('records'),
                filter_action = 'native', editable = True,
                columns=[{'id': c, 'name': c} for c in SC_RCA_mastersheet.columns if c != "id"],
                style_cell_conditional=[{
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Parent_Node', 'Problem_Name', 'Tags', 'Standard_Key', 'Condition', 'Logic', 'Additional condition', 'AdviceMessage']],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    # 'whiteSpace': 'normal',
                    # 'height': 'auto',
                },
                style_data_conditional=[{
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold'
                },
                # style_cell={
                #     'overflow': 'hidden',
                #     'textOverflow': 'ellipsis',
                #     'maxWidth': 0
                # }
                fixed_columns={
                    'headers': True, 'data': 2
                },
                style_table={
                    'minWidth': '110%'
                }),
                html.Button(id="SC_save_button",n_clicks=0,children="Save"),
                html.Div(id="SC_save",children="Press button to save changes")
                ])
            ]),        
        ])
                ])
                ], vertical=True, parent_style={'float': 'left'}),
            html.Div(id='subcooler_div', style={'float': 'left', 'width': '400'})
            ])
        ])
    ])
], fluid = True, className = 'dbc')



#selected row highlighting callbacks

@app.callback(
    Output("SC_RCA_table", "style_data_conditional"),
    Input("SC_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("SC_RCA_history_table", "style_data_conditional"),
    Input("SC_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("FV_RCA_table", "style_data_conditional"),
    Input("FV_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]


@app.callback(
    Output("FV_RCA_history_table", "style_data_conditional"),
    Input("FV_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("BOGH_RCA_table", "style_data_conditional"),
    Input("BOGH_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("BOGH_RCA_history_table", "style_data_conditional"),
    Input("BOGH_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("WUH_RCA_table", "style_data_conditional"),
    Input("WUH_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("WUH_RCA_history_table", "style_data_conditional"),
    Input("WUH_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("GWHS_RCA_table", "style_data_conditional"),
    Input("GWHS_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("GWHS_RCA_history_table", "style_data_conditional"),
    Input("GWHS_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("LD1_RCA_table", "style_data_conditional"),
    Input("LD1_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("LD1_RCA_history_table", "style_data_conditional"),
    Input("LD1_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("LD2_RCA_table", "style_data_conditional"),
    Input("LD2_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("LD2_RCA_history_table", "style_data_conditional"),
    Input("LD2_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback(
    Output("HD1_RCA_table", "style_data_conditional"),
    Input("HD1_RCA_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

@app.callback( 
    Output("HD1_RCA_history_table", "style_data_conditional"),
    Input("HD1_RCA_history_table", "derived_viewport_selected_row_ids"),
)
def style_selected_rows(selRows):
    if selRows is None:
        return dash.no_update
    return [
        {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "yellow",}
        for i in selRows
    ]

#Save edited dash table
@app.callback(
        Output("SC_save","children"),
        [Input("SC_save_button","n_clicks")],
        [State("SC_RCA_table","data")]
        )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\SC_table_from_dash.csv',index=False)
        return "Data Submitted"
    
@app.callback(
        Output("FV_save","children"),
        [Input("FV_save_button","n_clicks")],
        [State("FV_RCA_table","data")]
        )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\FV_table_from_dash.csv',index=False)
        return "Data Submitted"
    
@app.callback(
    Output("BOGH_save","children"),
    [Input("BOGH_save_button","n_clicks")],
    [State("BOGH_RCA_table","data")]
    )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\BOGH_table_from_dash.csv',index=False)
        return "Data Submitted"
    
@app.callback(
    Output("WUH_save","children"),
    [Input("WUH_save_button","n_clicks")],
    [State("WUH_RCA_table","data")]
    )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\WUH_table_from_dash.csv',index=False)
        return "Data Submitted"

@app.callback(
    Output("GWHS_save","children"),
    [Input("GWHS_save_button","n_clicks")],
    [State("GWHS_RCA_table","data")]
    )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\GWHS_table_from_dash.csv',index=False)
        return "Data Submitted"

@app.callback(
    Output("LD1_save","children"),
    [Input("LD1_save_button","n_clicks")],
    [State("LD1_RCA_table","data")]
    )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\LD1_table_from_dash.csv',index=False)
        return "Data Submitted"

@app.callback(
    Output("LD2_save","children"),
    [Input("LD2_save_button","n_clicks")],
    [State("LD2_RCA_table","data")]
    )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\LD2_table_from_dash.csv',index=False)
        return "Data Submitted"

@app.callback(
    Output("HD1_save","children"),
    [Input("HD1_save_button","n_clicks")],
    [State("HD1_RCA_table","data")]
    )

def selected_data_to_csv(nclicks,table1): 
    if nclicks == 0:
        raise PreventUpdate
    else:
        pd.DataFrame(table1).to_csv('C:\\Users\\okfar\\OneDrive\\Programming\\Plotly and dash\\assets\\HD1_table_from_dash.csv',index=False)
        return "Data Submitted"

# #input trend callback
# @app.callback(Output('input_trend', 'figure'),
#                 Input('input_dropdown', 'value'))

# def get_input_trend(tag):
#     print(tag)
#     print(type(tag))
#     if type(tag) == str:
#         tag = list(tag)
#         tag = ["".join(tag)]
#     print(type(tag))
#     print(len(tag))
#     fig = go.Figure()
#     size = 400
#     if len(tag) == 1:
#         fig.add_scatter(x=data['Nav_GPS1_UTC'], y=data[tag[0]])
#         size = 400
#     elif len(tag) > 1:
#         fig = make_subplots(rows = len(tag), cols = 1, shared_xaxes = True)
#         for i in range(len(tag)):
#             fig.append_trace(go.Scatter(x=data['Nav_GPS1_UTC'], y=data[tag[i]], name = tag[i], line={'width':2}), row = i+1, col = 1)
#         size = 400+(200*len(tag))
#     fig.update_layout(height = size)
#     return fig

@app.callback(
    Output("standard_key_trend", "figure"),
    Input("SC_RCA_table", "active_cell"),
    State("SC_RCA_table", "derived_viewport_data"),
)
def cell_clicked(cell, data):
    fig = go.Figure()
    # print(cell)
    # print(data)
    if cell:
        selected_key = data[cell["row"]][cell["column_id"]]

        # return f"You have selected {selected_key}"
        desired_column = text(f"select Nav_GPS1_UTC, {selected_key} from Input_history order by Nav_GPS1_UTC asc")
        quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=BOOK-1P8754C41H\SQLEXPRESS;DATABASE=S-Project;UID=user1;PWD=1234')
        # quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-O74IH9F\SPARTA;DATABASE=S-Project;UID=sa;PWD=1234')
        # quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-LPPLVAI\SQLEXPRESS2019;DATABASE=S-Project;UID=sa;PWD=Welcome1')
        # quoted = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=EMERSON\SQLEXPRESS01;DATABASE=S-Project;UID=user1;PWD=1234')
        engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
        conn = engine.connect()
        data = pd.read_sql(desired_column, conn)
        fig.add_scatter(x=data['Nav_GPS1_UTC'], y=data[selected_key])
        size = 400
        fig.update_layout(height = size, title = f"{selected_key}")

        return fig
    else:

        return dash.no_update

# if __name__ == '__main__':
#     app.run_server(debug=True)

