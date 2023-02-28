import streamlit as st
import pandas as pd
from textblob import TextBlob


def get_sentiment(text):
    return TextBlob(text).sentiment.polarity
# Create file uploader and define accepted file types
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# If a file was uploaded, read the contents into a Pandas DataFrame
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Convert 'timestamp' column to a pandas datetime object
# df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sort DataFrame by 'timestamp' column in ascending order
    df_sorted = df.sort_values(by='timestamp')

    # Calculate the time difference between rows in hours
    df_sorted['time_diff_hours'] = (df_sorted['timestamp'] - df_sorted['timestamp'].shift()).dt.total_seconds() / 3600
    df_sorted['hour_offset'] = (df_sorted['timestamp'] - df_sorted['timestamp'].min()).astype('timedelta64[h]')
    sentiments = []
    keywords = []
    for text in df_sorted['tweet']:
        sentiment = get_sentiment(str(text))
        sentiments.append(sentiment)
    df_sorted['sentiments'] = sentiment
    # Display the result
    st.table(df_sorted)

    csv = df_sorted.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Display the DataFrame
    # st.write(df_sorted)
