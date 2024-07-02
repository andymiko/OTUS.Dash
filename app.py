# ИМПОРТЫ

import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import geopandas as gpd
from graphfunc import print_bar_by_sales, print_histo_rentable

# ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ И ЗАГРУЗКА ДАННЫХ
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('data_for_otus.csv')

# Дата начало-конец периода
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
min_date = df['OrderDate'].min()
max_date = df['OrderDate'].max()

# Начало-конец слайдера
rent_max = df['rentabel'].max()
rent_min = df['rentabel'].min()

# Канал продаж
sales_options = [{'value':col,'label':col} for col in df['Channel'].unique().tolist()]

# ЭЛЕМЕНТЫ

sales_channel = dcc.Dropdown(
    id='sales_channel',
    options=sales_options,
    value=[],
    clearable=False,
    placeholder='Выберите канал продаж',
    multi=True
)

rentable_slider = dcc.RangeSlider(
    id='rent_slider',
    min=rent_min,
    max=rent_max,
    value=[rent_min,rent_max],
    dots=False,
    tooltip={"placement": "bottom", "always_visible": True}
)

date_range = dcc.DatePickerRange(
    id='data_filter',
    display_format='DD-MM-YYYY',
    min_date_allowed=min_date,
    max_date_allowed=max_date,
    start_date=min_date,
    end_date=max_date)

accept_button = dbc.Button('Выполнить',id='accept_button',n_clicks=0,className='me-1',color='warning')

# ВЁРСТКА
app.title = 'OTUS DASH'
app.layout = dbc.Container(
    html.Div([
    #     HEADER
        html.Div(
            dbc.Row([
                dbc.Col(html.Img(
                    src=app.get_asset_url("images/logo_black.png"),
                    style={'width':'200px','margin-top':'10px','margin-bottom':'10px'}),
                style={'width':'200px'}),
                dbc.Col(html.Div(html.H1('BI-dashboard on Dash')))]),className='app-header'
        ),
    # BODY
        html.Div([
            html.Div(sales_channel),
            html.Div(rentable_slider),
            html.Div(date_range),
            html.Div(accept_button),

            dcc.Graph(id='product_bar'),
            dcc.Graph(id='histogram')
        ]),
    # FOOTER
        html.Div(
            dbc.Row([
                dbc.Col(html.Img(src=app.get_asset_url("images/logo-small_black.png"),style={'width':'200px'})),
                dbc.Col(html.Div(html.H3('OTUS. Курс «BI-аналитика»')),align='center'),
                dbc.Col(html.P("Колесник Андрей, 2024 г.")),
        ],align='center'),
        className='app-footer')
    ])
)
# app.layout = html.Div([
#     html.H1("HELLO WORLD!"),
#     html.Div(sales_channel),
#     html.Div(rentable_slider),
#     html.Div(date_range),
#     html.Div(accept_button),
#     dcc.Graph(id='product_bar'),
#     dcc.Graph(id='histogram')
# ])

# CALLBACK'S (ФУНКЦИИ ОБРАТНОГО ВЫЗОВА)

@app.callback(
    Output(component_id='product_bar',component_property='figure'),
    Input(component_id='accept_button',component_property='n_clicks'),
    State(component_id='sales_channel',component_property='value'),
    State(component_id='data_filter',component_property='start_date'),
    State(component_id='data_filter',component_property='end_date'),
    State(component_id='rent_slider',component_property='value')
)
def sales_channel_filter(n_clicks, value_sales_channel, start_date, end_date, range_value):

    if bool(value_sales_channel):
        f_data = df.copy(deep=True)
        f_data = f_data[f_data['Channel'].isin(value_sales_channel)]
    else:
        f_data = df.copy(deep=True)

    f_data = f_data[(f_data['rentabel'] >= range_value[0]) & (f_data['rentabel'] <= range_value[-1])]

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    f_data = f_data[(f_data['OrderDate'] >= start_date) & (f_data['OrderDate'] <= end_date)]

    return print_bar_by_sales(f_data)

@app.callback(
    Output(component_id='histogram',component_property='figure'),
    Input(component_id='rent_slider',component_property='value')
)
def one_filter_renta(range_value):
    f_data = df.copy(deep=True)
    f_data = f_data[(f_data['rentabel'] >= range_value[0]) & (f_data['rentabel'] <= range_value[-1])]
    return print_histo_rentable(f_data)

# ЗАПУСК ПРИЛОЖЕНИЯ

if __name__ == '__main__':
    app.run_server(debug=True)