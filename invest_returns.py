import datetime
import pandas as pd
import yfinance as yf

class InvestReturns:
    def __init__(self, symbol):
        self.monthly_returns = yf.download(
            symbol
            ).resample('M')['Adj Close'].last().dropna()

    
    def returns(self, invest_values, start_date=pd.to_datetime("1990-04-01"), end_date=datetime.datetime.now()):
        gain_df = pd.DataFrame(
            self.monthly_returns.loc[start_date:end_date][-1]/self.monthly_returns.loc[start_date:end_date]
        )
        self.nb_annee = (end_date - start_date).days / 365.25
        self.benef_net = ((gain_df*invest_values).sum() - len(gain_df)*invest_values).values[0]
        self.total_invest = invest_values*len(gain_df)
        self.rend_moy_annuel = (self.benef_net/self.total_invest)/self.nb_annee
