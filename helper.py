import pandas as pd
import numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset = ['Team','NOC','City','Sport','Event','Medal','Games'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally

def country_year_list(df):
    years =  df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0,'Overall')
    return years,countries

def fetch_details(year,country,df):
    medal_df = df.drop_duplicates(subset = ['Team','NOC','City','Sport','Event','Medal','Games'])
    flag = 0
    if year == "Overall" and country == "Overall":
        temp = df
    if year != "Overall" and country == "Overall":
        temp = medal_df[medal_df['Year'] == int(year)]
    if year == "Overall" and country != "Overall":
        flag = 1
        temp = medal_df[medal_df['region'] == country]
    if year != "Overall" and country != "Overall":
        temp = medal_df[(medal_df['Year'] == int(year)) &( medal_df['region'] == country)]
    if flag == 1:   
        x = temp.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold').reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x

def data_over_time(df,col):
    over_time =df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('index')
    over_time.rename(columns = {'index':'Editions','Year':col},inplace = True)
    return over_time

def most_successfull(df,selected_sport):
    temp = df.dropna(subset = ['Medal'])
    if selected_sport != 'Overall':
        temp = temp[temp['Sport'] == selected_sport]
    x = temp['Name'].value_counts().reset_index().head(15).merge(df,left_on = 'index',right_on = 'Name',how= 'left')[['index','Name_x','region','Sport']].drop_duplicates('index').reset_index()
    x.drop('level_0',axis=1,inplace = True)
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace = True)
    return x

def most_successfull_athlete_country_wise(df,country):
    temp = df.dropna(subset = ['Medal'])
    temp = temp[temp['region'] == country]
    x = temp['Name'].value_counts().reset_index().head(15).merge(df,left_on = 'index',right_on = 'Name',how= 'left')[['index','Name_x','region','Sport']].drop_duplicates('index').reset_index()
    x.drop('level_0',axis=1,inplace = True)
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace = True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team','NOC','City','Sport','Event','Medal','Games'],inplace = True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def Country_event_heatmap(df,country):
    temp_df = df.dropna(subset = ['Medal'])
    temp_df.drop_duplicates(subset = ['Team','NOC','City','Sport','Event','Medal','Games'],inplace = True)
    new_df = temp_df[temp_df['region'] == country].fillna(0)
    final_df = new_df.pivot_table(index = 'Sport',columns = 'Year',values = 'Medal',aggfunc = 'count').fillna(0)
    return final_df

def weight_v_height(df,sport):
    athlete = df.drop_duplicates(['region','Name'])
    athlete['Medal'].fillna('No Medal',inplace = True)
    if sport != 'Overall':
        temp = athlete[athlete['Sport'] == sport]
        return temp
    else:
        return athlete

def men_v_women(df):
    athlete = df.drop_duplicates(['region','Name'])
    men = athlete[athlete['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete[athlete['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women,on='Year',how='left')
    final.rename(columns = {'Name_x' : 'Male','Name_y' : 'Female'},inplace = True)
    final.fillna(0,inplace = True)
    return final