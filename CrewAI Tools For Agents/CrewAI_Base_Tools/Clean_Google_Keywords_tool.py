import os
import pandas as pd

# Define root directory
root_directory = os.path.dirname(os.path.abspath(__file__))

# Define input directory two levels up from root
input_directory = os.path.join(root_directory, "..", "..", "Google_Keywords_Uncleaned")

# Create input directory if it doesn't exist
os.makedirs(input_directory, exist_ok=True)

# Define output directory two levels up from root
output_directory = os.path.join(root_directory, "..", "..", "Google_Keywords_Cleaned", "SEO", "Data")

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through each file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".xlsx"):
        # Read the data from the Excel file
        file_path = os.path.join(input_directory, file_name)
        df = pd.read_excel(file_path, header=None)
        
        # Extract directory name from cell A1 and create the directory if it doesn't exist
        directory_name = df.iloc[0, 0].strip()  # Strip to remove any leading/trailing spaces
        output_subdirectory = os.path.join(output_directory, directory_name)
        os.makedirs(output_subdirectory, exist_ok=True)
        
        # Extract the file name from cell A2
        output_file_name = df.iloc[1, 0].strip() + ".csv"  # Strip to remove any leading/trailing spaces

        # Find the row index where the actual header is located
        header_row_index = df[df.apply(lambda row: row.str.contains('Keyword', na=False)).any(axis=1)].index[0]

        # Use the row above the header row as the actual header
        df.columns = df.iloc[header_row_index]

        # Remove unnecessary rows before the header
        df = df.iloc[header_row_index + 1:]

        # Reset index
        df.reset_index(drop=True, inplace=True)

        # Remove columns with no data except for the header
        df = df.dropna(axis=1, how='all')

        # Remove columns with just one row of data
        df = df.dropna(thresh=2)

        # Add two columns "Search Intent" and "Focus"
        df["Search Intent"] = ""
        df["Focus"] = ""

        # Write the cleaned data to a new CSV file inside the output subdirectory
        output_file_path = os.path.join(output_subdirectory, output_file_name)
        df.to_csv(output_file_path, index=False)
