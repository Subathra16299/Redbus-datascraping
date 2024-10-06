#importing libraries
import pandas as pd
import mysql.connector
import numpy as np
# csv to dataframe
df_buses_1=pd.read_csv("df_buses_1.csv")
df_buses_2=pd.read_csv("df_buses_2.csv")
df_buses_3=pd.read_csv("df_buses_3.csv")
df_buses_4=pd.read_csv("df_buses_4.csv")
df_buses_5=pd.read_csv("df_buses_5.csv")
df_buses_6=pd.read_csv("df_buses_6.csv")
df_buses_7=pd.read_csv("df_buses_7.csv")
df_buses_8=pd.read_csv("df_buses_8.csv")
df_buses_9=pd.read_csv("df_buses_9.csv")
df_buses_10=pd.read_csv("df_buses_10.csv")

Final_df=pd.concat([df_buses_1,df_buses_2,df_buses_3,df_buses_4,df_buses_5,df_buses_6,
                    df_buses_7,df_buses_8,df_buses_9,df_buses_10],ignore_index=True)
Final_df

# data about the data
Final_df.info()

#convert prices to numeric
Final_df["Price"]=Final_df["Price"].str.replace("INR","")
Final_df["Price"]=Final_df["Price"].astype(float)
Final_df["Price"].fillna(0)

#convert Ratings to numeric
Final_df["Ratings"]=Final_df["Ratings"].str.replace("New","")
Final_df["Ratings"]=Final_df["Ratings"].str.strip()
Final_df["Ratings"]=Final_df["Ratings"].str.split().str[0]
Final_df["Ratings"] = pd.to_numeric(Final_df["Ratings"], errors='coerce')
Final_df["Ratings"] = Final_df["Ratings"].fillna(0)

# info after the data type change
Final_df.info()


Final_df = Final_df[Final_df["Price"] <= 7000]

# replacing the nan value
Final_df = Final_df.replace({np.nan: None})
#convert float to string for INR
# change dataframe to csv
path=r"D:/Subathra/DataScience/Redbus/Final_busdetails1_df.csv"
Final_df.to_csv(path,index=False)


#sql connection
conn=mysql.connector.connect(host="localhost", user="root", password="Ajith_suba99",database="redbus")
my_cursor = conn.cursor()
my_cursor.execute("CREATE DATABASE IF NOT EXISTS redbus")

# Table Creation
my_cursor.execute('''CREATE TABLE IF NOT EXISTS bus_details(
                  ID INT AUTO_INCREMENT PRIMARY KEY,
                  Bus_name VARCHAR(255) NOT NULL,
                  Bus_type VARCHAR(255) NOT NULL,
                  Start_time VARCHAR(255) NOT NULL,
                  End_time VARCHAR(255) NOT NULL,
                  Total_duration VARCHAR(255) NOT NULL,
                  Price FLOAT NULL,
                  Seats_Available VARCHAR(255) NOT NULL,
                  Ratings Float NULL,
                  Route_link VARCHAR(255) NULL,
                  Route_name VARCHAR(255) NULL
                  )''')
print("Table Created successfully")

# SQL query to insert data into bus_details table
insert_query = '''INSERT INTO bus_details(
                    Bus_name,
                    Bus_type,
                    Start_time,
                    End_time,
                    Total_duration,
                    Price,
                    Seats_Available,
                    Ratings,
                    Route_link,
                    Route_name)
                  VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
data = Final_df.values.tolist()

my_cursor.executemany(insert_query, data)

conn.commit()

print("Values inserted successfully")

