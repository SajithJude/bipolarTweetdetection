import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins
import streamlit.components.v1 as components

# Load the data
data = pd.read_csv("data/streamlitdatabase.csv", parse_dates=['timestamp'])
# st.table(data)
# Sidebar filters
x_axis = st.sidebar.selectbox('Select X-axis', ['timestamp', 'bp_label', 'hour', 'weekday', 'patient_index'])
y_axis = st.sidebar.selectbox('Select Y-axis', ['timestamp', 'bp_label', 'hour', 'weekday', 'patient_index'])
patient_filter = st.sidebar.selectbox("Select a patient", list(range(1, 26)))

# This code first loads the data from a CSV file into a DataFrame,
#  and assumes that the timestamp column has already been parsed as dates.
#   It then uses the value_counts method to count the occurrences of each hour 
#   in the timestamp column, and finds the index (i.e. hour) of the most common
#    value using the idxmax method. It then prints out the most common timestamp 
#    range by adding 1 to the index to get the end of the hour range.
# Similarly, it counts the occurrences of each weekday in the weekday column using 
# value_counts, finds the index of the most common value using idxmax, and prints out
#  the most common weekday.


x_axis_counts = df[x_axis].dt.hour.value_counts()
y_axis_counts = df[y_axis].dt.hour.value_counts()

mostcomonXaxis = x_axis_counts.idxmax()
mostcomonYaxis = y_axis_counts.idxmax()



y_low, y_up = st.sidebar.slider('Select Y limit range',  0, mostcomonYaxis, (0, timestamp_counts))
x_low, x_up = st.sidebar.slider('Select X limit range', 0, mostcomonXaxis, (0, timestamp_counts))

# Filter the data based on the selected patient index
filtered_data = data[data['patient_index'] == patient_filter]

# Create the scatter plot
fig, ax = plt.subplots()
scatter = ax.scatter(filtered_data[x_axis], filtered_data[y_axis], alpha=0.5,cmap="coolwarm")


# the c parameter of the scatter method is set to df_filtered["bp_label"],
#  which means the color of each data point will be determined by the bp_label column. 
#  The cmap parameter is set to "coolwarm", which is a colormap 
#  that ranges from cool colors (e.g. blue) for False values to warm colors (e.g. red) for True values.
#   If you want to use a different color scheme, you can replace "coolwarm" with the name of another colormap.
# To change the color of the scatter points themselves (as opposed to the color of the markers), 
# you can add the edgecolors parameter to the scatter method with your desired color. 
# For example, to make the points black, you can add edgecolors='black' to the scatter method.



# Add tooltip with tweet text
tooltip = plugins.PointHTMLTooltip(scatter, labels=list(filtered_data['tweet']))
plugins.connect(fig, tooltip)

# Format the plot
plt.xlabel(x_axis)
plt.ylabel(y_axis)


colorbar = plt.colorbar(scatter)
colorbar.set_label("Bipolar Label")



plt.title(f'Scatter Plot of {x_axis} vs {y_axis} for Patient {patient_filter}')
plt.ylim(y_low, y_up)
plt.xlim(x_low, x_up)

# Convert the plot to an interactive HTML
html_graph = mpld3.fig_to_html(fig)

# Display the interactive HTML graph
components.html(html_graph, height=600)
