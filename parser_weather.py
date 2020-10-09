import requests
import lxml
from bs4 import BeautifulSoup
import emoji as em


def get_page_soup(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def get_weather_for_today(soup):
    max_temp = soup.find('div', class_='max').find('span').text
    min_temp = soup.find('div', class_='min').find('span').text
    description = soup.find('div', class_='description').text.strip()

    return em.emojize(f':sun_with_face: мин.{min_temp}С, макс.{max_temp}С\n{description}')


def get_weather_for_tomorrow(soup):
    max_temp = soup.find('div', class_='main', id='bd2').find('div', class_='max').find('span').text
    min_temp = soup.find('div', class_='main', id='bd2').find('div', class_='min').find('span').text

    return em.emojize(f':sun_with_face: мин.{min_temp}С, макс.{max_temp}С ')


def get_weather_7_days(soup):
    weather_info = []
    for i in range(1, 8):
        weather = soup.find('div', class_='main', id='bd'+str(i))
        day = weather.find('p', class_='date').text
        month = weather.find('p', class_='month').text
        max_temp = weather.find('div', class_='max').find('span').text
        min_temp = weather.find('div', class_='min').find('span').text
        weather_info.append(f'Погода на {day} {month}: мин. {min_temp}С, макс. {max_temp}С ')
    return weather_info


def get_sunrise_set(soup):
    time_ = []
    sunrise_set = soup.find('div', class_='infoDaylight').find_all('span')
    for i in range(2):
        time_.append(sunrise_set[i].text)

    return em.emojize(f' :sunrise: Время восхода: {time_[0]} \n :sunrise_over_mountains: Время заката: {time_[1]} ')

