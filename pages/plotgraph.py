import streamlit as st
import pandas as pd
import altair as alt
alt.themes.enable("streamlit")

uf = st.file_uploader("Choose a CSV file", type=["csv"])

# If a file was uploaded, read the contents into a Pandas DataFrame
if uf is not None:
    df2 = pd.read_csv(uf)
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])
    st.table(df2.head(5))
        # Convert 'timestamp' column to a pa
    # Load dta from CSV file
    # df2 = pd.read_csv('data.csv')

    # Create a checkbox to toggle data points with true/false labels
    show_true = st.checkbox('Show True Labels')

    # Filter the data based on the checkbox value
    if show_true:
        dta = df2
        chart1 = alt.Chart(dta).mark_point(size=10).encode(
            x='timestamp:T',
            y='sentiment:Q',
            color=alt.Color('bp_label', scale=alt.Scale(domain=['True', 'False'], range=['red', 'blue'])),
            tooltip=['tweet']
        ).interactive().add_selection(selection)
        st.altair_chart((chart1), use_container_width=True)


    else:
        dta = df2[df2['bp_label'] == False]


    # Create a selection for the tooltip
        selection = alt.selection_single(fields=['timestamp'], nearest=True, on='mouseover', empty='none')

        # Create the chart
        chart1 = alt.Chart(dta).mark_point(size=10).encode(
            x='timestamp:T',
            y='sentiment:Q',
            color=alt.Color('bp_label', scale=alt.Scale(domain=['True', 'False'], range=['red', 'blue'])),
            tooltip=['tweet']
        ).interactive().add_selection(selection)
        st.altair_chart((chart1), use_container_width=True)


    # Add a line that follows the selected timestamp
    line1 = chart1.transform_filter(selection).mark_line(color='black')

    # Add the chart and line to the Streamlit app
