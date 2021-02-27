from collections import Counter
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def modeling(data):
    # print(chiSquareDeaths(data))
    # print(chiSquareCases(data))
    # knnPlot(data)
    knn(data)
    

def chiSquareCases(data):
    dataPerCapita = data
    dataPerCapita["cases_per_capita"] = dataPerCapita["cases"]/dataPerCapita["TotalPop"]
    avgCaseRate = dataPerCapita["cases_per_capita"].mean()
    trumpAndAbove = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] >= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["cases_per_capita"] >= avgCaseRate)])
    trumpAndBelow = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] >= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["cases_per_capita"] < avgCaseRate)])
    bidenAndAbove = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] <= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["cases_per_capita"] >= avgCaseRate)])
    bidenAndBelow = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] <= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["cases_per_capita"] < avgCaseRate)])
    obs = np.array([[trumpAndAbove, trumpAndBelow], [bidenAndAbove, bidenAndBelow]])
    return (chi2_contingency(obs))

def chiSquareDeaths(data):
    dataPerCapita = data
    dataPerCapita["deaths_per_cases"] = dataPerCapita["deaths"]/dataPerCapita["cases"]
    avgDeathRate = dataPerCapita["deaths_per_cases"].mean()
    trumpAndAbove = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] >= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["deaths_per_cases"] >= avgDeathRate)])
    trumpAndBelow = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] >= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["deaths_per_cases"] < avgDeathRate)])
    bidenAndAbove = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] <= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["deaths_per_cases"] >= avgDeathRate)])
    bidenAndBelow = len(dataPerCapita[(dataPerCapita["votes20_Donald_Trump"] <= dataPerCapita["votes20_Joe_Biden"]) & (dataPerCapita["deaths_per_cases"] < avgDeathRate)])
    obs = np.array([[trumpAndAbove, trumpAndBelow], [bidenAndAbove, bidenAndBelow]])
    return (chi2_contingency(obs))

def knnPlot(data):
    data = data.dropna(how='any',axis=0) 
    x = (data["cases"]/data["TotalPop"]).to_numpy()
    y = (data["deaths"]/data["cases"]).to_numpy()
    # x = data["cases"].to_numpy()
    # y = data["deaths"].to_numpy()
    print(x)
    print(y)
    # group = ["trump" if x["votes20_Donald_Trump"] > x["votes20_Joe_Biden"] else "biden" for x in data]
    group = []
    for index, row in data.iterrows():
        if row["votes20_Donald_Trump"] > row["votes20_Joe_Biden"]:
            group.append(1)
        elif row["votes20_Donald_Trump"] < row["votes20_Joe_Biden"]:
            group.append(2)
        else:
            group.append(3)
    cdict = {1: "red", 2: "blue", 3: "grey"}
    fig, ax = plt.subplots()
    for g in np.unique(group):
        ix = np.where(group == g)
        ax.scatter(x[ix], y[ix], c = cdict[g],label = g)
    ax.legend()
    plt.show()

def knn(data):
    df = data.dropna(how='any',axis=0) 
    x = df["cases"]
    y = df["deaths"]
    # x = (data["cases"]/data["TotalPop"])
    # y = (data["deaths"]/data["cases"])
    combined = pd.concat([x,y], axis=1).to_numpy()
    group = []
    for index, row in df.iterrows():
        if row["votes20_Donald_Trump"] > row["votes20_Joe_Biden"]:
            group.append(1)
        elif row["votes20_Donald_Trump"] < row["votes20_Joe_Biden"]:
            group.append(2)
        else:
            group.append(3)

    
    X_train, X_test, y_train, y_test = train_test_split(combined, group, test_size=0.20)
    
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    # print(y_test-y_pred)
    # print(len(y_test))
    # sample = [1]*617
    # print(y_pred)
    # print(y_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))