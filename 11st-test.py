import dotenv
import os
import requests
import xml.etree.ElementTree as ET

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
# API 엔드포인트 및 키 설정
api_url = "http://openapi.11st.co.kr/openapi/OpenApiService.tmall"
api_key = os.getenv("11ST_KEY")  # 실제 API 키로 대체하세요.
search_keyword = "핸드크림"  # 검색하려는 실제 검색어로 대체하세요.

# 상품 정보 조회 API 호출
params_search = {"key": api_key, "apiCode": "ProductSearch", "keyword": search_keyword}

response_search = requests.get(api_url, params=params_search)

# API 응답 확인
if response_search.status_code == 200:
    data_search = response_search.text
    # XML 데이터 파싱
    root = ET.fromstring(data_search)

    # 상품 정보 추출
    product_list = root.findall(".//Product")

    if product_list:
        for product_info in product_list:
            product_name_elem = product_info.find("ProductName")
            product_price_elem = product_info.find(".//ProductPrice")
            product_image_elem = product_info.find(".//ProductImage")

            # 하나 이상의 정보가 있을 때 가져옴
            if product_name_elem is not None:
                product_name = product_name_elem.text
            else:
                product_name = "상품 이름 없음"

            # 가격 정보가 있는 경우 가져오고, 없으면 "상품 가격 없음"으로 표시
            if product_price_elem is not None:
                product_price = product_price_elem.text
            else:
                product_price = "상품 가격 없음"

            if product_image_elem is not None:
                product_image_url = product_image_elem.text
            else:
                product_image_url = "상품 이미지 없음"

            # 상품 이름, 가격, 이미지 URL 출력 또는 다른 작업 수행
            print("상품 이름:", product_name)
            print("상품 가격:", product_price)
            print("이미지 URL:", product_image_url)
            print("\n")
    else:
        print("검색 결과가 없습니다.")
else:
    print("상품 정보 조회 API 호출에 실패했습니다. 상태 코드:", response_search.status_code)
