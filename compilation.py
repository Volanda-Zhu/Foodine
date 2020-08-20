import pandas as pd

# calculates the total number of restaurants scraped from each website
merged = pd.read_csv(".\data\merge_data_final.csv")
print(merged.head(10))

zomato = pd.read_excel(".\data\ScrapedData.xlsx",sheet_name="Zomato_clean")
dzdp = pd.read_excel(".\data\ScrapedData.xlsx",sheet_name="Dazhongdianping_clean")
yelp = pd.read_excel(".\data\ScrapedData.xlsx",sheet_name="Yelp_clean")
ta = pd.read_excel(".\data\ScrapedData.xlsx",sheet_name="Tripadvisor_clean")

dict1 = {'Zomato': len(zomato.index), 'Yelp': len(yelp.index), 'Dazhongdianping': len(dzdp.index), 'TripAdvisor': len(ta.index)}
summary_df1 = pd.DataFrame.from_dict(dict1,orient='index', columns=['Number of Restaurants'])
print(summary_df1)

dict2 = {'Total Number of Cuisine type ': len(merged['cuisine_style'].unique()),
         'Total number of Neighbourhoods ': len(merged.area.unique())}
summary_df2 = pd.DataFrame.from_dict(dict2, orient='index', columns=[' '])
print(summary_df2)
