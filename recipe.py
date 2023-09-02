import dotenv
import os
import openai

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

openai.api_key = os.getenv("OPENAI_API_KEY")
file_name = "w74dvSGcZoM"

with open(f"extractscript/script/{file_name}.txt", "r") as file:
    context = file.read().replace("\n", "")

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a cooking expert bot who can revise recipes according to individual health status.",
        },
        {
            "role": "user",
            "content": f"Arrange the list of recipe from following context, replace the ingredients and revise the recipe for good taste. \
         Because I have a diabetes, I need the recipe for my health not to increase sugars in blood. In addition, I'd like that the food made by revised recipe tastes good.\
         Answer in korean. Please give bad ingredients and new ingredients for someone with diabetes seperately in form of list like \
         bad = ['bad1', 'bad2', 'bad3',...'badN'], good = ['good1', 'good2',...'goodN']\
         If the spell is incorrect in korean, revise them correct words. For example, '모기버섯' to '목이버섯'.\
         And not use '대체' or 대체재, just give me detail ingredient I can search and put it in my cart directly with the ingredient's name. For example, '설탕 대체재' to '스테비아'\
         context: {context}\
         answer: {'bad': [], 'good': [], 'ingredients': [], 'recipe': []}",
        },
    ],
    temperature=0,
)

print(completion.choices[0].message["content"])
