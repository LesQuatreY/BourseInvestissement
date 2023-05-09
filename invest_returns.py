import pandas as pd
import yfinance as yf

class InvestReturns:
    def __init__(self, symbol, start_date, end_date):
        monthly_returns = yf.download(
            symbol, start=start_date, end=end_date
            ).resample('M')['Adj Close'].last().dropna().loc[start_date:end_date]
        self.monthly_returns = monthly_returns
        self.gain_df  = pd.DataFrame(
        {"percentage" : monthly_returns[-1]/monthly_returns}
        )
        self.nb_annee = (end_date - start_date).days / 365.25
    
    def returns(self, invest_values):
        self.benef_net = ((self.gain_df*invest_values).sum() - len(self.gain_df)*invest_values).values[0]
        self.total_invest = invest_values*len(self.gain_df)
