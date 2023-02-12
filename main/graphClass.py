import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Graph: 
    def __init__(self, data, x_title : str, graph_type: str, y_title: str = None, title: str = "Title", ticks: int = 11, color = '#001146'):
        self.data = data
        self.graph_type = graph_type
        self.x_title = x_title
        self.y_title = y_title
        self.ticks = ticks
        self.color = color
        self.title = title
    def graph(self):
        if self.graph_type == "line":
            sns.set(style="ticks", context="talk")
            sns.lineplot(x= self.x_title, y= self.y_title, data=self.data, color= self.color)
            l = []
            e = 0
            for i in range(self.ticks):
                l.append(e)
                e += len(self.data)/(self.ticks - 1)
            l[len(l)-1] = len(self.data) - 1
            plt.xticks(l)
            plt.title(self.title)
            plt.show()
        elif self.graph_type == "scatter":
            sns.set(style="ticks", context="talk")
            sns.scatterplot(x= self.x_title,  y= self.y_title, data= self.data, color = self.color)
            l = []
            e = 0
            for i in range(self.ticks):
                l.append(e)
                e += len(self.data)/(self.ticks - 1)
            l[len(l)-1] = len(self.data) - 1
            plt.xticks(l)
            plt.title(self.title)
            plt.show()
        elif self.graph_type == "box":
            #self.data = self.data.sort_values(self.x_title)
            categories = pd.qcut(self.data[self.x_title], q = self.ticks)
            sns.set(style= "darkgrid")
            sns.boxplot(x = categories, y = self.data[self.y_title])
            plt.title(self.title)
            plt.show()
if __name__ == "main":
    data = pd.read_csv("test.csv")
    pnlvstime = Graph(data = data, x_title = "date", y_title = "pnl_cum_sum", graph_type = "line", ticks = 5, title = "Profit and Loss vs time")
    pnlvstime.graph()
    volvstime = Graph(data = data, x_title = "date", y_title = "pnl_vol", graph_type = "line", ticks = 5, title= "The volatility of the profit and loss over time")
    volvstime.graph()
#volpnlvstime = Graph(data = data, x_title = )
# 
# '''                                                                                                                                                                                               
