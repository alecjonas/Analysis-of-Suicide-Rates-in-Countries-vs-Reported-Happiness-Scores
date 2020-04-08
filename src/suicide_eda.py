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

#Combines the above functions into process
def make_cumulative_df(metric_2015, metric_2016, metric_2017, metric_2018, metric_2019, name_of_column):
    list_of_dicts = [metric_2015, metric_2016, metric_2017, metric_2018, metric_2019]
    cumulative_scores = one_dict(list_of_dicts)
    count_of_each_country = count_of_occurances(list_of_dicts)
    scrubbed_scores = suicide_scrub(cumulative_scores, list_of_suicide_countries)
    scrubbed_count = suicide_scrub(count_of_each_country, list_of_suicide_countries)
    new_df = master_happiness_dict(scrubbed_scores, scrubbed_count)
    new_df_with_labels = pd.DataFrame(new_df.items(), columns=['country', name_of_column])
    sorted_new_df_with_labels = new_df_with_labels.sort_values(by=[name_of_column], ascending=False)
    return sorted_new_df_with_labels

#Below two functions are needed to build graphs to compare the various metrics to happinss
def compare_all_metrics_to_happiness(cumulative_metric_df, column_name2):
    top_10_country_mask = cumulative_metric_df['country'].isin(top_10_country_list)
    top_10_country = cumulative_metric_df.loc[top_10_country_mask, :]
    top_10_avg = top_10_country[column_name2].mean()
    
    bottom_10_country_mask = cumulative_metric_df['country'].isin(bottom_10_country_list)
    bottom_10_country = cumulative_metric_df.loc[bottom_10_country_mask, :]
    bottom_10_avg = bottom_10_country[column_name2].mean()
    
    return top_10_avg, bottom_10_avg

def make_metric_graphs(nested_list_of_metric_dfs_and_column_names):
    list_of_metric_graphs = [compare_all_metrics_to_happiness(i[0], i[1]) for i in nested_list_of_metric_dfs_and_column_names]
    return list_of_metric_graphs

def compare_suicide_rates(country1, country2):
    country1_mask = suicides['country'] == country1
    country1_df = suicides[country1_mask]
    country1_df_suicide_rate_over_time = country1_df[['year','suicides/100k_pop']]
    country1_df_total_suicide_rate = country1_df_suicide_rate_over_time.groupby(['year']).sum()
    
    country2_mask = suicides['country'] == country2
    country2_df = suicides[country2_mask]
    country2_df_suicide_rate_over_time = country2_df[['year','suicides/100k_pop']]
    country2_df_total_suicide_rate = country2_df_suicide_rate_over_time.groupby(['year']).sum()
    
    fig, ax = plt.subplots(figsize=(12,10))
    ax.plot(country1_df_total_suicide_rate['suicides/100k_pop'], label=f"Suicides/100k in {country1}")
    ax.plot(country2_df_total_suicide_rate['suicides/100k_pop'], label=f"Suicides/100k in {country2}")
    ax.legend()
    plt.show()

#Use to make plot of counts of each country in suicide database
def count_of_countries_per_year(top_10_country_list, bottom_10_country_list, df):
    top_10_country_mask = df['country'].isin(top_10_country_list)
    top_10_country_df = df.loc[top_10_country_mask, :]
    top_10_country_df_count = top_10_country_df.groupby(['year']).count()[:-1]
    
    bottom_10_country_mask = df['country'].isin(bottom_10_country_list)
    bottom_10_country_df = df.loc[bottom_10_country_mask, :]
    bottom_10_country_df_count = bottom_10_country_df.groupby(['year']).count()[:-1]
    
    return top_10_country_df_count, bottom_10_country_df_count

#Use bottom two functions to make a plot of suicide by age group
def age_top_and_bottom(age):
    my_mask = age_and_suicide_rate['age'] == age
    my_age_and_suicide_rate = age_and_suicide_rate[my_mask]

    top_10_country_list = ['Denmark','Norway','Switzerland','Iceland','Finland','Netherlands',
                           'Canada','Sweden','New Zealand','Australia']
    age_top_10_country_mask = my_age_and_suicide_rate['country'].isin(top_10_country_list)
    age_top_10_country = my_age_and_suicide_rate.loc[age_top_10_country_mask, :]
    age_top_10_sum = age_top_10_country.groupby(['year']).sum()[2:-1]

    bottom_10_country_list = ['Bosnia and Herzegovina' ,'Greece', 'Mongolia','South Africa','Bulgaria',
                              'Armenia','Sri Lanka' ,'Ukraine' ,'Georgia','Albania']
    age_bottom_10_country_mask = my_age_and_suicide_rate['country'].isin(bottom_10_country_list)
    age_bottom_10_country = my_age_and_suicide_rate.loc[age_bottom_10_country_mask, :]
    age_bottom_10_sum = age_bottom_10_country.groupby(['year']).sum()[2:-1]
    
    return age_top_10_sum, age_bottom_10_sum

def make_age_graphs(list_of_ages):
    list_of_graphs = [age_top_and_bottom(i) for i in list_of_suicide_ages]
    return list_of_graphs

#Use to two functions below to make a plot of suicides by sex
def suicide_by_sex(sex):
    sex_mask = sex_and_suicide_rate['sex'] == sex
    sex_country_and_suicide_rate = sex_and_suicide_rate[sex_mask]

    top_10_country_list = ['Denmark','Norway','Switzerland','Iceland','Finland','Netherlands',
                           'Canada','Sweden','New Zealand','Australia']
    sex_top_10_country_mask = sex_country_and_suicide_rate['country'].isin(top_10_country_list)
    sex_top_10_country = sex_country_and_suicide_rate.loc[sex_top_10_country_mask, :]
    sex_top_10_sum = sex_top_10_country.groupby(['year']).sum()[2:-1]

    bottom_10_country_list = ['Bosnia and Herzegovina' ,'Greece', 'Mongolia','South Africa',
                              'Bulgaria','Armenia','Sri Lanka' ,'Ukraine' ,'Georgia','Albania']
    sex_bottom_10_country_mask = sex_country_and_suicide_rate['country'].isin(bottom_10_country_list)
    sex_bottom_10_country = sex_country_and_suicide_rate.loc[sex_bottom_10_country_mask, :]
    sex_bottom_10_sum = sex_bottom_10_country.groupby(['year']).sum()[2:-1]
    
    return sex_top_10_sum, sex_bottom_10_sum

def make_sex_graphs(list_of_sexes):
    list_of_sex_graphs = [suicide_by_sex(i) for i in list_of_sexes]
    return list_of_sex_graphs

#For easily extrapolating metrics for various countries
class Country():
    
    def __init__(self, country):
        happiness_metric = cumulative_happiness[cumulative_happiness['country'] == country].to_numpy().item(1)
        gdp_metric = cumulative_gdp[cumulative_gdp['country'] == country].to_numpy().item(1)
        generosity_metric = cumulative_generosity[cumulative_generosity['country'] == country].to_numpy().item(1)
        family_metric = cumulative_family[cumulative_family['country'] == country].to_numpy().item(1)
        health_life_expectancy_metric = cumulative_health_life_expectancy[cumulative_health_life_expectancy['country'] == country].to_numpy().item(1)
        freedom_metric = cumulative_freedom[cumulative_freedom['country'] == country].to_numpy().item(1)
        corruption_metric = cumulative_trust_government_corruption[cumulative_trust_government_corruption['country'] == country].to_numpy().item(1)
        
        self.score = [f'Happiness Score is {happiness_metric}', 
                      f'GDP Weight is {gdp_metric}', 
                      f'Generosity Weight is {generosity_metric}', 
                      f'Family Weight is {family_metric}', 
                      f'Health and Life Expectancy Weight is {health_life_expectancy_metric}', 
                      f'Freedom Weight is {freedom_metric}', 
                      f'Corruption and Government Trust Weight is {corruption_metric}'
                     ]
        self.variables = [happiness_metric, 
                      gdp_metric, 
                      generosity_metric, 
                      family_metric, 
                      health_life_expectancy_metric, 
                      freedom_metric, 
                      corruption_metric
                     ]
        self.gdp = cumulative_gdp[cumulative_gdp['country'] == country].to_numpy().item(1)
        self.generosity = cumulative_generosity[cumulative_generosity['country'] == country].to_numpy().item(1)
        self.family = cumulative_family[cumulative_family['country'] == country].to_numpy().item(1)
        self.health_life_expectancy = cumulative_health_life_expectancy[cumulative_health_life_expectancy['country'] == country].to_numpy().item(1)
        self.happiness = cumulative_happiness[cumulative_happiness['country'] == country].to_numpy().item(1)
        self.trust_government_corruption = cumulative_trust_government_corruption[cumulative_trust_government_corruption['country'] == country].to_numpy().item(1)
        self.freedom = cumulative_freedom[cumulative_freedom['country'] == country].to_numpy().item(1)

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

    countries_in_the_suicides_df=suicides.country.unique()
    list_of_suicide_countries = countries_in_the_suicides_df.tolist()

    #Dict for Happiness
    h2015_dict = pd.Series(h2015.happiness_score.values,index=h2015.country).to_dict()
    h2016_dict = pd.Series(h2016.happiness_score.values,index=h2016.country).to_dict()
    h2017_dict = pd.Series(h2017.happiness_score.values,index=h2017.country).to_dict()
    h2018_dict = pd.Series(h2018.score.values,index=h2018.country_or_region).to_dict()
    h2019_dict = pd.Series(h2019.score.values,index=h2019.country_or_region).to_dict()

    cumulative_happiness = make_cumulative_df(h2015_dict, h2016_dict, h2017_dict, h2018_dict, h2019_dict, 'cumulative_happiness_score')

    #Dict for GDP
    gdp_2015_dict = pd.Series(h2015.economy_gdp_per_capita.values,index=h2015.country).to_dict()
    gdp_2016_dict = pd.Series(h2016.economy_gdp_per_capita.values,index=h2016.country).to_dict()
    gdp_2017_dict = pd.Series(h2017.economy__gdp_per_capita_.values,index=h2017.country).to_dict()
    gdp_2018_dict = pd.Series(h2018.gdp_per_capita.values,index=h2018.country_or_region).to_dict()
    gdp_2019_dict = pd.Series(h2019.gdp_per_capita.values,index=h2019.country_or_region).to_dict()

    cumulative_gdp = make_cumulative_df(gdp_2015_dict, gdp_2016_dict, gdp_2017_dict, gdp_2018_dict, gdp_2019_dict, 'cumulative_gdp')

    #Dict for Family
    family_2015_dict = pd.Series(h2015.family.values,index=h2015.country).to_dict()
    family_2016_dict = pd.Series(h2016.family.values,index=h2016.country).to_dict()
    family_2017_dict = pd.Series(h2017.family.values,index=h2017.country).to_dict()
    family_2018_dict = pd.Series(h2018.social_support.values,index=h2018.country_or_region).to_dict()
    family_2019_dict = pd.Series(h2019.social_support.values,index=h2019.country_or_region).to_dict()

    cumulative_family = make_cumulative_df(family_2015_dict, family_2016_dict, family_2017_dict, family_2018_dict, family_2019_dict, 'cumulative_family')
    
    #Dict for health_life_expectancy
    hle_2015_dict = pd.Series(h2015.health_life_expectancy.values,index=h2015.country).to_dict()
    hle_2016_dict = pd.Series(h2016.health_life_expectancy.values,index=h2016.country).to_dict()
    hle_2017_dict = pd.Series(h2017.health__life_expectancy_.values,index=h2017.country).to_dict()
    hle_2018_dict = pd.Series(h2018.healthy_life_expectancy.values,index=h2018.country_or_region).to_dict()
    hle_2019_dict = pd.Series(h2019.healthy_life_expectancy.values,index=h2019.country_or_region).to_dict()

    cumulative_health_life_expectancy = make_cumulative_df(hle_2015_dict,hle_2016_dict, hle_2017_dict, hle_2018_dict, hle_2019_dict, 'cumulative_health_life_expectancy')

    #Dict for freedom
    freedom_2015_dict = pd.Series(h2015.freedom.values,index=h2015.country).to_dict()
    freedom_2016_dict = pd.Series(h2016.freedom.values,index=h2016.country).to_dict()
    freedom_2017_dict = pd.Series(h2017.freedom.values,index=h2017.country).to_dict()
    freedom_2018_dict = pd.Series(h2018.freedom_to_make_life_choices.values,index=h2018.country_or_region).to_dict()
    freedom_2019_dict = pd.Series(h2019.freedom_to_make_life_choices.values,index=h2019.country_or_region).to_dict()

    cumulative_freedom = make_cumulative_df(freedom_2015_dict, freedom_2016_dict, freedom_2017_dict, freedom_2018_dict, freedom_2019_dict, 'cumulative_freedom')

    # Dict for trust_government_corruption
    corruption_2015_dict = pd.Series(h2015.trust_government_corruption.values,index=h2015.country).to_dict()
    corruption_2016_dict = pd.Series(h2016.trust_government_corruption.values,index=h2016.country).to_dict()
    corruption_2017_dict = pd.Series(h2017.trust__government_corruption_.values,index=h2017.country).to_dict()
    corruption_2018_dict = pd.Series(h2018.perceptions_of_corruption.values,index=h2018.country_or_region).to_dict()
    corruption_2019_dict = pd.Series(h2019.perceptions_of_corruption.values,index=h2019.country_or_region).to_dict()

    cumulative_trust_government_corruption = make_cumulative_df(corruption_2015_dict, corruption_2016_dict, corruption_2017_dict, corruption_2018_dict, corruption_2019_dict, 'cumulative_corruption')

    # Dict for generosity
    generosity_2015_dict = pd.Series(h2015.generosity.values,index=h2015.country).to_dict()
    generosity_2016_dict = pd.Series(h2016.generosity.values,index=h2016.country).to_dict()
    generosity_2017_dict = pd.Series(h2017.generosity.values,index=h2017.country).to_dict()
    generosity_2018_dict = pd.Series(h2018.generosity.values,index=h2018.country_or_region).to_dict()
    generosity_2019_dict = pd.Series(h2019.generosity.values,index=h2019.country_or_region).to_dict()

    cumulative_generosity = make_cumulative_df(generosity_2015_dict, generosity_2016_dict, generosity_2017_dict, generosity_2018_dict, generosity_2019_dict, 'cumulative_generosity')