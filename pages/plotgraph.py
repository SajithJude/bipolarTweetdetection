import streamlit as st
import pandas as pd
import altair as alt


uf = st.file_uploader("Choose a CSV file", type=["csv"])

# If a file was uploaded, read the contents into a Pandas DataFrame
if uf is not None:
    df = pd.read_csv(uf)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    st.table(df.head(10))
        # Convert 'timestamp' column to a pa
    # Load data from CSV file
    # df = pd.read_csv('data.csv')

    # Create a checkbox to toggle data points with true/false labels
    show_true = st.checkbox('Show True Labels')

    # Filter the data based on the checkbox value
    if show_true:
        data = df
    else:
        data = df[df['bp_label'] == False]

    # Create a selection for the tooltip
    selection = alt.selection_single(fields=['timestamp'], nearest=True, on='mouseover', empty='none')

    # Create the chart
    chart = alt.Chart(data).mark_circle().encode(
        x='timestamp:T',
        y='sentiment:Q',
        color=alt.Color('bp_label:N', scale=alt.Scale(domain=['TRUE', 'FALSE'], range=['red', 'blue'])),
        tooltip=['tweet:N']
    ).add_selection(selection)

    # Add a line that follows the selected timestamp
    line = chart.transform_filter(selection).mark_line(color='black')

    # Add the chart and line to the Streamlit app
    st.altair_chart(chart + line, use_container_width=True)
