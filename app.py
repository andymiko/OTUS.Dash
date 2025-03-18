# ИМПОРТЫ

import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import geopandas as gpd
from graphfunc import print_bar_by_sales, print_histo_rentable
from db_api.base import Database
import asyncio

# ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ И ЗАГРУЗКА ДАННЫХ
app = Dash(__name__)

db = Database()
asyncio.run(db.create_tables())

# Дата начало-конец периода

min_date = asyncio.run(db.get_data_for_filters(type='minmax',param='orderdate'))[0]
# min_date = pd.to_datetime(min_date)

max_date = asyncio.run(db.get_data_for_filters(type='minmax',param='orderdate'))[1]
# max_date = pd.to_datetime(max_date)

# Начало-конец слайдера
rent_max = float(asyncio.run(db.get_data_for_filters(type='minmax',param='rentabel'))[1])
rent_min = float(asyncio.run(db.get_data_for_filters(type='minmax',param='rentabel'))[0])

# Канал продаж
sales_options = asyncio.run(db.get_data_for_filters(type='option',param='channel'))

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
    value=[rent_min, rent_max],
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
app.layout = html.Div([
    html.H1("HELLO WORLD!"),
    html.Div(sales_channel),
    html.Div(rentable_slider),
    html.Div(date_range),
    html.Div(accept_button),
    dcc.Graph(id='product_bar'),
    dcc.Graph(id='histogram')
])

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

    channel = None
    rentabel_range = range_value
    orderdate_range = (start_date, end_date)

    if bool(value_sales_channel):
        channel = value_sales_channel

    records = asyncio.run(db.get_data(
        orderdate_range=orderdate_range,
        rentabel_range=rentabel_range,
        channel=channel
    ))

    df = pd.DataFrame([record.to_dict() for record in records])

    return print_bar_by_sales(df)

@app.callback(
    Output(component_id='histogram',component_property='figure'),
    Input(component_id='rent_slider',component_property='value')
)
def one_filter_renta(range_value):

    rentabel_range = range_value

    records = asyncio.run(db.get_data(
        rentabel_range=rentabel_range))

    df = pd.DataFrame([record.to_dict() for record in records])

    return print_histo_rentable(df)

# ЗАПУСК ПРИЛОЖЕНИЯ


if __name__ == '__main__':
    app.run_server(debug=True)