import dotenv
import os
import openai

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

openai.api_key = os.getenv("OPENAI_API_KEY")
file_name = "w74dvSGcZoM"

with open(f"extractscript/script/{file_name}.txt", "r") as file:
    context = file.read().replace("\n", "")

condition = "diabetes with chicken allergy"

prompt = f"""
First of all, correct the words in context if the spell is incorrect. For example, there isn't '모기버섯', '목이버섯' is correct.
And arrange the list of recipe from following {context}, replace the ingredients and revise the recipe with good taste according to my condition: {condition}.
In addition, I'd like that the food made by revised recipe tastes good.
Answer in Korean. Please give bad and new ingredients separately for me in some health condition in the form of lists.
If the spelling is incorrect in Korean, revise them to correct words. For example, '모기버섯' to '목이버섯'.
And do not use the word '대체' or '대체재,' just give me detailed ingredients I can search with the ingredient's name. For example, '설탕 대체재' to '스테비아'.
Give me the recipe with the weight of the ingredients to weigh easily for home cook.
context: {context}
Give me output which is as following format with JSON and not with any descriptions.
And finish the recipe with a word of advice.
Example Answer for diabetes:
answer= {{
  "recipe_name": "당뇨 환자를 위한 요리법"
  "bad": ["설탕", "등심", "전분", "달걀 흰자", "간장"],
  "good": ["스테비아", "닭 가슴살", "콩가루", "달걀 흰자 대체재(아쿠아파바)", "간장 대체재(코코아미노)"],
  "ingredients": [
    {{"name": "닭 가슴살", "amount": "150g"}},
    {{"name": "당근", "amount": "1/2개"}},
    {{"name": "오이", "amount": "1/2개"}},
    {{"name": "목이버섯", "amount": "50g"}},
    {{"name": "파인애플", "amount": "1/4개"}},
    {{"name": "스테비아", "amount": "5큰술"}},
    {{"name": "식초", "amount": "4큰술"}},
    {{"name": "코코아미노", "amount": "2큰술"}},
    {{"name": "콩가루", "amount": "1/2컵"}},
    {{"name": "아쿠아파바", "amount": "1개"}},
    {{"name": "물", "amount": "1컵 + 3분의 1컵"}}
  ],
  "recipe": [
    "1. 닭 가슴살을 편으로 썰어줍니다.",
    "2. 당근, 오이, 목이버섯, 파인애플을 적당한 크기로 썰어줍니다.",
    "3. 콩가루와 아쿠아파바를 섞어 튀김옷을 만듭니다.",
    "4. 닭 가슴살을 튀김옷에 묻혀 170-180도의 기름에서 5-6분 동안 튀깁니다.",
    "5. 물 1컵에 스테비아, 식초, 코코아미노를 넣고 섞어 소스를 만듭니다.",
    "6. 소스가 끓기 시작하면 콩가루와 물을 섞어 물전분을 만들고 소스에 부어줍니다.",
    "7. 튀긴 닭 가슴살을 소스에 묻히고 잘 섞어줍니다.",
    "8. 접시에 담아 완성합니다."
  ],
  "advice":"이 레시피는 건강을 위해 보조적으로 활용될 뿐이며, 특정 질환의 치료를 위해서는 가까운 병원을 찾아주시기 바랍니다."
}}
"""


completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system",
            "content": "You are a cooking expert bot who can revise recipes according to individual health status.",
        },
        {"role": "user", "content": prompt},
    ],
    temperature=0.7,
)

print(completion.choices[0].message["content"])
