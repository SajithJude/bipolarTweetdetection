import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mpld3

# Load the data
data = pd.read_csv('data/streamlitdatabase.csv', parse_dates=['timestamp'])

# Sidebar filters
x_var = st.sidebar.selectbox('X-axis variable', ['hour', 'weekday', 'timestamp'])
y_var = st.sidebar.selectbox('Y-axis variable', ['hour', 'weekday', 'timestamp'])
patient_filter = st.sidebar.slider('Patient index', 1, 25, 1)

# Filter the data
data_filtered = data[data['patient_index'] == patient_filter]

# Create the scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(data_filtered[x_var], data_filtered[y_var], c=data_filtered['bp_label'])

# Add tooltip with tweet text
tooltip = mpld3.plugins.PointHTMLTooltip(scatter, labels=data_filtered['tweet'])
mpld3.plugins.connect(fig, tooltip)

# Show the plot
mpld3.show(fig)

