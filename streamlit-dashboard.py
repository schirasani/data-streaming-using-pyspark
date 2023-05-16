import streamlit as st
import pandas as pd
import altair as alt
import time 
import numpy as np

color_mapping = {'negative': 'red', 'neutral': 'blue', 'positive': 'green'} #Color coding for the possible label output
option_state = ["new_york","boston","massachusetts"] #List of states present in the dataset


def statewise_customer_reviews_report_helper():
    """
    This function allows us to map the state wise customer review reports and helps to determine the number of positive, negative and neutral reviews
    """
    st.header("Sate Wise Customer Reviews")
    option = st.selectbox('Select the state', option_state )
    dataframe_address = "data/" + option + ".csv"
    state_df = pd.read_csv(dataframe_address)

    st.write('Selected State :', option)
    if len(state_df) > 0: # only carry out the graph creation process if there is a dataset available
        segregate_lables_and_generate_graph("Statewise graph",state_df)

def reveiews_per_state():
    """
    This function allows us to determine total number of reviews per state
    """
    st.header("Number of Reviews per state")
    map_id_review_map = {}
    for option in option_state:
        
        dataframe_address = "data/" + option + ".csv"
        state_df = pd.read_csv(dataframe_address)
       
        map_id_review_map[option] = state_df.shape[0]
   
    data = pd.DataFrame({'States': map_id_review_map.keys(), 'Number of Reviews': map_id_review_map.values()})

    chart = alt.Chart(data).mark_bar().encode(
    x='States',
    y= 'Number of Reviews'
    )
    st.altair_chart(chart, use_container_width=True)


def user_wise_customer_review_report_helper():
    """
    This function allows us to determine total number of reviews given be each user and how many out of them are positive, negative or neutral
    """
    st.header("Reviews per User")
    state_option = st.selectbox('Select the state for the user wise report', option_state )
    dataframe_address = "data/" + state_option + ".csv"
    state_df = pd.read_csv(dataframe_address)

    option_user = st.selectbox('Selected user id', state_df['user_id'].unique() ) #List of userId
    st.write('Selected User id:', option_user)
    user_db = state_df[state_df['user_id'] == option_user]
    segregate_lables_and_generate_graph("User graph",user_db)

def business_wise_customer_review_report():
    """
    This function allows us to determine total number of reviews given to each business and how many out of them are positive, negative or neutral. It also showcases the list of reviews
    """
    
    st.header("Reviews per Business")
    state_option = st.selectbox('Select the state for the business wise report', option_state )
    dataframe_address = "data/" + state_option + ".csv"
    state_df = pd.read_csv(dataframe_address)
    option = st.selectbox('Select Business', state_df['business_id'].unique() ) #List of busisnessId
    st.write('Selected business id:', option)
    business_db = state_df[state_df['business_id'] == option]
    st.dataframe(business_db["text"].tail(10),use_container_width=True)
    segregate_lables_and_generate_graph("Business wise graph",business_db)


def segregate_lables_and_generate_graph(graphHeading,dataFrame = None ):
    """
    helper function to count number of positive, negative and neutral reviews in the given dataset
    """
    st.write(graphHeading)

    if dataFrame is None:
        df = pd.read_csv("sample_data_1000.csv")
    else:
        df = dataFrame
    positive=0
    negative = 0
    neutral = 0
    for index, row in df.iterrows():
        # print(row)
        if row["labels_3"]=="neutral":
            neutral +=1
        elif row["labels_3"]=="negative":
            negative +=1
        else:
            positive +=1

    data = pd.DataFrame({'Category': ['positive', 'negative', 'neutral'], 'Value': [positive, negative, neutral]})
    chart = alt.Chart(data).mark_bar().encode(
    x='Category',
    y='Value',
    color=alt.Color('Category', scale=alt.Scale(domain=list(color_mapping.keys()), range=list(color_mapping.values())))
)

    st.altair_chart(chart, use_container_width=True)


def main():
        print("Starting the run")
        statewise_customer_reviews_report_helper()
        user_wise_customer_review_report_helper()
        business_wise_customer_review_report()
        reveiews_per_state()
        time.sleep(15)
        st.experimental_rerun()

if __name__ == '__main__':
    
    main()