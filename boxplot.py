import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
#########################################################################################
# displays 4 boxplots, showing how ratings vary amongst 4 websites according to category.
# top 4 categories were chosen for this
#########################################################################################


merged = pd.read_csv(".\data\merge_data_final.csv")

lst_Asian = ['Asian', 'Chinese', 'Japanese', 'Thai', 'Korean', 'Vietnamese']
lst_Italian = ['Italian', 'Pizza']
lst_European = ['European', 'French', 'German']
lst_Latin = ['Latin American', 'Brazilian', 'Mexican']
lst_FastFood = ['Fast Food']

merged.loc[merged['cuisine_style'].isin(lst_Asian), "cuisine_style"] = 'Asian'
merged.loc[merged['cuisine_style'].isin(lst_Italian), "cuisine_style"] = 'Italian'
merged.loc[merged['cuisine_style'].isin(lst_European), "cuisine_style"] = 'European'
merged.loc[merged['cuisine_style'].isin(lst_FastFood), "cuisine_style"] = 'Fast Food'
merged.loc[~merged['cuisine_style'].isin(
    lst_Latin + lst_European + lst_Italian + lst_Asian + lst_FastFood), "cuisine_style"] = 'Other'

list_wanted = ['Fast Food', 'Italian', 'European', 'Asian']
df_plot = merged[['cuisine_style', 'yelp_rating', 'dzdp_rating', 'zomato_rating', 'ta_rating']]
df_plot = df_plot.rename(columns={'yelp_rating': 'Yelp', 'dzdp_rating': 'Dazhongdianping', 'zomato_rating': 'Zomato',
                                  'ta_rating': 'TripAdvisor'})
#Asian boxplot
df_plot = df_plot[df_plot['cuisine_style'].isin(list_wanted)]
df_plot = df_plot.reset_index(drop=True)
df_Asian = df_plot[df_plot['cuisine_style'] == 'Asian']
sns.boxplot(data=df_Asian, palette=sns.color_palette("Set2")).set_title('Asian')
plt.show()

#European boxplot
df_Euro = df_plot[df_plot['cuisine_style'] == 'European']
sns.boxplot(data=df_Euro, palette=sns.color_palette("Set2")).set_title('European')
plt.show()

#Fast Food boxplot
df_American = df_plot[df_plot['cuisine_style'] == 'Fast Food']
sns.boxplot(data=df_American, palette=sns.color_palette("Set2")).set_title('Fast Food')
plt.show()

#Italian boxplot
df_Italian = df_plot[df_plot['cuisine_style'] == 'Italian']
sns.boxplot(data=df_Italian, palette=sns.color_palette("Set2")).set_title('Italian')
plt.show()
