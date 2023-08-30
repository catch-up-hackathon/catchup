import requests
import xml.etree.ElementTree as ET

def call_api(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        return None

def get_product_data(key, keyword, option=None):
    base_url = "http://openapi.11st.co.kr/openapi/OpenApiService.tmall"
    
    # 기본정보조회
    product_search_url = f"{base_url}?key={key}&apiCode=ProductSearch&keyword={keyword}"
    if option:
        product_search_url += f"&option={option}"
    
    product_search_data = call_api(product_search_url)
    if not product_search_data:
        return None
    
    root = ET.fromstring(product_search_data)
    products = []
    for product in root.findall('.//Product'):
        product_code = product.find('ProductCode').text
        product_name = product.find('ProductName').text
        product_price = product.find('ProductPrice').text
        
        # 이미지검색요청
        product_image_url = f"{base_url}?key={key}&apiCode=ProductImage&productCode={product_code}"
        product_image_data = call_api(product_image_url)
        if not product_image_data:
            return None
        
        image_root = ET.fromstring(product_image_data)
        image_url = image_root.find('.//ImageURL').text
        
        products.append({
            'name': product_name,
            'price': product_price,
            'image_url': image_url,
        })
        
    return products
        
key = '72318adbdecc7fca2f56c2d8fabe89a0'
keyword = '핸드크림'
option = 'Categories'  # 카테고리검색요청을 위해 필요, 기본정보조회를 위해선 None으로 둡니다.

products = get_product_data(key, keyword, option)

if products:
    for product in products:
        print(f"Product Name: {product['name']}")
        print(f"Product Price: {product['price']}")
        print(f"Image URL: {product['image_url']}")
