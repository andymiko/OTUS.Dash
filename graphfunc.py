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