import streamlit as st
import pandas as pd
import altair as alt


uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# If a file was uploaded, read the contents into a Pandas DataFrame
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
        # Convert 'timestamp' column to a pa
    # Load data from CSV file
    # df = pd.read_csv('data.csv')

    # Create a checkbox to toggle data points with true/false labels
    show_true = st.checkbox('Show True Labels')

    # Filter the data based on the checkbox value
    if show_true:
        data = df
    else:
        data = df[df['label'] == False]

    # Create a selection for the tooltip
    selection = alt.selection_single(fields=['timestamp'], nearest=True, on='mouseover', empty='none')

    # Create the chart
    chart = alt.Chart(data).mark_circle().encode(
        x='timestamp:T',
        y='sentiment_score:Q',
        color=alt.Color('label:N', scale=alt.Scale(domain=['True', 'False'], range=['red', 'blue'])),
        tooltip=['description:N', 'keywords:N']
    ).add_selection(selection)

    # Add a line that follows the selected timestamp
    line = chart.transform_filter(selection).mark_line(color='black')

    # Add the chart and line to the Streamlit app
    st.altair_chart(chart + line, use_container_width=True)
