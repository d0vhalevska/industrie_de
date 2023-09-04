import pandas as pd
import re

df = pd.read_csv('/opt/homebrew/anaconda3/envs/scrapy_env/industrie_de/output.csv')

#delete </dd> in some address entries
df['Address'] = df['Address'].str.replace('</dd>', '').str.strip()

#replace NaN values with 'N/A'
df.fillna('N/A', inplace=True)

#getting rid of e.g. <a href="http://www.xsuite.com" target="_blank">www.xsuite.com</a>
def extract_url(html_string):
    # Further simplified function to extract URL from href attribute
    match = re.search(r'href="([^"]+)"', html_string)
    return match.group(1) if match else html_string

# Correct the 'Website' column
df['Website'] = df['Website'].apply(extract_url)

#getting rid of e.g. <a href="mailto:info@xsuite.com">info@xsuite.com</a>
def extract_email(html_string):
  # Function to extract email from mailto attribute
  match = re.search(r'mailto:([^"]+)', html_string)
  return match.group(1) if match else html_string

df['Email'] = df['Email'].apply(extract_email)

#extract numbers from 'Employees'
df['Employees'] = df['Employees'].str.extract('(\d+)')[0].str.replace(',', '').fillna('N/A')

#extract numbers (years) from 'Established'
df['Established'] = df['Established'].str.extract('(\d{4})')[0].fillna('N/A')

df.to_csv('/opt/homebrew/anaconda3/envs/scrapy_env/industrie_de/cleaned_output.csv', index=False)

