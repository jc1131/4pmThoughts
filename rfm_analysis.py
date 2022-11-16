#import modules
import pandas as pd # for dataframes
import datetime as dt

cols = [0, 1, 3, 4, 5]
data = pd.read_excel("Dynamic Designs Invoice.xlsx",usecols=cols)

snapshot = data["InvoiceDate"].max() # the last day is our max date
PRESENT = snapshot + pd.Timedelta(days=1) # adding 1 day to the max date

data= data[pd.notnull(data['CustomerID'])]

data = data[(data['Amount']>0) ] #& (data['InvoiceNo'] == 53181)]

distinct_data = data.groupby(['InvoiceDate', 'InvoiceNo', 'CustomerID', 'Name'])['Amount'].sum().reset_index()

rfm= distinct_data.groupby('Name').agg({'InvoiceDate': lambda date: (PRESENT - date.max()).days,
                                        'InvoiceNo': lambda num: len(num),
                                        'Amount': lambda price: price.sum()})
rfm.columns=['recency','frequency','monetary']

rfm['recency'] = rfm['recency'].astype(int)

rfm['r_quartile'] = pd.qcut(rfm['recency'], q = 4, labels = False, duplicates="drop") #0 soonest, 4 furthest
rfm['f_quartile'] = pd.qcut(rfm['frequency'], q = 4, labels = False, duplicates="drop")
rfm['m_quartile'] = pd.qcut(rfm['monetary'], q = 4, labels = False, duplicates="drop")
rfm['RFM_Score'] = rfm.r_quartile.astype(str)+ rfm.f_quartile.astype(str) + rfm.m_quartile.astype(str)

rfm.to_csv('rfm_analysis.csv', header=True)

#Core - Your Best Customers RFM group 023
#New product introductions
output = rfm[rfm['RFM_Score']=='023'].sort_values('monetary', ascending=False)
print(output)

#High-spending New Customers — This group consists of those customers in 0-1-3. 
#These are customers who transacted only once, but very recently and they spent a lot.
output = rfm[rfm['RFM_Score']=='013'].sort_values('monetary', ascending=False).head()

#Lowest-Spending Active Loyal Customers — This group consists of those customers in segments 0-2-2
#They transacted recently and do so often, but spend the least
output = rfm[rfm['RFM_Score']=='022'].sort_values('monetary', ascending=False).head()

#Churned Best Customers — This segment consists of those customers in groups 1–3–3, 1–4–3, 1–3–4 and 1–4–4
#They transacted frequently and spent a lot, but it’s been a long time since they’ve transacted
output = rfm[rfm['RFM_Score']=='113'].sort_values('monetary', ascending=False).head()


#https://analyticseducator.com/Blog/Customer_Segmentation_Using_RFM_with_Python.html
#https://www.techtarget.com/searchdatamanagement/definition/RFM-analysis#:~:text=What%20is%20RFM%20%28recency%2C%20frequency%2C%20monetary%29%20analysis%3F%20RFM,the%20best%20customers%20and%20perform%20targeted%20marketing%20campaigns.
