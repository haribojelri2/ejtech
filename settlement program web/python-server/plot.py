from scipy.stats import linregress
import pandas as pd

class Graph():
    def __init__(self,df,start_date, end_date,predict_date,timeInterval=1):
        self.df = df
        self.start_date = pd.to_datetime(start_date)
        print(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.timeInterval = timeInterval
        self.rawSettlement = self.df['침하량']
        predictData = self.df[(self.df['측정일']>self.start_date) & (self.df['측정일']<self.end_date)]
        self.settlement = predictData['침하량']
        self.t = (predictData['측정일'] - self.start_date).dt.days
        self.so = self.settlement.iloc[0]
        self.sl = self.settlement.iloc[-1]
        self.s_diff = self.settlement - self.so
        self.date_pred = pd.date_range(start=self.start_date, end=self.end_date + pd.Timedelta(days=int(predict_date)),freq='D')
        self.date=self.df[self.df['측정일']<self.end_date]

    def basic_plot(self):
        return self.df['측정일'],self.df['성토고']
        
    def hyperbolic_plot(self):
        t_s = (-self.t[1:]/self.s_diff[1:])
        b,a,_,_,_ = linregress(self.t[1:],t_s)
        s_final = 1/b-self.so
        t_pred = (self.date_pred - self.start_date).days
        s_pred = self.so - t_pred / (a+b*t_pred)

        return self.date_pred, s_pred , self.date['측정일'] ,self.rawSettlement , self.t[1:] , t_s , a+b*self.t[1:]