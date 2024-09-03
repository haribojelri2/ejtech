from plot import Graph
import pandas as pd


path = "C:\\Users\\user\\Desktop\\ejproject\\침하량 데이터.xlsx"

df = pd.read_excel(path)

graph = Graph(df,'2017-11-28', '2018-02-22',100)

graph.asaoka_plot()