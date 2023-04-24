import pandas as pd
import numpy as np
import plotly.express as px
from bs4 import BeautifulSoup
import requests

#merging all domestic csv files in one in pandas
domesticcombined=pd.concat(map(pd.read_csv,['domestic_visitors_2016.csv','domestic_visitors_2017.csv','domestic_visitors_2018.csv','domestic_visitors_2019.csv']),ignore_index=True)
domesticcombined=domesticcombined.dropna()

#merging all foreign csv files in one in pandas
foreigncombined=pd.concat(map(pd.read_csv,['foreign_visitors_2016.csv','foreign_visitors_2017.csv','foreign_visitors_2018.csv','foreign_visitors_2019.csv']),ignore_index=True)

foreigncombined=foreigncombined.dropna()
foreigncombined['visitors']=pd.to_numeric(foreigncombined['visitors'],errors='coerce')
#research questions
#Q1.top 10 districts with highest no of domestic visitors
domesticcombined.head()
dcsum=domesticcombined[["district","visitors"]]
#float value only for domestic data
floatvalues=pd.to_numeric(dcsum['visitors'],errors='coerce')
dcsum['visitorsnostd']=floatvalues.values
dcsum=dcsum.groupby(['district'])['visitorsnostd'].sum()

dcsum=pd.DataFrame({'district':dcsum.index,'visitorsno':dcsum.values})
dcsum=dcsum.sort_values(by='visitorsno',ascending=False)
dcsum=dcsum.head(10)
fig=px.funnel(dcsum,y='district',x='visitorsno',template='plotly_white',color='visitorsno').update_layout(font=dict(size=25),showlegend=False)
fig.show()


#Q2. top 3 districts with highest annual growth
#domestic value
annualg=domesticcombined[["district","year","visitors"]]
annualg["visitors"]=floatvalues.values
annualg=annualg.dropna()
cagrbegval=annualg[annualg.year==2016]
cagrbegval=cagrbegval.groupby(['year', 'district'], as_index=False)['visitors'].sum()
cagrbegval=pd.DataFrame({'year':cagrbegval['year'],'district':cagrbegval['district'],'visitors':cagrbegval['visitors']})
cagrbegval.set_index('district',inplace=True)
cagrendval=annualg[annualg.year==2019]
cagrendval=cagrendval.groupby(['year', 'district'], as_index=False)['visitors'].sum()
cagrendval=pd.DataFrame({'year':cagrendval['year'],'district':cagrendval['district'],'visitors':cagrendval['visitors']})
cagrendval.set_index('district',inplace=True)
cagrendval=cagrendval.drop(["Mulugu","Narayanapet"])

cagr=pow(cagrendval['visitors']/cagrbegval['visitors'],1/3)-1
cagr=cagr*100.0
cagrdf=pd.DataFrame({'District':cagr.index,'CAGR':cagr.values})
cagrdf=cagrdf.drop(index=[10,17,24])
cagrdfdesc=cagrdf.sort_values(by='CAGR',ascending=False)
#top 3 districts with highest domestic cagr
cagrdfdesc=cagrdfdesc.head(3)
cagrfig=px.bar(cagrdfdesc,x='District',y='CAGR')
cagrfig.show()

#foreign value
foreignannualg=foreigncombined[["district","year","visitors"]]
cagrforthree=foreignannualg[foreignannualg.year==2016]
cagrforthree=cagrforthree.groupby(['year', 'district'], as_index=False)['visitors'].sum()
cagrforthree=pd.DataFrame({'year':cagrforthree['year'],'district':cagrforthree['district'],'visitors':cagrforthree['visitors']})
cagrforthree.set_index('district',inplace=True)

cagrend=foreignannualg[foreignannualg.year==2019]
cagrend=cagrend.groupby(['year', 'district'], as_index=False)['visitors'].sum()
cagrend=pd.DataFrame({'year':cagrend['year'],'district':cagrend['district'],'visitors':cagrend['visitors']})
cagrend.set_index('district',inplace=True)


print(cagrend)

cagrfor=pow(cagrend['visitors']/cagrforthree['visitors'],1/3)-1
cagrfor=cagrfor*100.0
cagrfordf=pd.DataFrame({'District':cagrfor.index,'CAGR':cagrfor.values})
cagrfordf.replace([np.inf, -np.inf], np.nan, inplace=True)
cagrfordf.dropna(inplace=True)
cagrfordfdesc=cagrfordf.sort_values(by='CAGR',ascending=False)
cagrfordfdesc=cagrfordfdesc.head(3)

#top 3 districts with highest foreign cagr
cagrforfig=px.bar(cagrfordfdesc,x="District",y='CAGR')
cagrfig.show()

#combined highest cagr
combined=[cagrdfdesc,cagrfordfdesc]
comcagr=pd.concat(combined)
comcagr['Type']=['Domestic','Domestic','Domestic','Foreign','Foreign','Foreign']
comcagrfig=px.bar(comcagr,x='District',y='CAGR',color='Type',template='plotly_white',text_auto=True).update_layout(font=dict(size=25))
comcagrfig.show()

#Q3.top 3 districts with lowest cgr
#domestic value
cagrdfasc=cagrdf.sort_values(by='CAGR',ascending=True)
cagrdfasc=cagrdfasc.head(3)
cagrasc=px.bar(cagrdfasc,x='District',y='CAGR')
cagrasc.show()

#top 3 districts with lowest foreign cagr
cagrforasc=cagrfordf.sort_values(by='CAGR',ascending=True)
cagrforasc=cagrforasc.head(3)
forascbar=px.bar(cagrforasc,x='District',y='CAGR')
forascbar.show()

#combined lowest cagr
combinedasc=[cagrdfasc,cagrforasc]
comcagrasc=pd.concat(combinedasc)
comcagrasc['Type']=['Domestic','Domestic','Domestic','Foreign','Foreign','Foreign']
comcagrascfig=px.bar(comcagrasc,x='District',y='CAGR',color='Type',template='plotly_white',text_auto=True).update_layout(font=dict(size=25))
comcagrascfig.show()

#Q4 peak and low season months for hyderabad district
#domestic value
hyderabaddata=domesticcombined[["district","month","visitors"]]
hyderabaddata['visitors']=floatvalues.values
hyderabaddata=hyderabaddata[hyderabaddata['district']=='Hyderabad']
hyderabaddata=hyderabaddata.groupby('month')['visitors'].mean()
hyderabaddata=pd.DataFrame({'month':hyderabaddata.index,'visitors':hyderabaddata.values})
hyderabaddata=hyderabaddata.sort_values(by=['month'])
hyderabaddata['monthdate']=pd.to_datetime(hyderabaddata['month'],format='%B',errors='coerce')
hyderabaddata['monthdate']=hyderabaddata['monthdate'].dt.month
hyderabaddata=hyderabaddata.sort_values(by=['monthdate'])
hyddomesticgraph=px.line(hyderabaddata,x='month',y='visitors')
hyddomesticgraph.show()


#foreign value(tbc)
hyderabadfordata=foreigncombined[["district","month","visitors"]]
hyderabadfordata=hyderabadfordata[hyderabadfordata['district']=='Hyderabad']
hyderabadfordata=hyderabadfordata.groupby('month')['visitors'].mean()
hyderabadfordata=pd.DataFrame({'month':hyderabadfordata.index,'visitors':hyderabadfordata.values})
hyderabadfordata=hyderabadfordata.sort_values(by=['month'])
hyderabadfordata['monthdate']=pd.to_datetime(hyderabadfordata['month'],format='%B',errors='coerce')
hyderabadfordata['monthdate']=hyderabadfordata['monthdate'].dt.month
hyderabadfordata=hyderabadfordata.sort_values(by=['monthdate'])
hydforeigngraph=px.line(hyderabadfordata,x='month',y='visitors')
hydforeigngraph.show()

#combined value for q4
comhyd=[hyderabaddata,hyderabadfordata]
comhyd=pd.concat(comhyd)
comhyd['Type']=['Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign']
fig=px.area(comhyd,x='month',y='visitors',color='Type',template='plotly_white').update_layout(font=dict(size=25))
fig.show()


#Q5.top and bottom 3 districts with high domestic to foreign tourist ratio
domesticvisitors=domesticcombined[['district','visitors']]
foreignvisitors=foreigncombined[['district','visitors']]
domesticvisitors['visitors']=floatvalues.values
domesticvisitors.rename(columns={'visitors':'domesticvisitors'},inplace=True)
foreignvisitors.rename(columns={'visitors':'foreignvisitors'},inplace=True)
domesticvisitors=domesticvisitors.groupby(['district'])['domesticvisitors'].sum()
foreignvisitors=foreignvisitors.groupby(['district'])['foreignvisitors'].sum()
dtofratio=domesticvisitors.values/foreignvisitors.values
dtofratiodf=pd.DataFrame({'District':domesticvisitors.index,'dtofratio':dtofratio})
dtofratiodf.replace([np.inf, -np.inf], np.nan, inplace=True)
dtofratiodf.dropna(inplace=True)
dtofratiodf['dtofratio']=dtofratiodf['dtofratio'].round(decimals=2)
dtofratiodf=dtofratiodf.sort_values(by=['dtofratio'],ascending=False)
topthree=dtofratiodf.head(3)
bottomthree=dtofratiodf.iloc[-3:]
dtoffig=px.pie(topthree,values='dtofratio',names='District',hole=.3,color_discrete_sequence=px.colors.sequential.OrRd_r).update_layout(font=dict(size=25))
dtoffig.show()

dtofflast3=px.pie(bottomthree,values='dtofratio',names='District',hole=.3,color_discrete_sequence=px.colors.sequential.Darkmint).update_layout(font=dict(size=25))
dtofflast3.show()


#Q6 ptfratio
populus2011=pd.read_csv('Demographics.csv')
url='https://www.indiacensus.net/states/telangana'
r=requests.get(url)
soup=BeautifulSoup(r.content)
populus23=[]
table=soup.select('table.pincode-tbl')[4]
for el in table.find_all("div", attrs={"class":"txt-right"}):
    populus23.append(el.get_text())

populus23.pop(0)
populus23=populus23[1::2]
populus23=[int(s.replace(',','')) for s in populus23]
populus23.pop(16)
populus23.pop(19)
populus2011['est._pop_23']=populus23
populus2011['growthrateperyear']=((populus2011['est._pop_23']-populus2011['Total'])/populus2011['Total'])*100/12
populus2011['est._pop_19']=populus2011['Total']*(1+populus2011['growthrateperyear']/100*8)
populus2011['est._pop_19']=populus2011['est._pop_19'].round(decimals=2)
populus2011.drop(25,inplace=True)

dv=domesticcombined[['year','district','visitors']]
fv=foreigncombined[['year','district','visitors']]
dv['visitors']=floatvalues.values
dv=dv[dv['year']==2019]
fv=fv[fv['year']==2019]
dv=dv.groupby(['district'])['visitors'].sum()
fv=fv.groupby(['district'])['visitors'].sum()

dv.drop(['Mulugu','Narayanapet'],inplace=True)
fv.drop(['Mulugu','Narayanpet','Suryapet'],inplace=True)

print(len(dv))

totaltourists=dv.values+fv.values
populus2011['totaltourists']=totaltourists
populus2011['totaltourists']=populus2011['totaltourists'].round(decimals=2)
populus2011['footfall_ratio']=populus2011['totaltourists']/populus2011['est._pop_19']
populus2011=populus2011.sort_values(by='footfall_ratio',ascending=False)
populus2011=populus2011[populus2011['footfall_ratio']>0.00]
populustop5=populus2011.head(5)
populustail=populus2011.tail(5)

top5fig=px.bar(populustop5,x='footfall_ratio',y='Districts')
top5fig.show()

tail5fig=px.bar(populustail,x='footfall_ratio',y='Districts')
tail5fig.show()

#combined for Q6
com5pd=[populustop5,populustail]
com5pd=pd.concat(com5pd)
com5pd['footfall_ratio']=com5pd['footfall_ratio'].astype(float).round(decimals=4)
com5pdfig=px.line(com5pd,x='Districts',y='footfall_ratio',text='footfall_ratio',template='plotly_white',color_discrete_sequence=px.colors.sequential.Greens_r).update_layout(font=dict(size=30)).update_traces(line=dict(width=5))
com5pdfig.show()


#Q7projected no of d and f tourists in hyderabad in 2025
#domestic no
predictedvalues=pd.DataFrame({'category':['Domestic value','Foreign value'],'values':['','']})
yearlyprojection=pd.DataFrame({'Year':[2019,2020,2021,2022,2023,2024,2025],'Domestic Values':['','','','','','',''],'Foreign Values':['','','','','','','']})
dv25=domesticcombined[['district','year','visitors']]
dv25['visitors']=floatvalues.values
fv25=foreigncombined[['district','year','visitors']]
dv25=dv25.groupby(['district','year'],as_index=False)['visitors'].sum()
dv25=pd.DataFrame({'district':dv25['district'],'year':dv25['year'],'visitors':dv25['visitors']})
dv25=dv25[dv25.district == 'Hyderabad']
dv2519val=dv25[dv25['year']==2019]
dv2516val=dv25[dv25['year']==2016]
cagrdv=(pow(dv2519val['visitors'].values/dv2516val['visitors'].values,1/3)-1)*100
predictedvalues['values'][0]=dv2519val['visitors'].values*(cagrdv/100+1)*(pow(cagrdv/100+1,6))
yearlyprojection['Domestic Values']=[dv2519val['visitors'].values,dv2519val['visitors'].values*(cagrdv/100+1)*(pow(cagrdv/100+1,1)),dv2519val['visitors'].values*(cagrdv/100+1)*(pow(cagrdv/100+1,2)),dv2519val['visitors'].values*(cagrdv/100+1)*(pow(cagrdv/100+1,3)),dv2519val['visitors'].values*(cagrdv/100+1)*(pow(cagrdv/100+1,4)),dv2519val['visitors'].values*(cagrdv/100+1)*(pow(cagrdv/100+1,5)),dv2519val['visitors'].values*(cagrdv/100+1)*(pow(cagrdv/100+1,6))]


#foreign no
fv25=fv25.groupby(['district','year'],as_index=False)['visitors'].sum()
fv25=pd.DataFrame({'district':fv25['district'],'year':fv25['year'],'visitors':fv25['visitors']})
fv25=fv25[fv25.district == 'Hyderabad']
fv2519val=fv25[fv25['year']==2019]
fv2516val=fv25[fv25['year']==2016]
cagrfv=(pow(fv2519val['visitors'].values/fv2516val['visitors'].values,1/3)-1)*100
predictedvalues['values'][1]=fv2519val['visitors'].values*(pow(cagrfv/100+1,6))
yearlyprojection['Foreign Values']=[fv2519val['visitors'].values,fv2519val['visitors'].values*(cagrfv/100+1)*(pow(cagrfv/100+1,1)),fv2519val['visitors'].values*(cagrfv/100+1)*(pow(cagrfv/100+1,2)),fv2519val['visitors'].values*(cagrfv/100+1)*(pow(cagrfv/100+1,3)),fv2519val['visitors'].values*(cagrfv/100+1)*(pow(cagrfv/100+1,4)),fv2519val['visitors'].values*(cagrfv/100+1)*(pow(cagrfv/100+1,5)),fv2519val['visitors'].values*(cagrfv/100+1)*(pow(cagrfv/100+1,6))]



predictedvalues['values']=predictedvalues['values'].astype(float).round(decimals=2)
predictvalbar=px.bar(predictedvalues,x='category',y='values',template='plotly_white',color='category',text_auto=True).update_layout(font=dict(size=25),showlegend=False)
predictvalbar.show()


#Q8 projected revenue
foravrrev=5600.00
domavrrev=1200.00
#2019 values
dv2519val['2019revenue']=(dv2519val['visitors']*domavrrev)
fv2519val['2019revenue']=(fv2519val['visitors']*foravrrev)
total19rev=dv2519val['2019revenue']+fv2519val['2019revenue']
#2025 values
dv2519val['2025revenue']=(predictedvalues['values'][0]*domavrrev)
fv2519val['2025revenue']=(predictedvalues['values'][1]*foravrrev)
total19predval=dv2519val['2025revenue']+fv2519val['2025revenue']
projrev=pd.DataFrame({'category':[2019,2025],'values':[total19rev.values,total19predval.values]})
projrev['values']=projrev['values'].astype(float).round(decimals=2)
#total value projection graph
fig=px.line(projrev,x='category',y='values')
fig.show()
yearlyprojection['Domestic Revenue']=yearlyprojection['Domestic Values'].values*domavrrev
yearlyprojection['Foreign Revenue']=yearlyprojection['Foreign Values'].values*foravrrev
yearlyprojection['Domestic Revenue']=yearlyprojection['Domestic Revenue'].astype(float).round(decimals=2)
yearlyprojection['Foreign Revenue']=yearlyprojection['Foreign Revenue'].astype(float).round(decimals=2)
yearlyprojection['Foreign Values']=yearlyprojection['Foreign Values'].astype(float).round(decimals=2)
yearlyprojection['Domestic Values']=yearlyprojection['Domestic Values'].astype(float).round(decimals=2)
#combined value
domesticprojection=yearlyprojection['Domestic Revenue']
foreignprojection=yearlyprojection['Foreign Revenue']
combinedproj=[domesticprojection,foreignprojection]
combinedproj=pd.concat(combinedproj)
combinedproj=pd.DataFrame({'Category':['Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Domestic','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign','Foreign'],'Year':[2019,2020,2021,2022,2023,2024,2025,2019,2020,2021,2022,2023,2024,2025],'Revenue':combinedproj.values})
fig=px.line(combinedproj,x='Year',y='Revenue',color='Category',template='plotly_white',color_discrete_sequence=px.colors.sequential.Blackbody).update_layout(font=dict(size=25)).update_traces(line=dict(width=5))
fig.show()








