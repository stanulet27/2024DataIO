import os
import pandas as pd
import plotly.express as px


def bubble_map_data(df, month):
        # Create a new DataFrame for start locations
        start_locations = df[['start_lat', 'start_lng']]
        start_locations['type'] = 'start'
        # Create a new DataFrame for end locations
        end_locations = df[['end_lat', 'end_lng']]
        end_locations['type'] = 'end'
        # Rename columns for consistency
        start_locations.columns = ['latitude', 'longitude', 'type']
        end_locations.columns = ['latitude', 'longitude', 'type']
        # Concatenate start and end location DataFrames
        all_locations = pd.concat([start_locations, end_locations])
        # Count occurrences for each location
        location_counts = all_locations.groupby(['latitude', 'longitude', 'type']).size().reset_index(name='count')
        # Add a new column for the month
        location_counts['month'] = month
        return location_counts

# Directory containing CSV files for each month
data_directory = 'Data'  # Replace with the path to your directory

# Create an empty DataFrame to store combined data
combined_data_bubble = pd.DataFrame(columns=['latitude', 'longitude', 'type', 'count', 'month'])

# Iterate through each CSV file in the directory
for filename in os.listdir(data_directory):
    if filename.endswith('.csv'):
        # Read the CSV file into a pandas DataFrame
        csv_path = os.path.join(data_directory, filename)
        df = pd.read_csv(csv_path)
        # Append data to the combined DataFrame
        filename = filename[2:]
        combined_data_bubble = pd.concat([combined_data_bubble, bubble_map_data(df, filename[:-4])])

combined_data_bubble['count'] = combined_data_bubble['count'].astype(int)

# Plot as animated bubble map using Plotly Express with specified range
fig = px.scatter_mapbox(combined_data_bubble,
                        lat='latitude',
                        lon='longitude',
                        size='count',
                        color='type',
                        hover_name='count',
                        animation_frame='month',
                        animation_group='latitude',  # Ensure smooth transitions
                        mapbox_style='open-street-map',
                        title='Animated Bubble Map of Start and End Locations',
)

# Show the plot or save it as an HTML file
# fig.show()
output_filename = 'animated_bubble_map.html'
fig.write_html(output_filename)

print(f'Animated bubble map created and saved as {output_filename}')
