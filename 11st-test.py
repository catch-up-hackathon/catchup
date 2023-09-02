import json
import dotenv
import os
import requests
import xml.etree.ElementTree as ET

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def get_product_info():
    # API 엔드포인트 및 키 설정
    api_url = "http://openapi.11st.co.kr/openapi/OpenApiService.tmall"
    api_key = os.getenv("11ST_KEY")
    search_keyword = "핸드크림"

    # 상품 정보를 담을 리스트 초기화
    products = []

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

                # 상품 정보를 딕셔너리 형태로 추가
                product_data = {
                    "상품 이름": product_name,
                    "상품 가격": product_price,
                    "이미지 URL": product_image_url,
                }

                # 상품 정보를 리스트에 추가
                products.append(product_data)

        # JSON 형식으로 결과 리턴
        products_json = json.dumps(products, ensure_ascii=False, indent=4)

        # 결과를 리턴
        return products_json
    else:
        return None


# 함수 호출하여 결과 출력
result = get_product_info()
if result is not None:
    print(result)
else:
    print("상품 정보 조회 API 호출에 실패했습니다.")
