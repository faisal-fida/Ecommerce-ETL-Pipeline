import json as Json
import pandas as pd
import numpy as np

df_final_products = pd.read_csv('output/df_final_products.csv')


def clean_data_step1():
    df_final_products["title"] = df_final_products["title"].str.lower()
    df_final_products["title"] = df_final_products["title"].str.replace(
        "/", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "+", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "^", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "-", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        ".", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "@", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "'", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "&", " ", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "  ", "-", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        " ", "-", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "--", "-", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        " -", "-", regex=False)
    df_final_products["title"] = df_final_products["title"].str.replace(
        "- ", "-", regex=False)

    df_final_products["category"] = df_final_products["category"].str.lower()
    df_final_products["category"] = df_final_products["category"].str.replace(
        "'", " ", regex=False)
    df_final_products["category"] = df_final_products["category"].str.replace(
        "  ", "-", regex=False)
    df_final_products["category"] = df_final_products["category"].str.replace(
        " ", "-", regex=False)
    df_final_products['sizeLabel'] = df_final_products['sizeLabel'].str.replace(
        "Size ", " ", regex=False)
    df_final_products['fabric'] = df_final_products['materials'].apply(
        lambda x: str(x).split()[1].replace("',", " ").replace("']", " ").lower().strip())
    df_final_products['color'] = df_final_products['colorNames'].apply(
        lambda x: str(x).split()[0].replace("['", " ").replace("']", " ").replace("',", " ").lower().strip())


def clean_data_step2(df):
    def id_to_url(image_id):
        return f"https://cf-assets-thredup.thredup.com/assets/{image_id}/retina.jpg"

    def extract_tags(row):
        values = [row['charsGeneral'],
                  row['charsCareInstructions'], row['charsAccent']]
        clean_values = [str(val).strip('[]').replace("'", " ").strip()
                        for val in values if val != [] and val != None and val != np.nan]
        tags = [x for x in filter(None, clean_values)]
        return tags
    df['Images'] = df_final_products['photoIds'].apply(
        lambda x: str(x).replace('[', '').replace(']', '').replace(' ', '').split(','))
    df['Images'] = df_final_products['photoIds'].apply(
        lambda x: [id_to_url(id) for id in eval(str(x))])
    df_final_products['charsGeneral'].dropna(inplace=True)
    df_final_products['charsCareInstructions'].dropna(inplace=True)
    df_final_products['charsAccent'].dropna(inplace=True)
    df['Tags'] = df_final_products.apply(extract_tags, axis=1)
    df['Name'] = "women-" + df_final_products['fabric'].astype(str) + "-" + df_final_products['title'].astype(
        str) + "-" + df_final_products['color'].astype(str) + "-" + df_final_products['category'].astype(str)
    df['URL'] = "https://www.thredup.com/product/" + \
        df['Name'].astype(str) + "/" + \
        df_final_products['itemNumber'].astype(str)
    df['Size Category'] = df_final_products.apply(lambda x: np.nan if x['merchandisingDepartment'] ==
                                                  'X' else 'Petite' if x['merchandisingDepartment'] == 'women' else 'Plus' if x['merchandisingDepartment'] == 'plus' else '', axis=1)
    df['Condition'] = df_final_products.apply(lambda x: 'Excellent' if x['qualityCode'] ==
                                              'Q1' else 'Very Good' if x['qualityCode'] == 'Q2' else 'Good' if x['qualityCode'] == 'Q2' else '', axis=1)


def clean_data_step3(df):
    df['Item #'] = df_final_products['itemNumber']
    df['objectID'] = df['Item #']
    df['Price'] = df_final_products['price']
    df['Brand'] = df_final_products['brand']
    df['Size'] = df_final_products['sizeLabel']
    df['Inseam Measurement (Inches)'] = df_final_products['charsInseamIn']
    df['Rise Measurement (Inches)'] = df_final_products['charsRiseIn']
    df['Waist Measurement (Inches)'] = df_final_products['charsWaistIn']
    df['Rise'] = df_final_products['charsWaist']
    df['Pant Cut'] = df_final_products['charsPantCut']
    df['New with Tags'] = df_final_products['newWithTags']
    df['Color'] = df_final_products['colorNames']
    df['Jean Wash'] = df_final_products['charsJeanWash']
    df['Number Favorites'] = df_final_products['favoriteCount']
    df['Material'] = df_final_products['materials']
    df['Pattern'] = df_final_products['charsPattern']
    df['Accents'] = df_final_products['charsAccent']


def clean_data():
    df = pd.DataFrame()

    clean_data_step1()
    clean_data_step2(df)
    clean_data_step3(df)

    df = df[['objectID', 'URL', 'Item #', 'Name', 'Images', 'Price', 'Brand', 'Size',
             'Size Category', 'Inseam Measurement (Inches)',
             'Rise Measurement (Inches)', 'Waist Measurement (Inches)', 'Rise',
             'Pant Cut', 'Condition', 'New with Tags', 'Color', 'Jean Wash',
             'Number Favorites', 'Material', 'Pattern', 'Accents', 'Tags']]

    with open('output/Latest_Products_Data.json', 'w') as f:
        dataJson = Json.loads(df.to_json(orient='records'))
        Json.dump(dataJson, f, indent=4, separators=(',', ':'))

    print("Json Products saved in the Directory.")

    return dataJson
