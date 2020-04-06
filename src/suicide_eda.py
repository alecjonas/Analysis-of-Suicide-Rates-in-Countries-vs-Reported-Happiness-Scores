import numpy as np
import pandas as pd

#Cleaning column headers
def clean_header(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '').str.replace('.', '_')
    return df.columns

#Making one dictionary that aggregates each country's happiness score
def one_dict(list_of_dicts):
    d={}
    for i in list_of_dicts:
        for k,v in i.items():
            if k not in d:
                d[k]=v
            if k in d:
                d[k]+=v
    return d

#Count how many times each country appears in the happiness index
def count_of_occurances(list_of_dicts):
    d={}
    for i in list_of_dicts:
        for k,v in i.items():
            if k not in d:
                d[k]=1
            if k in d:
                d[k]+=1
    return d

#Want to make one list of country's but only look at countries that appear in the suicide Database
def suicide_scrub(dictionary, _list):
    d={}
    for k,v in dictionary.items():
        if k in _list:
            d[k]=v
    return d

#This will adjust the cumulative scores by how many times it has appeared in the happiness index.
#Now I will have one dictionary that is a function of years 2015-2019.
def master_happiness_dict(scores, count):
    d={}
    for k in scores.keys():
        d[k]=scores[k]/count[k]
    return d

if __name__=='__main__':
    h2015 = pd.read_csv('/home/alec/galvanize/capstone/capstone_1/data/2015.csv')
    h2016= pd.read_csv('/home/alec/galvanize/capstone/capstone_1/data/2016.csv')
    h2017= pd.read_csv('/home/alec/galvanize/capstone/capstone_1/data/2017.csv')
    h2018= pd.read_csv('/home/alec/galvanize/capstone/capstone_1/data/2018.csv')
    h2019= pd.read_csv('/home/alec/galvanize/capstone/capstone_1/data/2019.csv')
    suicides = pd.read_csv('/home/alec/galvanize/capstone/capstone_1/data/master.csv')

    #Cleaning data headers
    data = [h2015, h2016, h2017, h2018, h2019]
    [clean_header(i) for i in data]
    clean_header(suicides)

    
    #Converting each df into a dictionary
    h2015_dict = pd.Series(h2015.happiness_score.values,index=h2015.country).to_dict()
    h2016_dict = pd.Series(h2016.happiness_score.values,index=h2016.country).to_dict()
    h2017_dict = pd.Series(h2017.happiness_score.values,index=h2017.country).to_dict()
    h2018_dict = pd.Series(h2018.score.values,index=h2018.country_or_region).to_dict()
    h2019_dict = pd.Series(h2019.score.values,index=h2019.country_or_region).to_dict()
    
    #Pulling all the countries from the suicides database and converting it to a list
    #The goal is to remove countrys from the happiness index that are not in this list
    countries_in_the_suicides_df=suicides.country.unique()
    list_of_suicide_countries = countries_in_the_suicides_df.tolist()
    
    #Creating two dictionaries. The first compilies the total scores across all 5 happiness csv files.
    #The second one makes a dictionary of how many times each country appears in all 5 happiness csv files.
    list_of_dicts = [h2015_dict, h2016_dict, h2017_dict, h2018_dict, h2019_dict]
    cumulative_scores = one_dict(list_of_dicts)
    count_of_each_country = count_of_occurances(list_of_dicts)
    
    #I removed countries from the happiness report that have no data in the suicides databse
    scrubbed_scores = suicide_scrub(cumulative_scores, list_of_suicide_countries)
    scrubbed_count = suicide_scrub(count_of_each_country, list_of_suicide_countries)
    
    #Making one dictionary that is adjusted for how many times the country has appeared between 2015-2019
    master_happy = master_happiness_dict(scrubbed_scores, scrubbed_count)

    #Making a new pandas dataframe out of the above dictionary
    cumulative_happiness = pd.DataFrame(master_happy.items(), columns=['country', 'cumulative_happiness_score'])
    