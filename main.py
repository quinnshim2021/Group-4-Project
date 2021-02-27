from clean import *
from eda import eda
from modeling import *
import pandas

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
    for pair in pairings:
        pearson(cleaned, pair[1], pair[0])
        spearman(cleaned, pair[1], pair[0])
        linearRegression(cleaned, pair[1], pair[0])
    
    modeling(cleaned)


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

    # run eda
    #eda(cleaned)

if __name__ == '__main__':
    main()
