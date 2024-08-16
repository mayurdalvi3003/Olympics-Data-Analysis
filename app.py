import streamlit as st 
import pandas as pd
import preprocessor , helper
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.figure_factory as ff


df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")

df  = preprocessor.preprocess(df , region_df) # it is returning the df and i am receiving here 

st.sidebar.title('Olympics Analysis')
st.sidebar.image('logo.jpeg')


user_menu = st.sidebar.radio("Select an option",
('Medal Tally','Overall Analysis','Country Wise Analysis','Athlete wise Analysis')
)
#st.dataframe(df) # here i am showing that dataframe which i have received using the preprocessor

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years , country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year" , years)
    selected_country = st.sidebar.selectbox("Select Country" , country)
    medal_tally = helper.fetch_medal_tally(df , selected_year, selected_country)

    if selected_year =="Overall" and selected_country == "Overall":
        st.title("Overall Tally")
    
    if selected_year != "Overall" and selected_country == "Overall":
        st.title('Medal Tally In '+ str(selected_year) + ' Olympics' )

    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country  +  " Overall Performance")
    
    if selected_year != "Overall" and selected_country != "Overall":
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    edition = df["Year"].unique().shape[0]-1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athlets = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    st.title("Top Statistics")
    col1, col2 , col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(edition)
    
    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    
    col1, col2 , col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(events)
    
    with col2:
        st.header("Athletes")
        st.title(athlets)

    with col3:
        st.header("Nations")
        st.title(nations)

        
    # ploting the line graph for year wise nations participations
    # making line plot using line 
    st.title("Participating Nations Over Years")
    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time , x = "Year" , y = "count")
    st.plotly_chart(fig)

    # ploting the no,of events happened
    st.title("No. Of Events Over Years")
    events_over_time = helper.data_over_time(df)
    fig = px.line(events_over_time , x = "Year" , y = "count")
    st.plotly_chart(fig)


    # ploting the no,of events happened
    st.title("Athletes Over Years")
    athlets = helper.athletes_over_time(df)
    fig = px.line(athlets , x = "Year" , y = "count")
    st.plotly_chart(fig)

    # showing the heatmap

    st.title("No. Of Events over time(Every Sports)")
    fig , ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year' ,'Sport' , 'Event'])
    ax = sns.heatmap(x.pivot_table(index="Sport" , columns='Year' , values='Event' , aggfunc="count").fillna(0).astype("int") , annot=True)
    st.pyplot(fig)

    # showing most succesfull athletes

    st.title("Most Succesfull Athletes")

    # now here i am adding dropdowns by using that user can select the sports
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0 , 'Overall')
    selected_sport = st.selectbox('Select a Sport' , sports_list)
    # here i am showing most succesfull athlet table
    x = helper.most_succesfull_athlete(df , selected_sport)
    st.table(x)

# -------------------------------------------------------------------------------------
# country wise analysis 

if user_menu == "Country Wise Analysis":
    st.sidebar.title("Country Wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    country_df = helper.yearwise_medal_tally(df , selected_country)
    fig = px.line(country_df , x = 'Year' ,y = 'Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)


    st.title(selected_country  + " excels in the following sports")
    pt = helper.country_event_heatmap(df , selected_country)
    fig , ax = plt.subplots(figsize = (20,20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)


    st.title("Top-10 Athletes of " +selected_country)
    top10_df = helper.most_succesfull_athlete_countrywise(df , selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    st.title('Distribution of Age')
    athlete_df = df.drop_duplicates(subset  =['Name' ,'region'])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df['Medal'] =='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] =='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] =='Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2,x3,x4],['Overall Age' ,'Gold Medalist' ,'Silver Medalist' ,'Bronze Medalist'] , show_hist=False , show_rug= False)
    fig.update_layout(autosize = False , width  =1000  , height = 600)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age w.r.t Sports(Gold Medalist)")
    st.plotly_chart(fig)



    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x = temp_df['Weight'],y = temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)



    st.title("Men VS Women participation over the year")
    final = helper.men_vs_women(df)
    fig = px.line(final , x= "Year" , y = ['Male','Female'])
    st.plotly_chart(fig)








