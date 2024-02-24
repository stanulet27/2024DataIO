import pandas as pd
import numpy as np
import plotly.express as px
import os

def density_map_data(df, name):
    dMd = pd.DataFrame(columns = ['lat', 'long', 'mag', 'month'])
    numberOfCoords = len(df['start_lat'])
    dMd['lat'] = pd.concat([df['start_lat'], df['end_lat']], ignore_index=True)
    dMd['long'] = pd.concat([df['start_lng'], df['end_lng']], ignore_index=True)
    dMd['mag'] = np.where(dMd.index > numberOfCoords,5,-5)
    dMd['coord'] = dMd['lat'].astype(str) + ', ' + dMd['long'].astype(str)
    dMdr = dMd.groupby('coord')['mag'].mean().reset_index()
    dMdr[['lat','long']] = dMdr['coord'].str.split(',',expand=True)
    dMdr['lat'] = dMdr['lat'].astype(np.float64)
    dMdr['long'] = dMdr['long'].astype(np.float64)
    dMdr['month'] = name
    return dMdr

data_directory = 'Data'  # Replace with the path to your directory

combined_density_data = pd.DataFrame(columns=['lat', 'long', 'mag', 'month'])

for filename in os.listdir(data_directory):
    if filename.endswith('.csv'):
        csv_path = os.path.join(data_directory, filename)
        df = pd.read_csv(csv_path)
        filename = filename[2:]
        combined_density_data = pd.concat([combined_density_data ,density_map_data(df,filename[:-4])])


fig = px.density_mapbox(combined_density_data, 
                        lat='lat', 
                        lon='long', 
                        z='mag', 
                        radius=5,
                        color_continuous_scale=px.colors.diverging.oxy,
                        mapbox_style="open-street-map", animation_frame='month', 
                        title='Density Map of Start and End Locations')
output_filename = 'animated_density_map.html'
fig.write_html(output_filename)

print(f'Animated density map created and saved as {output_filename}')