import random
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px

from invest_returns import InvestReturns

#Background
# st.markdown(
# """
# <style>
# [data-testid="stAppViewContainer"]{
#     background-image: url(
#         https://media.istockphoto.com/id/175600020/photo/money-pile-100-dollar-bills.jpg?b=1&s=170667a&w=0&k=20&c=yH3DQty7oarHDI_FW5ufcpfRozOHizU2oWG2_u3GCXo=
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

# Calcul de benefice et rendement
calculateur = InvestReturns(symbol)
calculateur.returns(invest_values, start_date, end_date)

col2.metric(
    "Gain", 
    "{:.0f} €".format(
    calculateur.benef_net
    ),
    delta = "{:.2f}%".format(round(calculateur.benef_net/calculateur.total_invest*100, 2))
)
col3.metric(
    "Rendement moyen annuel",
    "{:.2f}%".format(
    calculateur.rend_moy_annuel*100
    )
)

#graphique
df_graph = pd.DataFrame(calculateur.monthly_returns.loc[start_date:end_date])
fig = px.line(df_graph, x=df_graph.index, y="Adj Close")
last_value = df_graph["Adj Close"].iloc[-1]
fig.add_shape(
    type="line",
    x0=df_graph.index[0] ,y0=last_value,
    x1=df_graph.index[-1], y1=last_value,
    line=dict(color="red", width=1, dash="dashdot")
)

st.plotly_chart(fig)

#Calcul du bénéfice moyen du cours
st.header("Calcul du rendement moyen du cours")
period = st.slider(
    'Selectionner une période à étudier',
    0, 30, 10)
rend_moy_annuel_list = []
for i in range(1000):
    start_date = datetime.datetime.strptime("1985-10-01", "%Y-%m-%d").date() + datetime.timedelta(days=random.randint(0, (datetime.date.today() - datetime.timedelta(days=365*period) - datetime.datetime.strptime("1985-10-01", "%Y-%m-%d").date()).days))
    calculateur.returns(
        invest_values=1, start_date=start_date, end_date=start_date+datetime.timedelta(days=365*period)
        )
    rend_moy_annuel_list.append(calculateur.rend_moy_annuel)

st.metric("Rendement annuel moyen",
    "{:.2f}%".format(
    round(pd.Series(rend_moy_annuel_list).mean(),2)
    )
)