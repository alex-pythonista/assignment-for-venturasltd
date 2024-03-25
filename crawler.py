import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

baseurl = 'https://shop.adidas.jp/'

def make_breadcrumb_string(breadcrumbs):
    breadcrumbs.pop(0)
    temp_list = [breadcrumb.text.strip() for breadcrumb in breadcrumbs]
    return '/ '.join(temp_list)
        
def get_image_url(src):
    return baseurl + src

def make_available_size_string(available_sizes):
    temp_list = [available_size.text.strip() for available_size in available_sizes]
    return ', '.join(temp_list)

def make_description_list(itemized_description):
    temp_list = [item.text.strip() for item in itemized_description]
    return '\n'.join(temp_list)

def group_keywords(keywords):
    temp_list = [keyword.text.strip() for keyword in keywords]
    return ', '.join(temp_list)

product_dict_list = []
counter = 1
for page in range(1, 5):

    apiurl = f'https://shop.adidas.jp/f/v1/pub/product/list?order=5&page={page}&q=%E3%83%88%E3%83%A9%E3%83%83%E3%82%AF%E3%82%B8%E3%83%A3%E3%82%B1%E3%83%83%E3%83%88&searchbox=1'

    r = requests.get(apiurl)
    res = r.json()
    product_list = res['articles_sort_list']

    for product in product_list:
        product_details = requests.get(baseurl + 'products/' +f'{product}')
        soup = bs(product_details.content, 'html.parser')

        product_infos = {
            'breadcrumbs_string': make_breadcrumb_string(soup.find_all('li', class_='breadcrumbListItem')),
            'product_url': f'{baseurl}product/{product}', # product url
            'category': soup.find('span', class_='categoryName').text.strip(), # category
            'product_name': soup.find('h1', class_='itemTitle').text.strip(), # product name
            'price': soup.find('p', class_='price-text').text.strip(),
            'image_url': get_image_url(soup.find('img', class_='test-img')['src']),
            'avaiable_sizes': make_available_size_string(soup.find_all('li', class_='sizeSelectorListItem')),
            'coordinated_product': '',
            'coordinated_price': '',
            'coordinated_product_number': '',
            'coordinated_product_imageurl': '',
            'coordinated_product_pageurl': '',
            'title_of_description': soup.find('h4', class_='itemFeature').text.strip(),
            'general_description': soup.find('div', class_='commentItem-mainText').text.strip(),
            'general_description_itemized': make_description_list(soup.find_all('ul', class_='articleFeatures')),
            'tale_of_size': '',
            'rating': '',
            'no. of rating': '',
            'reviewer_data': '',
            'keywords': group_keywords(soup.find_all('a', class_='css-1ka7r5v'))
        }
        # print(product_infos)
        product_dict_list.append(product_infos)

        print(f"product_count: {counter}")
        counter+=1

dataframe = pd.DataFrame(product_dict_list)
dataframe.to_csv('adidas_mens_collection.csv', index=False, encoding='utf-8')

