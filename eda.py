import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def eda(cleanData):
    print(list(cleanData))
    casesByWinningPartyHist(cleanData)
    casesPerCapitaHist(cleanData)
    casesVsDeathsScatter(cleanData)
    maskUsage(cleanData)


def casesByWinningPartyHist(data):
    dataPerCapita = data
    dataPerCapita["cases_per_capita"] = dataPerCapita["cases"]/dataPerCapita["TotalPop"]
    trumpData = dataPerCapita[dataPerCapita["votes20_Donald_Trump"] > dataPerCapita["votes20_Joe_Biden"]]["cases_per_capita"]
    bidenData = dataPerCapita[dataPerCapita["votes20_Donald_Trump"] < dataPerCapita["votes20_Joe_Biden"]]["cases_per_capita"]
    bins = 50
    plt.hist(trumpData, bins=bins,alpha=0.5, label="Trump",color="red")
    plt.hist(bidenData, bins=bins,alpha=0.5, label="Biden",color="blue")
    plt.title('County COVID Cases Per Capita by Winner')
    plt.xlabel('COVID Cases by % of Population')
    plt.ylabel('Number of Counties')
    plt.legend()
    plt.show()

def casesPerCapitaHist(data):
    dataPerCapita = data
    dataPerCapita["cases_per_capita"] = dataPerCapita["cases"]/dataPerCapita["TotalPop"]
    casesData = dataPerCapita["cases_per_capita"]

    plt.boxplot(casesData.dropna())
    plt.title('County COVID Cases Per Capita Boxplot')
    plt.xlabel('US Counties')
    plt.ylabel('COVID Cases Per Capita')
    plt.show()
    # Plot as histogram

    # bins = 30
    # plt.hist(casesData, bins=bins)
    # plt.title('County COVID Cases Per Capita')
    # plt.xlabel('COVID Cases by % of Population')
    # plt.ylabel('Number of Counties')
    # plt.show()

    
    


def casesVsDeathsScatter(data):
    casesData = data["cases"]
    deathsData = data["deaths"]
    plt.scatter(casesData, deathsData)
    plt.title('COVID Cases vs Deaths by County')
    plt.xlabel('Cases')
    plt.ylabel('Deaths')
    plt.show()

def maskUsage(data):
    maskCategories = ["NEVER", "RARELY", "SOMETIMES", "FREQUENTLY", "ALWAYS"]
    trumpData = []
    bidenData = []
    for c in maskCategories:
        trumpData.append(data[data["votes20_Donald_Trump"] > data["votes20_Joe_Biden"]][c].mean()*100)
        bidenData.append(data[data["votes20_Donald_Trump"] < data["votes20_Joe_Biden"]][c].mean()*100)
    x = np.arange(len(maskCategories))  # the label locations
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(x-width/2, trumpData, width, label="Trump", color="red")
    ax.bar(x+width/2, bidenData, width, label="Biden", color="blue")
    ax.set_xticks(x)
    ax.set_xticklabels(maskCategories)
    ax.set_ylabel('Percentage')
    plt.title('Average Mask Usage in Trump vs Biden Counties')
    ax.legend()
    plt.show()