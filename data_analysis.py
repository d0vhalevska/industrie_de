import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/opt/homebrew/anaconda3/envs/scrapy_env/industrie_de/cleaned_output.csv')

# Generate descriptive statistics
descriptive_stats = df.describe(include='all')
print(descriptive_stats)

sns.set_style("whitegrid")

#plot for the distribution of missing values
plt.figure(figsize=(10, 6))
#getting all NaN entries and summing them up
missing_values = df.isnull().sum()
sns.barplot(x=missing_values.index, y=missing_values.values)
plt.title('Distribution of Missing Values')
plt.ylabel('Number of Missing Values')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#plot distribution of establishment years
plt.figure(figsize=(14, 6))
sns.histplot(df['Established'].dropna(), bins=30, kde=True)
plt.title('Distribution of Company Establishment Year')
plt.xlabel('Year')
plt.ylabel('Number of Companies')
plt.show()
