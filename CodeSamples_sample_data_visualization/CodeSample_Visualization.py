import pandas as pd
import plotly.express as px

def read_file(filePath):
    return pd.DataFrame(filePath)
    
def generateKeyMetricsPlot(df):
    fig = px.line(df, x="date", y=df.columns,
              title='Key Metrics"')
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y",
        ticklabelmode="period")
    fig.write_html("plot/fig_key_metrics.html")
    
def generateProductPlot(df):
    fig = px.bar(df, x='cgeocountry', y='PageViews', title='Page View by Country"',labels={
                     "cgeocountry": "Country"
                 },)
    fig.write_html("plot/fig_page_views_products_by_country.html")
    
    fig = px.bar(df, x='cgeocountry', y='Visits', title='Visits by Country"',labels={
                     "cgeocountry": "Country"
                 },)
    fig.write_html("plot/fig_visits_products_by_country.html")

if __name__ == "__main__":
    df = pd.read_json('flatten_key_metrics.json')
    generateKeyMetricsPlot(df)
    
    df = pd.read_json('flatten_products.json')
    generateProductPlot(df)