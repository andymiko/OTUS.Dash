# ИМПОРТЫ

import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import geopandas as gpd
from graphfunc import print_bar_by_sales

# ИНИЦИАЛИЗАЦИЯ ПРИЛОЖЕНИЯ И ЗАГРУЗКА ДАННЫХ
app = Dash(__name__)

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

# ВЁРСТКА
app.title = 'OTUS DASH'
app.layout = html.Div([
    html.H1("HELLO WORLD!"),
    html.Div(sales_channel),
    html.Div(rentable_slider),
    html.Div(date_range),
    dcc.Graph(figure=print_bar_by_sales(dataFrame=df))
])

# CALLBACK'S (ФУНКЦИИ ОБРАТНОГО ВЫЗОВА)

# ЗАПУСК ПРИЛОЖЕНИЯ

if __name__ == '__main__':
    app.run_server(debug=True)