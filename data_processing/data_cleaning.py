import re
import numpy as np
import json as Json
import pandas as pd
from ast import literal_eval as str_to_list


def clean_data_step1(df_products):
    pattern = r'[\/\+\^.@\'&\s]+'
    df_products["title"] = df_products["title"].str.lower()
    df_products['title'] = df_products['title'].apply(lambda x: re.sub(pattern, '-', x)).str.strip('-')

    df_products["category"] = df_products["category"].str.lower()
    df_products["category"] = df_products["category"].str.replace("'", " ", regex=False)
    df_products["category"] = df_products["category"].str.replace("  ", "-", regex=False)
    df_products["category"] = df_products["category"].str.replace(" ", "-", regex=False)
    df_products['sizeLabel'] = df_products['sizeLabel'].str.replace("Size ", "", regex=False)
    df_products['fabric'] = df_products['materials'].apply(lambda x: str(x).split()[1].replace("',", " ").replace("']", " ").lower().strip())
    df_products['color'] = df_products['colorNames'].apply(lambda x: str(x).split()[0].replace("['", " ").replace("']", " ").replace("',", " ").lower().strip())


def clean_data_step2(df,df_products):
    def id_to_url(image_id):
        return f"https://cf-assets-thredup.thredup.com/assets/{image_id}/retina.jpg"

    def extract_tags(row):
        values = [row['charsGeneral'],row['charsCareInstructions'],row['charsAccent']]
        #clean_values = [str(val).strip('[]').replace("'", " ").strip() for val in values if val != [] and val != None and val != np.nan and val != 'nan']
        clean_values = [str(val).strip('[]').replace("'", " ").strip()for val in values if val not in ([], None, np.nan) and not pd.isna(val)]
        tags = [x for x in filter(None, clean_values)]
        return tags

    df['Images'] = df_products['photoIds'].apply(lambda x: str(x).replace('[', '').replace(']', '').replace(' ', '').split(','))
    df['Images'] = df_products['photoIds'].apply(lambda x: [id_to_url(id) for id in eval(str(x))])
    
    df_products['charsGeneral'].dropna(inplace=True)
    df_products['charsCareInstructions'].dropna(inplace=True)
    df_products['charsAccent'].dropna(inplace=True)
    
    df['Tags'] = df_products.apply(extract_tags, axis=1)
    df['Name'] = "women-" + df_products['fabric'].astype(str) + "-" + df_products['title'].astype(str) + "-" + df_products['color'].astype(str) + "-" + df_products['category'].astype(str)
    df['URL'] = "https://www.thredup.com/product/" + df['Name'].astype(str) + "/" + df_products['itemNumber'].astype(str)
    df['Size Category'] = df_products.apply(lambda x: np.nan if x['merchandisingDepartment'] == 'X' else 'Petite' if x['merchandisingDepartment'] == 'women' else 'Plus' if x['merchandisingDepartment'] == 'plus' else '', axis=1)
    df['Condition'] = df_products.apply(lambda x: 'Excellent' if x['qualityCode'] =='Q1' else 'Very Good' if x['qualityCode'] == 'Q2' else 'Good' if x['qualityCode'] == 'Q2' else '', axis=1)


def clean_data_step3(df,df_products):
    df['Item #'] = df_products['itemNumber']
    df['objectID'] = df['Item #']
    df['Price'] = df_products['price']
    df['Brand'] = df_products['brand']
    df['Size'] = df_products['sizeLabel']
    df['Inseam Measurement (Inches)'] = df_products['charsInseamIn']
    df['Rise Measurement (Inches)'] = df_products['charsRiseIn']
    df['Waist Measurement (Inches)'] = df_products['charsWaistIn']
    df['Rise'] = df_products['charsWaist']
    df['Pant Cut'] = df_products['charsPantCut']
    df['New with Tags'] = df_products['newWithTags']
    df['Color'] = df_products['colorNames'].apply(lambda x: str_to_list(x) if isinstance(x, str) else x)
    df['Jean Wash'] = df_products['charsJeanWash'].apply(lambda x: str_to_list(x) if isinstance(x, str) else x)
    df['Number Favorites'] = df_products['favoriteCount']
    df['Material'] = df_products['materials'].apply(lambda x: str_to_list(x) if isinstance(x, str) else x)
    df['Pattern'] = df_products['charsPattern'].apply(lambda x: str_to_list(x) if isinstance(x, str) else x)
    df['Accents'] = df_products['charsAccent'].apply(lambda x: str_to_list(x) if isinstance(x, str) else x)
    df['SearchTags'] = df_products['searchTags'].apply(lambda x: str_to_list(x) if isinstance(x, str) else x)
    df['SellThroughScore'] = df_products['sellthroughScore'].apply(lambda x: str_to_list(x) if isinstance(x, str) else x)


def clean_data():
    df = pd.DataFrame()
    df_products = pd.read_csv('output/df_products.csv')
    clean_data_step1(df_products)
    clean_data_step2(df,df_products)
    clean_data_step3(df,df_products)

    df = df[['objectID', 'URL', 'Item #', 'Name', 'Images', 'Price', 'Brand', 'Size',
             'Size Category', 'Inseam Measurement (Inches)',
             'Rise Measurement (Inches)', 'Waist Measurement (Inches)', 'Rise',
             'Pant Cut', 'Condition', 'New with Tags', 'Color', 'Jean Wash',
             'Number Favorites', 'Material', 'Pattern', 'Accents', 'Tags',  'SellThroughScore', 'SearchTags']]

    with open('output/Latest_Products_Data.json', 'w') as f:
        dataJson = Json.loads(df.to_json(orient='records'))
        Json.dump(dataJson, f, indent=4, separators=(',', ':'))

    print("Json Products saved in the Directory.")

    return dataJson
