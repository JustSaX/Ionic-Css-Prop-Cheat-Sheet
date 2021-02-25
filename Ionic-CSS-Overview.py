from bs4 import BeautifulSoup
import requests
import pandas as pd

page = requests.get('https://ionicframework.com/docs/api')

soup = BeautifulSoup(page.content, 'html.parser')

#save all links containing /docs/api/ in list
link_to_ui_elements = [link.get('href') for link in soup.find_all('a') if link.get('href') is not None and '/docs/api/' in link.get('href')]
# remove doubles in case there are
link_to_ui_elements = list(dict.fromkeys(link_to_ui_elements))

#create dictionary with ui components as keys and css props as values
css_props = {} 
for link in link_to_ui_elements:
    link_complete = 'https://ionicframework.com' + link
    ui_name = link.replace('/docs/api/','')

    print(link_complete)
    
    page = requests.get(link_complete)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find(id='css-custom-properties')

    if table is not None:  #if there are no CSS custom properties table will be none
        table_content = table.next_sibling
    else:
        pass

    my_table = []
    for row in table_content.findAll('tr'):
        temp = []
        for th in row.findAll('td'):
            temp.append(th.text)
        my_table.append(temp)
    my_table = [x[0] for x in my_table if len(x)!=0] #remove all []

    css_props[ui_name]=my_table

css_props_list = []
for ui_elem in list(css_props.values()):
    css_property = []
    for css_prop in ui_elem:
        css_property.append(css_prop)
    css_props_list.append(css_property)

#create list that contains all CS properties without duplicates:
all_css_props = []
for row in css_props_list:
    for css_prop in row:
        if css_prop not in all_css_props:
            all_css_props.append(css_prop)

is_applicable_matrix = []
for css_prop in all_css_props:
    temp = []
    for key in css_props.keys():
        if css_prop in css_props[key]:
            temp.append('x')
        else:
            temp.append('')
    is_applicable_matrix.append(temp)

df = pd.DataFrame(is_applicable_matrix, columns=css_props.keys(), index=all_css_props)

with open("Ionic-CSS-Prop-Cheat-Sheat.csv", 'w') as file:
    file.write(df.to_csv())
