import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#######################################################################################################################
# This file fetches top 100 restaurants based on rating from each website - Yelp, Dazhongdianping(dzdp), TripAdvisor(ta) and Zomato
# Counts the number of restaurants in each category and displays the result in a stacked bar chart
# Certain categories have been combined in to one generic category.
# For example -Japanese,Chinese,Thai,Korean,Vietnamese have been combined to Asian and so on.
# categories which were very few in number - like Carribean etc are grouped as Other
#######################################################################################################################

merged = pd.read_csv(".\data\merge_data_final.csv")
# merged['zomato_rating'] = pd.to_numeric(merged['zomato_rating'], errors='coerce').fillna(0).astype(float)

zomato = merged.sort_values('zomato_rating', ascending=False)
top_restaurant = zomato[:101]
zomato = top_restaurant.groupby(['cuisine_style']).size().to_frame('count').reset_index()
zomato = zomato.sort_values('count', ascending=False)
zomato = zomato.reset_index(drop=True)

lst_Asian = ['Asian', 'Chinese', 'Japanese', 'Thai', 'Korean', 'Vietnamese']
lst_Italian = ['Italian', 'Pizza']
lst_European = ['European', 'French', 'German']
lst_Latin = ['Latin American', 'Brazilian', 'Mexican']
lst_FastFood = ['Fast Food']
zomato.loc[zomato['cuisine_style'].isin(lst_Asian), "cuisine_style"] = 'Asian'
zomato.loc[zomato['cuisine_style'].isin(lst_Italian), "cuisine_style"] = 'Italian'
zomato.loc[zomato['cuisine_style'].isin(lst_European), "cuisine_style"] = 'European'
zomato.loc[zomato['cuisine_style'].isin(lst_Latin), "cuisine_style"] = 'Latin American'
zomato.loc[~zomato['cuisine_style'].isin(
    lst_Latin + lst_European + lst_Italian + lst_Asian ), "cuisine_style"] = 'Other'

zomato = pd.pivot_table(zomato, index=['cuisine_style'], values=['count'], aggfunc='sum')

###############################################################################################################
# merged = pd.read_excel("C:/Users/anany/Documents/Ananya Ghosh/Semester 1/Subjects/Python/Project/restaurant_data.xlsx",
#                        sheet_name="merged_data")
merged['yelp_rating'] = pd.to_numeric(merged['yelp_rating'], errors='coerce').fillna(0).astype(float)
merged['dzdp_rating'] = pd.to_numeric(merged['dzdp_rating'], errors='coerce').fillna(0).astype(float)
merged['ta_rating'] = pd.to_numeric(merged['ta_rating'], errors='coerce').fillna(0).astype(float)
yelp = merged.sort_values('yelp_rating', ascending=False)
yelp_top_restaurant = yelp[:103]
dzdp = merged.sort_values('dzdp_rating', ascending=False)
dzdp_top_restaurant = dzdp[:108]
ta = merged.sort_values('ta_rating', ascending=False)
ta_top_restaurant = ta[:149]
yelp = yelp_top_restaurant.groupby(['cuisine_style']).size().to_frame('count').reset_index()
dzdp = dzdp_top_restaurant.groupby(['cuisine_style']).size().to_frame('count').reset_index()
ta = ta_top_restaurant.groupby(['cuisine_style']).size().to_frame('count').reset_index()

yelp = yelp.sort_values('count', ascending=False)
dzdp = dzdp.sort_values('count', ascending=False)
ta = ta.sort_values('count', ascending=False)

yelp = yelp.reset_index(drop=True)
dzdp = dzdp.reset_index(drop=True)
ta = ta.reset_index(drop=True)

yelp.loc[yelp['cuisine_style'].isin(lst_Asian), "cuisine_style"] = 'Asian'
yelp.loc[yelp['cuisine_style'].isin(lst_Italian), "cuisine_style"] = 'Italian'
yelp.loc[yelp['cuisine_style'].isin(lst_European), "cuisine_style"] = 'European'
yelp.loc[yelp['cuisine_style'].isin(lst_Latin), "cuisine_style"] = 'Latin American'
yelp.loc[~yelp['cuisine_style'].isin(
    lst_Latin + lst_European + lst_Italian + lst_Asian + lst_FastFood), "cuisine_style"] = 'Other'
yelp = pd.pivot_table(yelp, index=['cuisine_style'], values=['count'], aggfunc='sum')

dzdp.loc[dzdp['cuisine_style'].isin(lst_Asian), "cuisine_style"] = 'Asian'
dzdp.loc[dzdp['cuisine_style'].isin(lst_Italian), "cuisine_style"] = 'Italian'
dzdp.loc[dzdp['cuisine_style'].isin(lst_European), "cuisine_style"] = 'European'
dzdp.loc[dzdp['cuisine_style'].isin(lst_Latin), "cuisine_style"] = 'Latin American'
dzdp.loc[~dzdp['cuisine_style'].isin(
    lst_Latin + lst_European + lst_Italian + lst_Asian + lst_FastFood), "cuisine_style"] = 'Other'
dzdp = pd.pivot_table(dzdp, index=['cuisine_style'], values=['count'], aggfunc='sum')

ta.loc[ta['cuisine_style'].isin(lst_Asian), "cuisine_style"] = 'Asian'
ta.loc[ta['cuisine_style'].isin(lst_Italian), "cuisine_style"] = 'Italian'
ta.loc[ta['cuisine_style'].isin(lst_European), "cuisine_style"] = 'European'
ta.loc[ta['cuisine_style'].isin(lst_Latin), "cuisine_style"] = 'Latin American'
ta.loc[~ta['cuisine_style'].isin(
    lst_Latin + lst_European + lst_Italian + lst_Asian ), "cuisine_style"] = 'Other'
ta = pd.pivot_table(ta, index=['cuisine_style'], values=['count'], aggfunc='sum')
ta_lst = []
yelp_lst = []
dzdp_lst = []
zomato_lst = []
for row in ta.values:
    ta_lst.append(int(str(row).strip('[]')))
for row in yelp.values:
    yelp_lst.append(int(str(row).strip('[]')))
for row in zomato.values:
    zomato_lst.append(int(str(row).strip('[]')))
for row in dzdp.values:
    dzdp_lst.append(int(str(row).strip('[]')))


final_df = pd.DataFrame(index=['Asian','European','Italian','Latin American','Other'])
final_df["Yelp"]=yelp_lst

final_df["Dazhongdianping"]=dzdp_lst
final_df["Zomato"]=zomato_lst
final_df["TripAdvisor"]=ta_lst
final_df.transpose().plot(kind='bar',stacked=True, color=sns.color_palette("BuPu_r"))
plt.show()

#######################################################################################################################

