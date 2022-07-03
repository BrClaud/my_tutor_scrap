from bs4 import BeautifulSoup
import requests
import json
import csv

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
#
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.58"
}
# req = requests.get(url,headers=  headers)
# src = req.text
# print(src)
#
# with open('index.html',"w",encoding='utf-8') as file:
#     file.write(src)

# with open('index.html',encoding='utf-8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src,'lxml')
#
#
# all_product = soup.find_all(class_="mzr-tc-group-item-href")
#
# all_categories_dict = {}
# for i in all_product:
#     item_text = i.text
#     item_href = 'https://health-diet.ru'+i.get('href')
#
#     all_categories_dict[item_text] = item_href
#
# with open('all_categories_dict.json','w') as file:
#     json.dump(all_categories_dict,file,indent=4,ensure_ascii=False)

with open('all_categories_dict.json') as file:
    all_categories = json.load(file)

iteration_cnt = len(all_categories) - 1
print(f"всего итераций {iteration_cnt}")
count = 0
for category_name, category_href in all_categories.items():


    rep = [' ', '.', ',', '-', "'"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, '_')
    # print(category_name)
    req = requests.get(url=category_href,headers= headers)
    src= req.text

    with open(f"data/{count}_{category_name}.html","w",encoding='utf-8')as file:
        file.write(src)

    with open(f"data/{count}_{category_name}.html", encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    alert_ = soup.find(class_="uk-alert-danger")
    if alert_ is not None:
        continue

    header = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    print(header)
    product = header[0].text
    calories = header[1].text
    proteins = header[2].text
    farts = header[3].text
    carbohydrates = header[4].text

    with open(f"data/{count}_{category_name}.csv", 'w', encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                farts,
                carbohydrates
            )
        )


    all_product = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_info = []

    for i in all_product:
        prod_td = i.find_all('td')
        title = prod_td[0].find('a').text
        calories = prod_td[1].text
        proteins = prod_td[2].text
        farts = prod_td[3].text
        carbohydrates = prod_td[4].text

        product_info.append(
            {
                "Title":title,
                "Calories": calories,
                "proteins" : proteins,
                "fats" : farts,
                "carbohydrates": carbohydrates
            }
        )
        with open(f"data/{count}_{category_name}.csv", 'a', encoding="utf-8-sig", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    farts,
                    carbohydrates
                )
            )

    with open(f"data/{count}_{category_name}.json","a",encoding="utf-8")as file:
        json.dump(product_info,file,indent=4,ensure_ascii=False)



    count += 1
    print(f"итерация {count}. {category_name} записан.")
    iteration_cnt -= 1
    print(f"итераций осталось {iteration_cnt}")
