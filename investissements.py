import datetime
import pandas as pd
import yfinance as yf
import streamlit as st
import plotly.express as px

#Background
# st.markdown(
# """
# <style>
# [data-testid="stAppViewContainer"]{
#     background-image: url(
#         https://t3.ftcdn.net/jpg/05/34/10/18/360_F_534101844_xIyxkPs1EBHj7kFULi1burnV7qlgx5Y4.jpg
#         );
#     background-size: 100%, 100%;
#     background-position: 100%, center;
#     background-repeat: no-repeat;
#     }
# </style>
# """, 
# unsafe_allow_html=True)

#Title
st.title("Calculateur de bénéfice boursier")

# Choix utilisateur
col1, col2, col3 = st.columns(3)
start_date = col1.date_input(
    "Début d'investissement :", 
    value = pd.to_datetime("2003-01-05"), min_value = datetime.datetime(1971, 1, 1)
    )
end_date = col2.date_input(
    "Fin d'investissement :",
    value = datetime.datetime.now(), min_value = start_date, max_value = datetime.datetime.now()
    )
symbol_list = {
    "CAC40" : "^FCHI", 
    "Nasdaq" : "^NDX", 
    "Dow Jones" : "^DJI", 
    "S&P 500": "^GSPC",
    "Apple": "AAPL", 
    "custom" :""}

indice = col3.selectbox("Cours souhaité :", symbol_list.keys())
if indice=="custom": symbol_list["custom"] = col3.text_input("Symbole du cours souhaité :", value = "^NDX")
symbol = symbol_list[indice]
invest_values = col1.number_input(
    "Argent investi chaque mois :", value=50, min_value=0
)
col2.metric(
    "Durée de l'investissement en année",
    round((end_date - start_date).days / 365.25, 2) 
)
total_invest = col3.metric(
    "Argent total investi", 
    "{:.0f} €".format(
    invest_values*((end_date.year - start_date.year)*12 + end_date.month - start_date.month)
    )
    )

df = yf.download(symbol, start=start_date, end=end_date)

# sélection uniquement des fins de mois
monthly_returns = df.resample('M')['Adj Close'].last().dropna().loc[start_date:end_date]
percentage_df  = pd.DataFrame(
    {"percentage" : monthly_returns[-1]/monthly_returns}
)
benef_net = ((percentage_df*invest_values).sum() - len(percentage_df)*invest_values).values[0]
total_invest = invest_values*len(percentage_df)
nb_annee = (end_date - start_date).days / 365.25
col2.metric(
    "Gain", 
    "{:.0f} €".format(
    benef_net
    ),
    delta = "{:.2f}%".format(round(benef_net/total_invest*100, 2))
)
col3.metric(
    "Rendement moyen annuel",
    "{:.2f}%".format(
    (benef_net/total_invest*100)/nb_annee
    )
)
col1.metric(
    "Rendement moyen annuel composé",
    "{:.2f}%".format(
    ((1+benef_net/total_invest)**(1/nb_annee)-1)*100
    )
)

#graphique
df_graph = df.loc[start_date:end_date].resample("M").last()
fig = px.line(df_graph, x=df_graph.index, y="Close")
last_value = df_graph["Close"].iloc[-1]
fig.add_shape(
    type="line",
    x0=df_graph.index[0] ,y0=last_value,
    x1=df_graph.index[-1], y1=last_value,
    line=dict(color="red", width=1, dash="dashdot")
)

st.plotly_chart(fig)
