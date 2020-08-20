#dzdp.py scrape information of restaurants in Pittsburgh on Dazhongdianping website's downloaded html 
#and generates a DataFrame with columns cotaining name, address, rating for a restaurant
#finally it saves the DataFrame as a cvs file named 'dazhongdianping.csv'

from bs4 import BeautifulSoup
import pandas as pd

path=".\data\DZDP_web"

#function that gets info of restaurants on the web page
def analysierenhtml(html):

    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('li',class_="")
    ul=[]

    for link in links:
        if link.h4 != None:#get restaurant name
            name=link.h4.string
            print('{:^50s}'.format(link.h4.string))#print reataurant name 

            a5 = link.find('div', class_='comment')#get rating
            if a5:  
                rating=int(a5.span['class'][1][-2:])/10
            else: 
                rating=' '   


            span1 = link.find('span', {'class': 'addr'})#get restaurant address
            if span1:
                address=span1.string
            else:
                address=' '

            ul.append([name,address,rating])  
    return ul

#invoke analysierenhtml function to get info for all restaurants and put them in a list
final_list=[]
for i in range(42):
    file_name=path+'\\p'+str(i+1)+'.html'
    with open(file_name,encoding="utf8") as html_file:
        final_list.extend(analysierenhtml(html_file))

#turn the list into a dataFrame
final_pd=pd.DataFrame(final_list,columns=['name','address','dzdp_rating'])

#store the DataFrame to a csv file named 'Dazhongdianping.csv'
export_csv=final_pd.to_csv(r'Dazhongdianping.csv',index=None,header=True)
