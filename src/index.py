import pandas as pd
from app import app
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_file_path = os.path.join(project_root, 'src', 'data', 'Clean Sexual Harassment NY.csv')

# Load the CSV file once
df = pd.read_csv(csv_file_path, usecols=['year', 'PD_DESC', 'CMPLNT_NUM', 'BORO_NM', 'victim_sex_rand', 'victim_age_rand', 'suspector_sex_rand', 'suspector_age_rand', 'LOC_OF_OCCUR_DESC',
                                         'HOUR', 'PREM_TYP_DESC', 'Lat_Lon'])

# Create a function to get the dataset
def get_data():
    return df

server = app.server  # Expose the server for deployment

if __name__ == "__main__":
    app.run_server(debug=False)