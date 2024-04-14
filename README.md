import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import sql
import mysql.connector
import json
import requests


#DataFrame creation

#sql connection
mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        port=3306,
        password='Umarani@6383',
        database='phonepy_data')
cursor=mydb.cursor()

#aggre_transaction

cursor.execute("select * from aggregated_transaction")

table1 =cursor.fetchall()

Aggre_transaction=pd.DataFrame(table1, columns=("States","Years","Quarter","Transaction_type","Transation_count","Transaction_amount"))

mydb.commit()

#aggre_user

cursor.execute("select * from aggregated_user")

table2 =cursor.fetchall()

aggregated_user=pd.DataFrame(table2, columns=("States","Years","Quarter","Transaction_type","Transation_count","Transaction_amount"))

mydb.commit()

#map transacation

cursor.execute("select * from map_transation")

table3 =cursor.fetchall()

map_transaction=pd.DataFrame(table3, columns=("States", "Years", "Quarter" , "Districts",  "Transation_count" , "Transaction_amount" ))
mydb.commit()

                            
#map user


cursor.execute("select * from map_user")

table4 =cursor.fetchall()

map_user=pd.DataFrame(table4, columns=("States", "Years", "Quarter" , "Districts",  "RegisteredUsers" , "AppOpens" ))
mydb.commit() 

#top transaction

cursor.execute("select * from top_transaction")

table5 =cursor.fetchall()

top_transaction=pd.DataFrame(table5, columns=("States", "Years", "Quarter" , "Pincodes",  "Transation_count" , "Transaction_amount" ))
mydb.commit() 

#top user

cursor.execute("select * from top_user")

table6 =cursor.fetchall()

top_user=pd.DataFrame(table6, columns=("States", "Years", "Quarter" , "Pincodes",  "RegisteredUsers" ))
mydb.commit() 






                            
        
                            
                            






def Transaction_amount_count_Y(df,year):

    tacy = df[df["Years"] ==year]

    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("States")[["Transation_count","Transaction_amount"]].sum()

    tacyg.reset_index(inplace=True)

    fig_amount =px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Blues)
    st.plotly_chart(fig_amount)

    fig_count=px.bar(tacyg, x="States", y="Transation_count", title=f"{year} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Bluered_r)
    st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for future in data1["features"]:
        states_name.append(future["properties"]["ST_NM"])

    states_name.sort()

    fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                              color="Transaction_amount",color_continuous_scale="Rainbow",
                               range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max() ),
                               hover_name="States",title=f"{year} TRANSACTION AMOUNT",fitbounds="locations")
    
    fig_india_1.update_geos(visible=False)
    
    st.plotly_chart(fig_india_1)

    fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                              color="Transation_count",color_continuous_scale="Rainbow",
                               range_color=(tacyg["Transation_count"].min(),tacyg["Transation_count"].max() ),
                               hover_name="States",title=f"{year} TRANSACTION COUNT ",fitbounds="locations")
    
    fig_india_2.update_geos(visible=False)
    
    st.plotly_chart(fig_india_2)


def top_chart_tran(table_name):
    
        mydb = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                port=3306,
                password='Umarani@6383',
                database='phonepy_data')
        cursor=mydb.cursor()
        #plot1
        query1=f'''select States,sum(Transaction_amount) as Transaction_amount
                from {table_name}
                group by States
                order by Transaction_amount desc
                limit 10;'''

        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1,columns=("States","Transaction_amount"))

        col1,col2=st.columns(2)
        with col1:
            fig_amount =px.bar(df1, x="States", y="Transaction_amount", title=f"TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Magma)
            st.plotly_chart(fig_amount)

        #plot2

        query2=f'''select States,sum(Transaction_amount) as Transaction_amount
                        from {table_name}
                        group by States
                        order by Transaction_amount 
                        limit 10;'''
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table2,columns=("States","Transaction_amount"))

        with col2:
            fig_amount2 =px.bar(df2, x="States", y="Transaction_amount", title=f"TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Purples)
            st.plotly_chart(fig_amount2)

        #plot3

        query3=f'''select States,avg(Transaction_amount) as Transaction_amount
                        from {table_name}
                        group by States
                        order by Transaction_amount;'''
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3,columns=("States","Transaction_amount"))

        fig_amount3 =px.box(df3, x="States", y="Transaction_amount", title=f"TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_amount3)


        #transaction count 
def top_chart_transation_count(table_name): 
    
        mydb = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                port=3306,
                password='Umarani@6383',
                database='phonepy_data')
        cursor=mydb.cursor()
        #plot1
        query1=f'''select States,sum(Transation_count) as Transation_count
                        from aggregated_transaction
                        group by States
                        order by Transation_count desc
                        limit 10;'''

        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1,columns=("States","Transation_count"))
        fig_amount =px.line(df1, x="States", y="Transation_count", title=f"TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Magma)
        st.plotly_chart(fig_amount)

        #plot2

        query2=f'''select States,sum(Transation_count) as Transation_count
                        from {table_name}
                        group by States
                        order by Transation_count 
                        limit 10;'''
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table2,columns=("States","Transation_count"))
        fig_amount1 =px.line(df2, x="States", y="Transation_count", title=f"TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Purples)
        st.plotly_chart(fig_amount1)

        #plot3

        query3=f'''select States,avg(Transation_count) as Transation_count
                        from {table_name}
                        group by States
                        order by Transation_count;'''
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3,columns=("States","Transation_count"))
        fig_amount3 =px.bar(df3, x="States", y="Transation_count", title=f"TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_amount3)


def map_users(year):
    MU=map_user[map_user["Years"]==year]
    MU.reset_index(drop=True,inplace=True)
    mug=MU.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    mug.reset_index(inplace=True)
    fig_line_1=px.line(mug,x="States",y=["RegisteredUsers","AppOpens"],title="REGISTEREDUSERS",markers=True)
    st.plotly_chart(fig_line_1)

    return mug     

    

#streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select=option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select=="HOME":
    
    col1,col2=st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA's BEST TRANSACTION APP")
        st.markdown("phonepe is an digital payments and finacial technology company")
        st.write("****features****")
        st.write("****credit and debit card linking****")
        st.write("***Money storage***")
        st.download_button("DOWNLOAD THE APP NOW","https://www.phonepe.com/app-download/")


elif select=="DATA EXPLORATION":

    tab1, tab2, tab3 =st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        
        method = st.radio("Select the Method", ["Transaction Analysis", "User Analysis"])

        if method == "Transaction Analysis":
             
             col1,col2=st.columns(2)
             with col1:

                years=st.slider("Select the year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
             Transaction_amount_count_Y(Aggre_transaction, years)
        
        elif method == "User Analysis":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the year",aggregated_user["Years"].min(),aggregated_user["Years"].max(),aggregated_user["Years"].min())
            Transaction_amount_count_Y(aggregated_user, years)
        
    
    
    with tab2:

        method2 = st.radio("Select the Method", ["Map Trasaction","Map User "])

        if method2 == "Map Trasaction":
            col3,col4=st.columns(2)
            with col3:
             #map_transaction

             year1=st.slider("Select the year_MT",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
            Transaction_amount_count_Y(map_transaction, years)
        

        elif method2 == "Map User":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the year",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
            map_user_y=map_users(map_user, years)

    with tab3:

        method3 = st.radio("Select the Method", ["Top Trasaction","Top User "])

        if method3 == "Top Trasaction":
            col5,col6=st.columns(2)
            with col5:
             #top_transaction

              year=st.slider("Select the year_TT",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
            Transaction_amount_count_Y(top_transaction, years)
        elif method3 == "Top User":
            pass


elif select== "TOP CHARTS":
    
    question = st.selectbox("Select the Question",["1. Transation Amount and Count of Aggregated Trnsation",
                                                   "2. Transation Amount and Count of Map Trnsation", 
                                                   "3. Transation Amount and Count of Top Trnsation",  
                                                   ])
    
    if question == "1. Transation Amount and Count of Aggregated Trnsation":
       
        top_chart_tran("aggregated_transaction")
        top_chart_transation_count("aggregated_transaction")
    

    elif question =="2. Transation Amount and Count of Map Trnsation":
        
        top_chart_tran("map_transation")
        top_chart_transation_count("map_transation")

    elif question =="3. Transation Amount and Count of Top Trnsation":

        top_chart_tran("top_transaction")
        top_chart_transation_count("top_transaction")
    
    



 # Phonepe-Pulse-Data-Visualization
Phonepe Pulse Data Visualization and Exploration: A User-Friendly Tool Using Streamlit and Plotly
