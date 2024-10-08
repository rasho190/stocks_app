# %%
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import streamlit as st

# %%
st.title('Control de Inversiones en Portafolio')

acciones = st.text_input('Ingresa las empresas a analizar (separadas por comas)', "AAPL, MSFT, GOOGL, TSLA")

inicio = st.date_input('Selecciona una fecha para iniciar el análisis',
                       value = pd.to_datetime('2022-01-01'))

datos = yf.download(acciones, start = inicio)['Adj Close']
print(datos.columns)

# %%
df_ret = datos.pct_change()
acum_ret = (df_ret + 1).cumprod() - 1
port_ret = acum_ret.mean(axis = 1)
port_ret.index = pd.to_datetime(port_ret.index).tz_convert(None)
port_ret

# %%
benchmark_1 = yf.download('^GSPC', start = inicio)['Adj Close']
bench_ret_1 = benchmark_1.pct_change()
bench_dev_1 = (bench_ret_1 + 1).cumprod() - 1
bench_dev_1

benchmark_2 = yf.download('VT', start = inicio)['Adj Close']
bench_ret_2 = benchmark_2.pct_change()
bench_dev_2 = (bench_ret_2 + 1).cumprod() - 1

# %%
w = (np.ones(len(df_ret.cov()))/len(df_ret))
port_std = (w.dot(df_ret.cov()).dot(w))**(1/2)

# %%
st.subheader('Rendimiento de Portafolio vs S&P500 vs VT')

df_final = pd.concat([port_ret, bench_dev_1, bench_dev_2], axis = 1)
df_final.columns = ['Rendimiento de Portafolio','Rendimiento S&P500','Rendimiento VTI']

fig = go.Figure()
fig.add_trace(go.Line(x = df_final.index, y = df_final.iloc[:,0], line = dict(color = 'royalblue'), name = 'Portafolio'))
fig.add_trace(go.Line(x = df_final.index, y = df_final.iloc[:,1], line = dict(color = 'firebrick'), name = 'S&P500'))
fig.add_trace(go.Line(x = df_final.index, y = df_final.iloc[:,2], line = dict(color = '#109618'), name = 'VTI'))
st.plotly_chart(fig)

# %%
st.subheader('Riesgo del Portafolio')
port_std

st.subheader('Riesgo del S&P 500 (Benchmark)')
bench_risk_1 = bench_ret_1.std()
bench_risk_1

st.subheader('Riesgo del VTI (Benchmark)')
bench_risk_2 = bench_ret_2.std()
bench_risk_2

st.subheader('Composición del Portafolio')
fig_2 = px.pie(w, labels = datos.columns, values = w, names = datos.columns, color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_2)


