import streamlit as st
import pandas as pd
import altair as alt

color_mapping = {'negative': 'red', 'neutral': 'blue', 'positive': 'green'}
option_state = ["new_york","boston","massachusetts"]


def dynamic_label_reader(requestGap):
    counter = counter+1

    if counter % requestGap==0:
        data = pd.DataFrame({'Category': ['positive', 'negative', 'neutral'], 'value': [positive, negative, neutral]})

    # create a bar chart using Altair
        chart = alt.Chart(data).mark_bar().encode(x='category', y='value')
        st.altair_chart(chart, use_container_width=True)



def statewise_customer_reviews_report_helper():
    option_state = ["new_york","boston","massachusetts"]
    option = st.selectbox('Select the state', option_state)
    dataframe_address = "data/" + option + ".csv"
    state_df = pd.read_csv(dataframe_address)

    # print the selected option
    st.write('Selected State :', option)
    if len(state_df) > 0:
        segregate_lables_and_generate_graph("Statewise graph",state_df)

def reveiews_per_state():
    map_id_review_map = {}
    for option in option_state:
        
        dataframe_address = "data/" + option + ".csv"
        state_df = pd.read_csv(dataframe_address)
       
        map_id_review_map[option] = state_df.shape[0]
   
    data = pd.DataFrame({'States': map_id_review_map.keys(), 'Number of Reviews': map_id_review_map.values()})
    # create a bar chart using Altair
    chart = alt.Chart(data).mark_bar().encode(
    x='States',
    y= 'Number of Reviews'
    )
    st.altair_chart(chart, use_container_width=True)
# Render the chart using altair_chart in Streamlit

def user_wise_customer_review_report_helper():
    state_option = st.selectbox('Select the state for the user wise report', option_state)
    dataframe_address = "data/" + state_option + ".csv"
    state_df = pd.read_csv(dataframe_address)

    option_user = st.selectbox('Selected user id', state_df['user_id'].unique()) #List of userId

    # print the selected option
    st.write('Selected User id:', option_user)
    user_db = state_df[state_df['user_id'] == option_user]
    segregate_lables_and_generate_graph("User graph",user_db)

def business_wise_customer_review_report(): #List of Business Names
    state_option = st.selectbox('Select the state for the business wise report', option_state)
    dataframe_address = "data/" + state_option + ".csv"
    state_df = pd.read_csv(dataframe_address)
    option = st.selectbox('Select Business', state_df['business_id'].unique())
    # print the selected option
    st.write('Selected business id:', option)
    business_db = state_df[state_df['business_id'] == option]
    segregate_lables_and_generate_graph("Business wise graph",business_db)


def segregate_lables_and_generate_graph(graphHeading,dataFrame = None ):
    
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
    # create a bar chart using Altair
    chart = alt.Chart(data).mark_bar().encode(
    x='Category',
    y='Value',
    color=alt.Color('Category', scale=alt.Scale(domain=list(color_mapping.keys()), range=list(color_mapping.values())))
)

# Render the chart using altair_chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


def main():
    # dynamic_label_reader()
    statewise_customer_reviews_report_helper()
    user_wise_customer_review_report_helper()
    # business_wise_customer_review_report()
    reveiews_per_state()

if __name__ == '__main__':
    global counter
    global positive_counter
    global negative_counter
    global neural_counter
    positive_counter = 0
    negative_counter = 0
    neural_counter = 0
    counter = 0

    print("Starting the graph generation")
    main()