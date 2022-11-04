"""
Kimberly Stochaj
DS2500
Data cleaning for voter turnout
2022 November 3
clean_voterturnout.py
"""
VOTE = "VoterTurnoutData.csv"
POP  = "PopulationData.csv"

import pandas as pd


def clean_voters(filename):
    # read in the csv file as the dataframe
    df_voters = pd.read_csv(filename, skiprows = 3)
    
    # for our purposes, whether we use total or citizen data is unimportant, as
    # we are examining trends, so we just have to stay consistent - I chose total
    
    # first, set the headers to be citizen or total and drop citizen cols
    df_voters.columns = df_voters.iloc[1]
    df_voters.drop("Citizen", axis = 1, inplace = True)
   
    # change the column header to year, as this is more descriptive
    df_voters.columns = df_voters.iloc[0]
    
    # drop duplicated and empty rows
    df_voters.drop([0, 1, 2], axis = 0, inplace= True)
    
    # change the indexes to the name of the states
    df_voters.set_index("State", inplace = True)

    return df_voters


def clean_pop(filename):
    # read inthe csv file as the dataframe
    df_pop = pd.read_csv(filename, skiprows = 4)
    
    # drop the "Fips" column
    df_pop.drop("Fips", axis = 1, inplace = True)
    
    # make the areas the indexes
    df_pop.set_index("Area Name", inplace = True)
    
    return df_pop
    

def get_grand_avg(pct_lst, n_lst):
    
    total_voters = 0
    for i in range(len(pct_lst)):
        total_voters += pct_lst[i] * n_lst[i]
        
    total_pop = sum(n_lst)
    
    grand_avg = (total_voters / total_pop)
    return(grand_avg)

def get_year_data(df_vote, df_pop, year):
    pct_lst = []
    pop_lst = []
    
    vote_locs = df_vote.index
    for state in vote_locs:
        if not pd.isna(df_vote.loc[state, str(year)]):
            pct_lst.append(float(df_vote.loc[state, str(year)])/100)
            pop_lst.append(int((df_pop.loc[state, str(year)]).replace(",", "")))
        
    avg = get_grand_avg(pct_lst, pop_lst)
    return avg
        
    
def main():
    # get the cleaned DataFrames
    df_pop = clean_pop(POP)
    df_voters = clean_voters(VOTE)
    
    print(df_voters)
    
    
    # create the desired dataframe
    final_dict = {"years": [], "voting_pop": []}
    
    for year in df_voters.columns:
        final_dict["years"].append(year)
        final_dict["voting_pop"].append(get_year_data(df_voters, df_pop, year))
    
    
    final_df = pd.DataFrame(final_dict)
    print(final_df)
    
main()
