from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty
from kivy.core.image import Image
from bs4 import BeautifulSoup
import requests


class HomeScreen(Screen):
    
    weather = StringProperty()
    description = StringProperty()
    location = StringProperty()
    humidity = StringProperty()
    pressure = StringProperty()
    visibility = StringProperty()
    
    def search(self):
        try:
            country_name = self.ids.country_name.text
            city_name = self.ids.city_name.text
            
            country_name = country_name.replace(' ', '')
            city_name = city_name.replace(' ', '')
            
            url = f'https://www.timeanddate.com/weather/{country_name}/{city_name}'

            response = requests.get(url=url)
            # print(response.status_code)
            
            
            soup = BeautifulSoup(response.text, 'html.parser')
            id_qlook = soup.find(id='qlook')
            class_table = soup.find(class_='table')
            
            
            self.weather = id_qlook.find(class_='h2').get_text()
            self.description = id_qlook.find('p').get_text()
            
            self.location = class_table.find('tbody').find_all('tr')[0].get_text().replace('Location: ', '')
            self.visibility = class_table.find('tbody').find_all('tr')[3].get_text().replace('Visibility: ', '')
            self.pressure = class_table.find('tbody').find_all('tr')[4].get_text().replace('Pressure: ', '')
            self.humidity = class_table.find('tbody').find_all('tr')[5].get_text().replace('Humidity: ', '')
        except (IndexError, AttributeError): # multiple exceptions
            self.ids.country_name.hint_text = 'invalid country name'
            self.ids.city_name.hint_text = 'invalid city name'
        else:
            self.ids.country_name.hint_text = 'country name'
            self.ids.city_name.hint_text = 'city name'


class WeatherApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        Window.size = (400, 700)

        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.primary_hue = '500'
        self.theme_cls.theme_style = 'Light'


WeatherApp().run()