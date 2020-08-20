import matplotlib.pyplot as plt
# pip install squarify (algorithm for treemap)
import squarify
import seaborn as sns
import pandas as pd
#######################################################################################################################
# This file displays a treemap comparing different areas based on the number of restaurants present
# It also displays a pie chart showing proportions of cuisine categories - Chinese, American etc
# And proportion of restaurants based on price range
#######################################################################################################################


merged = pd.read_csv(".\data\merge_data_final.csv")
area = merged.area.unique()
area_group = merged.groupby(['area']).size().to_frame('count').reset_index()
area_group = area_group.sort_values('count', ascending=False)
area_group = area_group.reset_index(drop=True)
area_top30 = area_group[:30]
# area_top30.loc[30] =['other',2430]
colors = sns.color_palette("BuPu",4)
squarify.plot(sizes=area_top30['count'], color=colors,label=area_top30.area, alpha=.8)
plt.axis('off')
plt.show()


# Price Range pie chart
price=merged[merged['cost'].notnull()].cost.value_counts()
labels = ['$','\$\$','\$\$\$','\$\$\$\$']
sizes = price.values
explode = (0, 0, 0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90,colors=sns.diverging_palette(220, 20, n=7))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Propotion of Price Range')

plt.show()


##cuisine Style pie chart
styles=8
cuisine=merged[merged['cuisine_style'].notnull()]['cuisine_style'].value_counts()
cuisine[styles]=cuisine[styles:].sum()
cuisine=cuisine.rename(index={cuisine.index[styles]:'Others'})
labels = cuisine[:styles+1].index
sizes = cuisine[:styles+1].values
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90,colors=sns.diverging_palette(220, 20, n=7))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Propotion of Cuisine_Styles')
plt.show()