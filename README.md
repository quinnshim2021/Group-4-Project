# Group-4-Project - Quinn Shim, David Ding

# Running Clean
Have a folder at the same directory level as this repository called `Data`. In `Data`, have `county-statistics.csv`, `mask-use-by-county.csv`, and `us-counties.csv`.

Then, enter this repository and run `python3 clean.py`

# Notes on Cleaning

Cleaning gets the raw data, then reformats each dataframe to have only necessary columns. This includes casting data into similar data types and renaming columns. The county election statistics do not have a `fips` field and their `state` column was just abbreviations, so we had to map the states of a dictionary of {state names : abbreviations} to allow the data to be merged via county-state pairs.

Other notes on cleaning can be found in comments in the code.

# Notes for David

1. around 3100 counties were at the end. This is because some data sets have weird counties (from Guam or ones that aren't actual counties) and others don't have data for everything

2. we'll want to make sure we filter for NaN values (especailly in vote columns) during EDA

3. want to make sure we account for cases/deaths per capita (with toalPop)
