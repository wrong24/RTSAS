"""
This code was developed by
wrong24
"""
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix


class Profile:
    def __init__(self, name, loc):
        self.name = name
        self.loc = loc

    def create_profile(self):

        uloc = 'C:\\Users\\wrong\\Desktop\\RTSAS\\user_profiles.csv'
        userprof = pd.read_csv(uloc)
        if self.name not in userprof.columns:
            df1 = pd.DataFrame(columns=['Open', 'Close', 'Volume'])
            df1.to_csv(uloc)
            userprof.insert(0, self.name, "Active User")
            userprof.to_csv(uloc)
            print("NEW PROFILE CREATED")
        else:
            print("EXISTING PROFILE FOUND")
    def saveprof(self,stock,data):
        q = input("Do You want to save this data in your profile ?(Y/N):")
        if q.casefold() == 'y':
            ud = pd.read_csv(self.loc,index_col=0)
            data = data[['Open','Close','Volume']]
            data = pd.concat([data],keys=[stock])
            ud = pd.concat([ud,data])
            ud.to_csv(self.loc)
            print("Saved")
        else:
            pass


class StockAnalyser:
    def __init__(self, name, sdate, edate):
        self.name = name
        self.sdate = sdate
        self.edate = edate

    def retrieve(self):
        data = web.DataReader(self.name,'yahoo',start=self.sdate, end=self.edate)
        return data

    def CandleGraph(self):
        df = web.DataReader(self.name,'yahoo',start = self.sdate,end = self.edate)
        plt.figure(figsize=(10,14))
        plt.bar(range(1,len(df)+1),(df['Volume']/df['Volume'].mean())*(df['High'].mean()//5))
        df = df.drop('Volume', axis=1)
        bp = plt.boxplot([x for x in df.values], meanline=False, patch_artist=True)
        plt.title(self.name)
        c = ['#00FF00','#FF0000']
        colors = []
        for i in range(df.shape[0]):
            colors.append(c[int(df['Close'][i] < df['Open'][i])])
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        plt.show()

    def growth_percentage(self):
        df = web.DataReader(self.name,'yahoo',start = self.sdate,end = self.edate)
        close = np.array(df['Close'])
        gp = close[1:]-close[:-1]
        gp /= close[:-1]
        gp *= 100
        colors = []
        red = '#FF0000'
        green = '#00FF00'
        for c in gp:
            if c>0:
                colors.append(green)
            elif c<0:
                colors.append(red)
        print(gp)
        plt.figure(figsize = (16,10))
        plt.bar(list(df.index)[:-1],gp,color = colors)
        plt.title(f"{self.name} GROWTH PERCENTAGE")
        plt.show()

    def volatility(self):
        df = web.DataReader(self.name, 'yahoo', start=self.sdate, end=self.edate)
        close = np.array(df['Close'])
        gp = close[1:] - close[:-1]
        gp /= close[:-1]
        gp *= 100
        plt.hist(gp,bins=len(gp))
        plt.title(f"{self.name} Volatility")
        plt.show()


n = input("Please Enter A Profile Name : ")
loc = f'C:\\Users\\wrong\Desktop\\RTSAS\\{n.casefold()}.csv'
profile = Profile(n.casefold(),loc)
profile.create_profile()
print("Enter start and end date:(YYYY MM DD)")
Y1, M1, D1 = [int(x) for x in input("Start date: ").split()]
Y2, M2, D2 = [int(x) for x in input("End date: ").split()]
start = datetime.datetime(Y1, M1, D1)
end = datetime.datetime(Y2, M2, D2)
Proceed = True

while Proceed:
    print("1 - Stock data menu\n2 - Stock data visualisation menu\n3 - View Profile Data") #Menu(main) selection.
    choice_main = int(input("Enter choice: "))
    if choice_main == 1:
        company_symbol = input("Enter company symbol: ")
        company = web.DataReader(company_symbol,'yahoo',start,end)
        print("a - Display all data\nb - Select data to be displayed- High,Low,Open,Close,Volume,Adj Close") #Data field selection.
        data_choice = input("Enter choice: ")
        if data_choice.casefold() =='a':
            print('Display head/tail data?H/T/Pass') #row selection.
            row = input('Enter choice: ')
            if row.casefold() =='h':
                num = int(input('Number of values to be displayed: '))
                print(company.head(num))
            elif row.casefold() =='t':
                num = int(input('Number of values to be displayed: '))
                print(company.tail(num))
            elif row.casefold() =='pass':
                print(company)
        elif data_choice.casefold() =='b':
            d =[]
            Data_Field = {'high':'High','low':'Low','open':'Open','close':'Close','volume':'Volume','adj close':'Adj Close'}
            print('Data input - XXXX XXXX XXXX...')
            d1 = [d.append(Data_Field[x.casefold()]) for x in input('Enter data to be displayed: ').split()]
            print('Display head/tail data?H/T/Pass')
            row = input('Enter choice: ')
            if row.casefold() =='h':
                num = int(input('Number of values to be displayed: '))
                print(company[d].head(num))
            elif row.casefold() =='t':
                num = int(input('Number of values to be displayed: '))
                print(company[d].tail(num))
            elif row.casefold() =='pass':
                print(company[d])
        profile.saveprof(company_symbol, company)
    elif choice_main == 2:
        company_variable ={} # to create and store dynamic variables(keys) which have company ticker symbol as values.
        company_ticker ={} # take the values from above and make it into keys and make their values the company data.
        v1 = 'v'
        num_stock = int(input('Enter number of stocks: '))
        for i in range(1,num_stock+1):
            company_variable[v1+str(i)]=input("Enter company ticker symbol: ")
            company_ticker[company_variable[v1+str(i)]] = web.DataReader(company_variable[v1+str(i)],'yahoo',start,end)
        choice_vis = input("a. Plot graph for specific data.\nb. View correlation (Scatter Matrix)."
                           "\nc. View Candle Graph.\nd. View daily Percentage change.\ne. View Stock Volatility."
                           "\nf. View Cumalative Returns.\nEnter your Choice :")
        #Visualisation selection^

        Data_Field = {'high':'High','low':'Low','open':'Open','close':'Close','volume':'Volume','adj close':'Adj Close'}
        if choice_vis.casefold() == 'a':
            spec_data = input("Data to be presented:[High,Low,Open,Close,Volume,Adj Close]")
            spec_data = spec_data.casefold()
            for x in company_ticker.keys():
                company_ticker[x][Data_Field[spec_data]].plot(label = x,figsize = (17,5))
            plt.legend()
            plt.ylabel(spec_data)
            plt.show()
        elif choice_vis.casefold() =='b':
            spec_data = input("Data to be presented:[High,Low,Open,Close,Volume,Adj Close]")
            spec_data = spec_data.casefold()
            comp_concat = pd.concat([company_ticker[x][Data_Field[spec_data]] for x in company_ticker],axis = 1)
            comp_concat.columns = [x for x in company_ticker]
            scatter_matrix(comp_concat,figsize = [8,8],hist_kwds = {'bins':50})
            plt.show()
        elif choice_vis.casefold() == 'c':
            l1 = list(company_variable.keys())
            for a in company_variable:
                stock = StockAnalyser(company_variable[a],start,end)
                stock.CandleGraph()
        elif choice_vis.casefold() == 'd':
            for a in company_variable:
                stock = StockAnalyser(company_variable[a],start,end)
                stock.growth_percentage()
        elif choice_vis.casefold() == 'e':
            for a in company_variable:
                stock = StockAnalyser(company_variable[a], start, end)
                stock.volatility()
        elif choice_vis.casefold() == 'f':
            for a in company_variable:
                stock = StockAnalyser(company_variable[a], start, end)
                df = stock.retrieve()
                df['Returns'] = df['Close']-df['Open']
                plt.hist(df['Returns'],cumulative=True,bins=len(df['Returns']))
                plt.title('Cumulative Return vs Time')
                plt.show()
    elif choice_main == 3:
        d = pd.read_csv(loc,index_col = 0)
        if d.empty:
            print("NO DATA FOUND")
        else:
            if "Unnamed: 0.1" in d.index:
                d = d.drop("Unnamed: 0.1", axis=1)
            print(d)
    print("Return to menu?Y/N") #Menu return selection.
    ret = input()
    if ret.casefold() =='y':
        continue
    elif ret.casefold() =='n':
        break
    else:
        print("Invalid choice.")
        break
