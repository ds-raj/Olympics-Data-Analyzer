import streamlit as st
import pandas as pd
import helper,preprocessor
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.sidebar.title('Olympic Analysis')
st.sidebar.image('data:image/jpeg;base64,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')
df = pd.read_csv('athlete_events.csv')
regions = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, regions)
user_selection = st.sidebar.radio('SELECT AN OPTION', ('Athlete-wise analysis','Country-wise analysis','Medal tally','Overall analysis'))
if user_selection == 'Medal tally':
    st.sidebar.header('Medal Tally')
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Years',years)
    selected_country = st.sidebar.selectbox('Select Country',country)
    if (selected_year == 'Overall') and (selected_country == 'Overall'):
        st.title('Overall Tally')
    elif (selected_year != 'Overall') and (selected_country == 'Overall'):
        st.title(f"Medal Tally in  {selected_year} Olympics")
    elif (selected_year == 'Overall') and (selected_country != 'Overall'):
        st.title(f"Overall Performance of {selected_country}")
    elif (selected_year != 'Overall') and (selected_country != 'Overall'):
        st.title(f"{selected_country} Performance in {selected_year} Olympics")
    medal_tally = helper.fetch_details(selected_year,selected_country,df)
    st.dataframe(medal_tally)

if user_selection == 'Overall analysis':
    st.title('Overall Analysis')
    st.header('Top Statistics')
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Cities")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)

    st.header('Participation Nations Over the Years')
    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time,x = 'Editions',y = 'region')
    st.plotly_chart(fig)

    st.header('Events over time')
    nation_over_time = helper.data_over_time(df,'Event')
    fig = px.line(nation_over_time,x = 'Editions',y = 'Event')
    st.plotly_chart(fig)
    
    st.header('Athletes over Editions')
    nation_over_time = helper.data_over_time(df,'Name')
    fig = px.line(nation_over_time,x = 'Editions',y = 'Name')
    st.plotly_chart(fig)

    st.title('Events occuring at each sport over the years')
    fig,ax = plt.subplots(figsize = (25,25))
    x = df.drop_duplicates(['Year','Event','Sport'])
    ax = sns.heatmap(x.pivot_table(index = 'Sport',columns = 'Year',values = 'Event',aggfunc = 'count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most Successful Players')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox('select a sport',sports_list)
    x = helper.most_successfull(df,selected_sport)
    st.table(x)

if user_selection == 'Country-wise analysis':
    country_list = df['region'].unique().tolist()
    country = st.selectbox('Select Country',country_list)
    st.title('Country Wise Analysis')
    st.header(f'{country} Medal Tally Over the Years')
    country_df = helper.yearwise_medal_tally(df, country)
    fig = px.line(country_df,x = 'Year',y= 'Medal')
    st.plotly_chart(fig)

    st.title(f'{country} Excels in the following Sports')
    fig,ax = plt.subplots(figsize = (20,20))
    country_event = helper.Country_event_heatmap(df, country)
    ax = sns.heatmap(country_event,annot=True)
    st.pyplot(fig)

    st.title(f'{country}\'s Most Successful Players')
    x = helper.most_successfull_athlete_country_wise(df, country)
    st.table(x)

if user_selection == 'Athlete-wise analysis':
    st.title('Athlete Wise Analysis')
    st.title('Distribution of Age')
    athlete = df.drop_duplicates(['region','Name'])
    x1 = athlete['Age'].dropna()
    x2 = athlete[athlete['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete[athlete['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete[athlete['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4], ['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize = False,width = 1000,height = 600)
    st.plotly_chart(fig)


    st.title('Distribution of Age wrt Sports(Gold)')

    x = []
    name = []
    sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']

    for sport in sports:
        temp_df = athlete[athlete['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        
        if not gold_ages.empty:
            x.append(gold_ages)
            name.append(sport)

    if len(x) > 0:
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected sports.")

    st.title('Weight vs Height')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
    selected_sport = st.selectbox('select a sport',sports_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', s=100, data=temp_df)
    st.pyplot(fig)

    st.title('Men vs Women Participation Over the Years')
    final = helper.men_v_women(df)
    fig = px.line(final,x = 'Year' ,y = ['Male','Female'])
    st.plotly_chart(fig)
















