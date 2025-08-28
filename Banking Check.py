'''
Author: Iraj Junaid
Date: 08/27/2025
Description: This script performs data analysis on banking data, including data merging, cleaning, and visualizations.

'''
## Import Libraries
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#Making all joins between csv's first

df = pd.read_csv('banking.csv')
relationships = pd.read_csv('banking-relationships.csv')
clients = pd.read_csv('banking-clients.csv')
gender = pd.read_csv('gender.csv')
advisors = pd.read_csv('investment-advisors.csv')  

# Create Joins

df = df.merge(gender, on='GenderID', how='left')
df = df.merge(advisors, left_on='IAId', right_on='AdvisorID', how='left')
df = df.merge(relationships, left_on='BRId', right_on='RelationshipID', how='left') 
df = df.merge(clients, on='Name', how='left')

#Create connection to SQL database
conn = sqlite3.connect('bank_case.db')
mouse = conn.cursor()

# Save DataFrames to SQL tables
df.to_sql("Bankings", conn, if_exists='replace', index=False)
relationships.to_sql("Relationships", conn, if_exists='replace', index=False)
clients.to_sql("Clients", conn, if_exists='replace', index=False )
gender.to_sql("Genders", conn, if_exists='replace', index=False )
advisors.to_sql("Advisors", conn, if_exists='replace', index=False )

# Verify the number of records in each table in Relationships (Test)
mouse.execute("SELECT COUNT(*) FROM Relationships")
print("Number of Relationships:", mouse.fetchone()[0])

query = "SELECT RelationshipID,ClientID,AdvisorID,StartDate,EndDate FROM Relationships LIMIT 5;"
res = pd.read_sql(query, conn)
df.info() #print summary of dataframe

print(df.describe()) # Print statistical summary of dataframe

print(df.shape) #Print shape of dataframe

print(df.isnull().sum()) # Print number of null values in each column

print(df.columns) #debug check; pring all column names from df (banking.csv)
bins = [0, 100000, 200000, float('inf')] # Define bins for income bands 
labels = ['Low', 'Med', 'High'] # Define labels for income bands
df["Income Band"] = pd.cut(df['Estimated Income'], bins=bins, labels=labels,include_lowest=True) # Create Income Band column based on Estimated Income
df['Income Band'].value_counts().plot(kind='bar')  # Plot value counts of Income Band
plt.show() # Show plot

# Visualizations

categorical_cols = df[["Income Band", "BRId", "GenderID_y","IAId", "Amount of Credit Cards", "Nationality", "Occupation", "Fee Structure", "Loyalty Classification", "Properties Owned", "Risk Weighting"]].columns

# Show visuals for unique categorical columns
for col in categorical_cols:
    print(f"Value Counts for '{col}':")
    ax = (df[col].value_counts().plot(kind='bar'))
    plt.show()



cols = ["Income Band", "BRId", "GenderID_y","IAId", "Amount of Credit Cards", "Nationality", "Occupation", "Fee Structure", "Loyalty Classification", "Properties Owned", "Risk Weighting"]

# Show count plots for categorical columns (No hue)
for i, predictor in enumerate(cols):
	plt.figure(i)
	sns.countplot(data=df, x=predictor)
	plt.show()

 # show count plots for categorical columns (with hue)
for i, predictor in enumerate(cols):
	plt.figure(i)
	sns.countplot(data=df, x=predictor, hue="GenderID_y")
	plt.show()

# Show histograms for occupation
for col in cols:
	if col == "Occupation":
		continue
	plt.figure(figsize=(8,4))
	sns.histplot(df[col])
	plt.title('Histogram of Occupation Count')
	plt.xlabel(col)
	plt.ylabel("Count")
	plt.show()

# Show histograms for numerical columns with KDE(curve)
numerical_cols = ['Estimated Income', 'Superannuation Savings']
plt.figure(figsize=(8,4))
for i,col in enumerate(numerical_cols):
	plt.subplot(2,1,i+1) 
	sns.histplot(df[col],kde=True)
	plt.title(col)
plt.show()

# Show heatmap for correlation between estimated income and superannuation savings
numerical_cols =  ['Estimated Income', 'Superannuation Savings'] 
correlation_matrix = df[numerical_cols].corr()
plt.figure(figsize=(12,12))
sns.heatmap(correlation_matrix,annot=True, cmap='crest',fmt='.2f')
plt.title("Correlaion matrix")
plt.show()

