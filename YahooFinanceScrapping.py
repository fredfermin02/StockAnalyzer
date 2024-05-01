from bs4 import BeautifulSoup
import requests
import json
import re
import statistics
from datetime import datetime, timedelta, timezone

url_Sales = 'https://finance.yahoo.com/quote/DELL/analysis'
url_yahoo_Key_statistics = 'https://finance.yahoo.com/quote/DELL/key-statistics'
url_cnbc_for_Debt = 'https://apps.cnbc.com/view.asp?symbol=DELL.O&uid=stocks/stockvsPeers&view=keyMeasures'
url_wallmine_incomestatement = 'https://wallmine.com/NASDAQ/DELL/historical-statement-values.json?statement_kind=income_statements'
url_ycharts_PERatio = 'https://ycharts.com/charts/fund_data.json?calcs=id%3Ape_ratio%2Cinclude%3Atrue%2C%2C&chartId=&chartType=interactive&correlations=&customGrowthAmount=&dataInLegend=value&dateSelection=range&displayDateRange=false&endDate=&format=real&legendOnChart=false&lineAnnotations=&nameInLegend=name_and_ticker&note=&partner=basic_2000&quoteLegend=false&recessions=false&scaleType=linear&securities=id%3ADELL%2Cinclude%3Atrue%2C%2C&securityGroup=&securitylistName=&securitylistSecurityId=&source=false&splitType=single&startDate=&title=&units=false&useCustomColors=false&useEstimates=false&zoom=1&hideValueFlags=false&redesign=true&chartAnnotations=&axisExtremes=&maxPoints=681&chartCreator=false'
url_AlphaVantage_CompanyOverview = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=DELL&apikey=3X4SXZL8VFMG6W45'
url_Alphavanatge_CompranyStockPrice = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=DELL&apikey=3X4SXZL8VFMG6W45'

def SalesGrowth():
    try:
        page = requests.get(url_Sales, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
        page.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(page.text, features="html.parser")
        
        # Find the row containing the sales growth percentage
        sales_growth_table = soup.find('td', string='Sales Growth (year/est)').parent.parent
        
        if sales_growth_table  == None: 
            print("Error getting sales growth from yahoo finance.")
            return None
        
        # Get all <td> elements within the <tr> element
        find_elements_in_table = sales_growth_table.find_all('tr')[1]
        # Extract the text from the last <td> element
        nextYear_Sales_Growth = find_elements_in_table.find_all('td')[3].get_text()
        return add_format_for_yahooValues(nextYear_Sales_Growth)

    except (requests.RequestException, IndexError, AttributeError) as e:
        if AttributeError: 
            print("Sales Growth (year/est) not found in Yahoo Finance")
        print(f"An error occurred: {e}")
        return None

def SMA200():
    try:
        response = requests.get(url_AlphaVantage_CompanyOverview)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        sma200_value = data.get("200DayMovingAverage")
        return float(sma200_value)
    except Exception as e:
        print(f"Error in SMA200 function: {e}")
        return None

def marketCap():
    try:
        response = requests.get(url_AlphaVantage_CompanyOverview)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        mrkCap = data.get("MarketCapitalization")
        return int(mrkCap)
    except Exception as e:
        print(f"Error in marketCap function: {e}")
        return None

def Cash_of_company(url_yahoo_Key_statistics):
    try:
        page = requests.get(url_yahoo_Key_statistics, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
        page.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(page.text, features="html.parser")
        total_cash_row = soup.find('td', string='Total Cash  (mrq)').find_next_sibling('td', class_='value')
        total_cash_value = total_cash_row.get_text()
        
        return total_cash_value
    
    except (requests.RequestException, AttributeError) as e:
        if AttributeError: 
            print("Total Cash  (mrq) not found in Yahoo Finance")
        print(f"An error occurred: {e}")
        return None

def total_debt_to_capital():
    try:
        page = requests.get(url_cnbc_for_Debt,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
        soup = BeautifulSoup(page.text,features="html.parser")

        find_td_debt_to_capital = soup.find_all('span', string='(MRQ)')[3].parent.parent
        td_debt_to_capital = find_td_debt_to_capital.find_all('td')[3:]
        values = [td.get_text(strip=True) for td in td_debt_to_capital ]
        return values

    except (requests.RequestException, AttributeError) as e:
        if AttributeError: 
            print("Total debt  (mrq) not found in Yahoo Finance")
        print(f"An error occurred: {e}")
        return None
    

def operatingExpenses_of_company():
    try:
        response = requests.get(url_wallmine_incomestatement, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
        response.raise_for_status()  # Raise an exception for bad status codes
        json_data = response.json()
        annual_state_income = json_data["annual"][0]
        total_operating_expenses = annual_state_income.get("total_operating_expenses")
        return total_operating_expenses
    except (requests.RequestException, KeyError) as e:
        print(f"An error occurred: {e}")
        return None

def solvency_of_company():
    try:
        expenses = operatingExpenses_of_company(url_wallmine_incomestatement)
        cash = add_format_for_yahooValues(Cash_of_company())
        # Further processing
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

    #print((operatingExpenses_of_company()/12))


def add_format_for_yahooValues(value):
    try:
        match = re.match(r'^([\d.]+)([BM])$', value)
        if not match:
            raise ValueError("Invalid value format")
        
        integer_part, letter_part = match.groups()
        integer_part = float(integer_part)
        
        if letter_part == "B":
            value = integer_part * 1_000_000_000
        elif letter_part == "M":
            value = integer_part * 1_000_000
        
        return value
    except ValueError as e:
        print(f"An error occurred: {e}")
        return None

def avg_ProfitMargin_Last4Years():
    try:
        response = requests.get(url_wallmine_incomestatement,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
        response_text = response.text
        json_data = json.loads(response_text)
        #Number of years is 1 from most recent year to 4 latest.
        net_Income_wallmine = float(json_data["annual"][i]["net_income"])
        total_revenue_wallmine =float(json_data["annual"][i]["total_revenue"])
        profitMargin_Per_Year = [(net_Income_wallmine/total_revenue_wallmine)*100 for i in range(4) ]
        standard_deviation = statistics.stdev(profitMargin_Per_Year)
        avg_ProfitMargin = statistics.mean(profitMargin_Per_Year)
        return avg_ProfitMargin
    except (requests.RequestException, KeyError, ZeroDivisionError) as e:
        print(f"An error occurred: {e}")
        return None

def get_EpochTime_OfFirstDay_Last_6_Month():
    try:
        dt = datetime.now(timezone.utc)
        epoch_times=[]  
        
        #Loop to get the Epoch time of the first day of the last 6 months
        for i in range(6):
            # replace day number with 1 and the hour, minute, second with 0
            res = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Validate is if is not in a weekend. 
            if res.weekday() == 5:
                res = dt.replace(day=3, hour=0, minute=0, second=0, microsecond=0)
            elif res.weekday() == 6:
                res = dt.replace(day=2, hour=0, minute=0, second=0, microsecond=0)
            #Epoch time of the first day of the month.
            epoch_time = int(res.timestamp())
            epoch_times.append(epoch_time*1000)
            #Go one day before. So 30th or 31th of the month 
            dt = res - timedelta(days=1)
        
        return epoch_times
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def avg_PERatio_Last_6_Month():
    try:
        response = requests.get(url_ycharts_PERatio,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
        response_text = response.text
        json_data = json.loads(response_text)

        chart_data = json_data["chart_data"][0][0]["raw_data"]
        epoch_Times = get_EpochTime_OfFirstDay_Last_6_Month()

        pe_Ratios = []
        chart_data_pointer = len(chart_data)
        for time in epoch_Times:
            for i in range(chart_data_pointer - 1, -1, -1):
                if time == chart_data[i][0]:
                    pe_Ratios.append(chart_data[i][1])
                    chart_data_pointer = i - 10
                    break
        return statistics.mean(pe_Ratios)
    
    except (requests.RequestException, KeyError, IndexError) as e:
        print(f"An error occurred: {e}")
        return None
    
def discover_profit_for_year():
    if avg_ProfitMargin_Last4Years()  == None:
        print("Error with avg_ProfitMargin_Last4Years()")
        return None
    return SalesGrowth()*(avg_ProfitMargin_Last4Years()/100)

def future_market_cap():
    if discover_profit_for_year()  == None:
        print("Error with discover_profit_for_year()")
        return None
    return discover_profit_for_year() * avg_PERatio_Last_6_Month()

def possible_return():
    # print(future_market_cap()/marketCap())
    
    if future_market_cap()  == None:
        print("Error with future_market_cap()")
        return None

    todays_date = datetime.now()
    if todays_date.weekday() == 5:
        todays_date = todays_date.replace(day=todays_date.day-1)
    elif todays_date.weekday() == 6:
        todays_date = todays_date.replace(day=todays_date.day-2)
    response = requests.get(url_Alphavanatge_CompranyStockPrice)
    data = json.loads(response.text)
    closing_price = data['Time Series (Daily)'][str(todays_date.date())]['4. close']
    
    possbile_return = (future_market_cap()/marketCap()) * float(closing_price)

    return possbile_return

print(possible_return())
print("Done")