import plotly.express as px

def print_bar_by_sales(dataFrame):
    filtred_data = dataFrame.groupby(['product_name']).agg({'line_total': 'sum'}).reset_index()
    filtred_data.sort_values(by='line_total', ignore_index=True, inplace=True)
    fig = px.bar(filtred_data, x="product_name", y="line_total", title="Продажи")
    fig.update_layout(xaxis_title="Продукт", yaxis_title="Рубли")
    return fig

def print_histo_rentable(dataFrame):
    filtred_data = dataFrame.copy(deep=True)
    fig = px.histogram(filtred_data, x="rentabel", color="category", marginal="box")
    fig.update_layout(xaxis_title="Рентабельность", yaxis_title="Кол-во")
    return fig