import pandas

# god bless someone did this on a github already
state_symbols = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}

# creates raw dataframes from csv data
def createRaws():
    mask_data = pandas.read_csv('../Data/mask-use-by-county.csv')
    raw_covid_data = pandas.read_csv('../Data/us-counties.csv')
    raw_counties_election = pandas.read_csv('../Data/county_statistics.csv')
    return mask_data, raw_covid_data, raw_counties_election

# only uses county, state, dt votes, jb votes, and total population
# replaces state abbreviations with full state (for merging later)
def cleanElectionData(raw_counties_election):
    counties_election_trimmed = raw_counties_election[['county', 'state', 'votes20_Donald_Trump', 'votes20_Joe_Biden', 'TotalPop']]

    for index, row in counties_election_trimmed.iterrows():
        if row['state'] in state_symbols:
            
            counties_election_trimmed.loc[index, 'state'] = state_symbols[row['state']]

    return counties_election_trimmed.dropna()

# gets covid data for just 11/02/2020 (day before election day)
# casts fips column from float to int
def cleanCovidData(raw_covid_data):
    covid_data = raw_covid_data.loc[raw_covid_data['date'] == '2020-11-02'].drop(columns='date')
    covid_data['fips'] = covid_data['fips'].fillna(0.0).astype(int)
    return covid_data.dropna()

# renames column to be consistent with covid data df
def cleanMaskData(mask_data):
    global state_symbols
    mask_data = mask_data.rename(columns={'COUNTYFP': 'fips'})

    return mask_data.dropna()

# merge first on mask (m) and covid (c) data on fips column
# then merge with election data  on county, state pair
def mergeData(mask_data, covid_data, election_data):
    merged_m_c = pandas.merge(covid_data, mask_data, on='fips')
    merged = pandas.merge(merged_m_c, election_data, on=['county', 'state'])

    merged["percent_Biden"] = merged["votes20_Joe_Biden"] / merged["TotalPop"]
    merged["percent_Trump"] = merged["votes20_Donald_Trump"] / merged["TotalPop"]
    merged["infrequent_mask_use"] = merged["NEVER"] + merged["RARELY"]
    merged["frequent_mask_use"] = merged["FREQUENTLY"] + merged["ALWAYS"] + merged["SOMETIMES"]
    # cases per capita
    merged["cases_pc"] = merged["cases"] / merged["TotalPop"]
    merged["deaths_pc"] = merged["deaths"] / merged["TotalPop"]
    merged["deaths_over_cases"] = merged["deaths"] / merged["cases"]
    return merged
    