import plotly.express as px

def print_bar_by_sales(dataFrame):
    filtred_data = dataFrame.groupby(['Product Name']).agg({'Line Total': 'sum'}).reset_index()
    filtred_data.sort_values(by='Line Total', ignore_index=True, inplace=True)
    fig = px.bar(filtred_data, x="Product Name", y="Line Total", title="Продажи")
    fig.update_layout(xaxis_title="Продукт", yaxis_title="Рубли")
    return fig

def print_histo_rentable(dataFrame):
    filtred_data = dataFrame.copy(deep=True)
    fig = px.histogram(filtred_data, x="rentabel", color="Category", marginal="box")
    fig.update_layout(xaxis_title="Рентабельность", yaxis_title="Кол-во")
    return fig

def print_bar_by_district_subdistrict(dataFrame,type_layout:str):
    if type_layout == 'district':
        fig = px.histogram(dataFrame, x='District', y='Line Total')
        fig.update_layout(xaxis_title="Округ", yaxis_title="RUB")
        return fig
    if type_layout == 'subdistrict':
        fig = px.histogram(dataFrame, x='SubDistrict', y='Line Total')
        fig.update_layout(xaxis_title="Район", yaxis_title="RUB")
        return fig

def print_treemap_sales_district_subdistric(dataFrame):
    fig = px.treemap(dataFrame, path=[px.Constant("Москва"), 'District', 'SubDistrict', 'Category'],
                     values='Line Total', maxdepth=3)
    fig.update_traces(textinfo='label+percent parent')
    return fig

def print_box_price_for_one(dataFrame):
    fig = px.box(dataFrame, x='District', y='Unit Price', color="Category",)
    fig.update_layout(xaxis_title="Округ", yaxis_title="RUB")
    return fig

def print_pie_category(dataFrame):
    fig = px.pie(dataFrame, values='Line Total', names='Category')
    return fig

def print_line_dynamic(dataFrame):
    fig = px.line(dataFrame, x='OrderDate_month', y='Line Total')
    fig.update_layout(xaxis_title="Дата", yaxis_title="Всего")
    return fig