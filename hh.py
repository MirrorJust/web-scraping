import requests
from bs4 import*
import json
import pandas as pd
a = 'разработчик'
page = 0
par = {'text': a, 'page': page}
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
r = requests.get('https://kazan.hh.ru/search/vacancy?L_is_autosearch=false&area=88&clusters=true&enable_snippets=true', headers = head, params = par)

r.encoding = 'utf-8'
t = r.text

soup = BeautifulSoup(t, 'html.parser')
total_vac = soup.find('h1')

vac_list = []
a = 0
for each_div in soup.find_all(class_ = 'vacancy-serp-item'):
    vac_list.append(each_div)
    a += 1

all_vac_page = []
for i in range(len(vac_list)):
    # Получаем название одной вакансии
    soup_1 = BeautifulSoup(str(vac_list[i]))
    name_vac = soup_1.find(class_ = 'bloko-link HH-LinkModifier').text
    
    # Получаем указанную зарплату, если не указана пишем «Не указана»
    salary = soup_1.find(class_ = 'vacancy-serp-item__sidebar').text.replace(u'\xa0', '')
    
    #Получаем параметры скрипта, который содержит id вакансии и работодателя
    l_par = soup_1.find_all('script')
    l_par_need = {}
    # Получаем атрибуты скриптов вакансии
    list_script = []
    for i in l_par:
        list_script.append(i.attrs)
    # Проверяем содержит ли элемент списка с атрибутами, значение data-name = "HH/VacancyResponsePopup/VacancyResponsePopup"
    for j in range(len(list_script)):
        for key,value in list_script[j].items():
            if key == 'data-name' and value == 'HH/VacancyResponsePopup/VacancyResponsePopup':
                dict_need_script = list_script[j]

    #Читаем json файл с ключем параметров и разделяем все параметры запятыми
    y = json.dumps(dict_need_script['data-params']).split(',')

    #Вытягиваем int из нужных вакансий + преобразуем в строку
    for i in range(len(y)):
            if len(y[i]):

                if i == 2:
                    a = []
                    for j in y[i]:
                        if j == '0' or j == '1' or j == '2' or j == '3' or j == '4' or j == '5' or j == '6' or j == '7' or j == '8' or j == '9':
                            a += j
                    a_1 = ''.join(a) 
                elif i == 3:
                    b = []
                    for j in y[i]:
                        if j == '0' or j == '1' or j == '2' or j == '3' or j == '4' or j == '5' or j == '6' or j == '7' or j == '8' or j == '9':
                            b += j
                    b_1 = ''.join(b)

    #Записываем все полученные значения в один массив        
    all_vac_page.append([name_vac, a_1, b_1, salary])
    
list_pandas_vacancy = []
for i in range(len(all_vac_page)):
    dict = {}
    for j in range(len(all_vac_page[i])): 
        dict['Название вакансии'] = all_vac_page[i][0]
        dict['Id вакансии'] = all_vac_page[i][1]
        dict['Id работодателя'] = all_vac_page[i][2]
        dict['Зарплата'] = all_vac_page[i][3]
        if all_vac_page[i][3] == '':
            all_vac_page[i][3] = 'Не указана'
    list_pandas_vacancy.append(dict)

pd.DataFrame(list_pandas_vacancy)