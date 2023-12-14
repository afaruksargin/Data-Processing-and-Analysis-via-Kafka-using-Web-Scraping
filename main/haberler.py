from bs4 import BeautifulSoup
import requests
import time
import csv
import pandas as pd
from datetime import datetime
import locale
from googletrans import Translator


data = {
    'Title': [],
    'SpotTitle':[],
    'Time': [],
    'Content': []
}


def transform_time(date):

    locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

    date_time_str = ' '.join(date.split(' ')[1:6])

    date_time_obj = datetime.strptime(date_time_str, '%d %B %Y %A, %H:%M')

    return date_time_obj.strftime('%Y/%m/%d')

def link_finder(soup):
    link_list = []
    divs_box_4 = soup.find_all('div',class_='box box-4')
    divs_box_6 = soup.find_all('div',class_='box box-6')

    for div in divs_box_4:
        link = 'https://www.bloomberght.com/'+(div.find('a',attrs = {'class':'gtm-tracker'})).get('href')
        link_list.append(link)

    for div in divs_box_6:
        link = 'https://www.bloomberght.com/'+(div.find('a',attrs={'class':'gtm-tracker'})).get('href')
        link_list.append(link)
    
    return link_list

def translate_to_english(text):
    if text is not None:

        max_lenght= 5000
        translator = Translator()

        chunks = [text[i:i + max_lenght] for i in range(0, len(text), max_lenght)]

        translated_chunks = []

        for chunk in chunks:
            translated = translator.translate(chunk, src='tr', dest='en')
            translated_chunks.append(translated.text)

        translated_text = ' '.join(translated_chunks)
        return translated_text
    else:
        return None


def main():
    response = requests.get("https://www.bloomberght.com/haberler")

    if response.status_code ==200:
        page = BeautifulSoup(response.content, 'lxml')

        news= page.find_all('div', class_='box-row widget-box-news type1')
        link_list = []
        for new in news:
            return_list = link_finder(new)
            link_list.extend(return_list)

        for link in link_list:
            response = requests.get(link)
            if response.status_code ==200:
                page =BeautifulSoup(response.content, 'lxml')

                paragraphs = page.find('article',class_='content').find_all('p')

                page = page.find('section',attrs={'class':'featured type4'})

                title = page.find('h1', attrs={'class':'title'}).text
                title = title.strip()

                spot_title = page.find('h2', attrs={'class':'spot-title'})
                spot_title = '\n'.join(spot_title)

                time_tags = page.select('time')
                time_ = [ tag.get_text() for tag in time_tags][1]
                time_ = transform_time(time_)

                extracted_paragraphs = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True) ]
                paragraphs_as_string = '\n'.join(extracted_paragraphs)

                # Verileri sözlüğe ekleme
                data['Title'].append(title)
                data['SpotTitle'].append(spot_title)
                data['Time'].append(time_)
                data['Content'].append(paragraphs_as_string)
        df = pd.DataFrame(data)

        columns_to_translate = ['Title','SpotTitle','Content']  # Çevirilecek sütunlar
        translated_columns = {}

        for column in columns_to_translate:
            translated_columns[column + '_English'] = df[column].apply(translate_to_english)

        translated_df = pd.concat([df, pd.DataFrame(translated_columns)], axis=1)
        translated_df.drop(["Title","SpotTitle","Content"], axis=1, inplace=True)

        return translated_df
    else:
        print('Hatalı Gönderme')

if __name__ == '__main__':
    main()
