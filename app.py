import streamlit as st
import nltk
import pandas as pd
import altair as alt
from wordcloud import WordCloud
from textblob import TextBlob
import os
nltk.download('punkt')
nltk.download('brown')

alt.themes.enable("streamlit")
# Define a function to get sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

def get_keyword(text):
    return TextBlob(text).noun_phrases

st.set_page_config(
    page_title="Bipolar Tweet Prediction", page_icon=":brain:", layout="wide"
)


st.title("Instancy")

########### select CSV##################
directory = 'data'
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

# Create a selectbox widget to allow the user to choose a CSV file


selected_file = st.sidebar.selectbox('Select a User', csv_files)

if selected_file:
# Use pandas to read the selected file into a dataframe
    data = pd.read_csv(os.path.join(directory, selected_file))
    sentiments = []
    keywords = []
    for text in data['tweet']:
        sentiment = get_sentiment(str(text))
        sentiments.append(sentiment)




    blob = TextBlob(text)
    word_freq = {}
    for word in blob.words:
        word_freq[word.lower()] = word_freq.get(word.lower(), 0) + 1
    wordcloud = WordCloud(width=800, height=800, background_color='white', max_words=100).generate_from_frequencies(word_freq)

    # keey = get_keyword(str(text))
    # keywords_string = ', '.join(keywords)
    keywords.append(word_freq)
    # Add a new column 'sentiment' to the DataFrame with the calculated sentiment scores
    data['sentiment'] = sentiments
    # data['keywords'] = keywords
    global source
    source = data
    timeline = st.slider("TimeLine", min_value=2008,
    max_value=2021,
    value=(2010),
    step=1)

    # keyword_choice = st.sidebar.multiselect(    'Choose Keyword Filters:', keywords, default=keywords)

    # st.sidebar.write("Final Year Undergraduate")
    # st.sidebar.write("IIT (University of Westminster)")

# with st.beta_expander("Click to expand Graph"):

#     annotations_df = pd.DataFrame(source, columns=["timestamp", "sentiment","tweet","bp_label"])
#     annotations_df.timestamp = pd.to_datetime(annotations_df.timestamp)
#     annotations_df["y"] = 0

#     slider = alt.binding_range(min=-1, max=1, step=0.01, name='SentimentFilter:')
#     selector = alt.selection_single(name="SelectorName", fields=['cutoff'],
#                                     bind=slider, init={'cutoff': 0.5})

#     c = alt.Chart(annotations_df).mark_point().encode(
#         x='timestamp', y='sentiment',
#         tooltip=['tweet','bp_label'] ,color=alt.condition(
#             alt.datum.sentiment < selector.cutoff,
#             alt.value('red'), alt.value('blue'))).add_selection( selector )
#     st.altair_chart((c).interactive(), theme="streamlit",use_container_width=True)


    # st.write("Content inside the expandable section")
    # Create a chart with annotations

with st.beta_expander("Click to expand Table"):
    st.subheader("Dataset")
    st.dataframe(data, width=800, height=500)
