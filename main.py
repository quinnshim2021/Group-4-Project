from clean import *
from eda import eda
from modeling import *
import pandas
import plotly
import plotly.graph_objects as go
import plotly.express as px
from urllib.request import urlopen
import json

def runModeling(cleaned):
    # pairing to test
    pairings = [
        ["percent_Biden", "cases_pc"],
        ["percent_Trump", "cases_pc"],
        ["percent_Biden", "deaths_pc"],
        ["percent_Trump", "deaths_pc"],
        ["percent_Biden", "deaths_over_cases"],
        ["percent_Trump", "deaths_over_cases"],
        ["percent_Biden", "frequent_mask_use"],
        ["percent_Biden", "infrequent_mask_use"],
        ["percent_Trump", "frequent_mask_use"],
        ["percent_Trump", "infrequent_mask_use"]
    ]

    linearRegression(cleaned, "cases_pc", "percent_Trump")
    f = open("modelingResults.txt", "a")  # append mode 
    for pair in pairings:
        f.write(pearson(cleaned, pair[1], pair[0]))
        f.write(spearman(cleaned, pair[1], pair[0]))
        f.write(linearRegression(cleaned, pair[1], pair[0]))
        f.write('\n\n')
    f.close()
    
    modeling(cleaned)

def draw(cleaned, category):
    cleaned['infrequent_mask_use'].astype(float)
    cleaned['fips'].astype(str)

    # from https://plotly.com/python/mapbox-county-choropleth/
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    fig =  px.choropleth_mapbox(cleaned, geojson=counties, locations='fips', color=category, # trump or infrequent mask use
                           color_continuous_scale="Viridis",
                           range_color=(0, 1), # percentage, so only need 0 through 1
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()


# first grabs data, then cleans, then does eda
def main():
    # get data
    mask_data, raw_covid_data, raw_counties_election = createRaws()

    # clean data
    mask_data = cleanMaskData(mask_data)
    covid_data = cleanCovidData(raw_covid_data)
    election_data = cleanElectionData(raw_counties_election)
    # merge data
    cleaned = mergeData(mask_data, covid_data, election_data)

    # modeling
    runModeling(cleaned)

    # visualization
    draw(cleaned, "infrequent_mask_use")
    draw(cleaned, "percent_Trump")

    # # run eda
    eda(cleaned)

if __name__ == '__main__':
    main()
