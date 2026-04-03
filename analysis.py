
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

def load(file):
 print("Trying to load:", file)
 try:
      data=pd.read_csv(file)
      print("file successfully loaded")
      return data
 except:
    print("error")
    return None

def cleanin(data):
    print("\nCleaning data...")
    data = data.drop_duplicates()

    numeric_cols = data.select_dtypes(include='number').columns
    categorical_cols = data.select_dtypes(include='object').columns


    for col in numeric_cols:
        data[col].fillna(data[col].mean(), inplace=True)

    
    for col in categorical_cols:
        if not data[col].mode().empty:
            data[col].fillna(data[col].mode()[0], inplace=True)

    return data
      
         
         
def analyze_data(data):
          print("\n basic info")
          print(data.info())
          
          print("\n summary statistics ")  
          print(data.describe())
          
          print("\ncategorical analysis")  
          for col in data.select_dtypes(include='object').columns:
              print(f"{col}value counts:")
              print(data[col].value_counts())
         
          print("\n correlation matrix:")
          print(data.corr(numeric_only=True))
         

def visualization(data):
    if not os.path.exists("outputs"):
     os.makedirs("outputs")
    
    print("\n creating visualization: ")
    for col in data.select_dtypes(include='number').columns:
        plt.figure()
        data[col].hist()
        plt.title(f"{col}distribution")
        plt.savefig(f"outputs/{col}_hist.png")
        plt.show()
      
    for col in data.select_dtypes(include='object').columns:
        plt.figure()
        data[col].value_counts().plot(kind='bar')
        plt.title(f"{col}distribution")
        plt.savefig(f"outputs/{col}_bar.png")
        plt.show()

    plt.figure()
    sns.heatmap(data.corr(numeric_only=True),annot=True)
    plt.title("correlation Heatmap")
    plt.savefig(f"outputs/heatmap.png")
    plt.show()

def insights(data):
    print("\n Generating insights...")
    for col in data.select_dtypes(include='number').columns:
        print(f"insights for {col}: ")
        
        print(f"average: {data[col].mean()}")
        print(f"MAXIMUM:{data[col].max()}")
        print(f"MINIMUM: {data[col].min()}")
   
    for col in data.select_dtypes(include='object').columns:
        print(f"insights for {col}: ")

        top=data[col].value_counts().idxmax()
        print(f"most frequent {col}: {top}")
      
    corr = data.corr(numeric_only=True)

    print("\n🔹 Strong Relationships:")
    for col in corr.columns:
        for row in corr.index:
            if col != row and abs(corr.loc[row, col]) > 0.7:
                print(f"{row} and {col} are strongly related")



def save_insights(data):
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    with open("outputs/insights.txt", "w") as f:
        f.write("Data Insights\n\n")

  
        for col in data.select_dtypes(include='number').columns:
            f.write(f"Insights for {col}:\n")
            f.write(f"Average: {data[col].mean()}\n")
            f.write(f"Max: {data[col].max()}\n")
            f.write(f"Min: {data[col].min()}\n\n")

       
        for col in data.select_dtypes(include='object').columns:
            f.write(f"Insights for {col}:\n")
            top = data[col].value_counts().idxmax()
            f.write(f"Most frequent: {top}\n\n")

   
        corr = data.corr(numeric_only=True)

        f.write("Strong Relationships:\n")
        for col in corr.columns:
            for row in corr.index:
                if col != row and abs(corr.loc[row, col]) > 0.7:
                    f.write(f"{row} and {col} are strongly related\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python analysis.py data/file.csv")
        return

    file = sys.argv[1]

    data = load(file)

    if data is not None:
        data = cleanin(data)
        analyze_data(data)
        visualization(data)
        insights(data)
        save_insights(data)


print("PROGRAM STARTED")   

if __name__ == "__main__":
    main()

         
         
