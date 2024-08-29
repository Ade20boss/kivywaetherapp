from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
import requests
from bs4 import BeautifulSoup
Window.size = (350, 600)

kv = '''
MDFloatLayout:
    md_bg_color: 1,1,1,1
    Image:
        source: "assets/loaction.png"
        size_hint: .1, .1
        pos_hint: {"center_x": .5, "center_y": .95}
        
    MDLabel:
        id: location
        text:""
        pos_hint: {"center_x": .5, "center_y": .89}
        halign: "center"
        font_size: "20sp"
        font_name: "Poppins"
        
    Image:
        id: weather_image
        source: ""
        pos_hint: {"center_x": .5, "center_y": .77}
        
    
    MDLabel:
        id: temperature
        text:""
        markup: True
        pos_hint: {"center_x": .5, "center_y": .62}
        halign: "center"
        font_size: "60sp"
    
    MDLabel:
        id: weather
        text:""
        pos_hint: {"center_x": .5, "center_y": .54}
        halign: "center"
        font_size: "20sp"
        font_name: "Poppins"
        
        
    MDFloatLayout:
        pos_hint: {"center_x": .25, "center_y": .4}
        size_hint: .22, .1
        
        Image:
            source: "assets/humidity.png"
            pos_hint: {"center_x": .1, "center_y": .5}
            
            
        MDLabel:
            id: humidity 
            text:"80%"
            pos_hint: {"center_x": .9, "center_y": .7}
            font_size: "18sp"
            font_name: "Poppins"
        
        
    
        MDLabel:
            text:"Humidity"
            pos_hint: {"center_x": .8, "center_y": .3}
            halign: "center"
            font_size: "14sp"
            font_name: "Poppins"
            
    MDFloatLayout:
        pos_hint: {"center_x": .7, "center_y": .4}
        size_hint: .22, .1
        
        Image:
            source: "assets/wind.png"
            pos_hint: {"center_x": .1, "center_y": .5}
            
            
        MDLabel:
            id: wind_speed
            text:"80km/h"
            pos_hint: {"center_x": 1.1, "center_y": .7}
            font_size: "16sp"
            font_name: "Poppins"
        
        
    
        MDLabel:
            text:"Wind"
            pos_hint: {"center_x": 1.1, "center_y": .3}
            halign: "center"
            font_size: "14sp"
            font_name: "Poppins"
            
            
            
    MDFloatLayout:
        size_hint_y: .3
        canvas:
            Color:
                rgb: rgba(148, 117, 255, 255)
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [10, 10, 0, 0]
                
        MDFloatLayout:
            pos_hint: {"center_x": .5, "center_y": .71}
            size_hint: .9, .32
            canvas:
                Color:
                    rgb: rgba(131, 69, 255, 255)
                RoundedRectangle:
                    size: self.size
                    pos: self.pos
                    radius: [6]
                
            TextInput:
                id: city_name
                hint_text: "Enter City Name"
                size_hint: 1, None
                pos_hint: {"center_x": .5, "center_y": .5}
                height: self.minimum_height
                multiline: False
                font_name: "assets/Poppins/Poppins-Bold.ttf"
                font_size: "20sp"
                hint_text_color: 1,1,1,1
                foreground_color: 1,1,1,1
                background_color: 1,1,1,0
                padding: 15
                cursor_width: "2sp"
                
                
        Button:
            text: "Get Weather"
            font_size: "20sp"
            font_name: "assets/Poppins/Poppins-Bold.ttf"
            size_hint: .9, .32
            pos_hint: {"center_x": .5, "center_y": .29}
            background_color: 1,1,1,0
            color: rgba(148, 117, 255, 255)
            on_release: app.search_weather() 
            canvas.before:
                Color:
                    rgb: 1,1,1,1
                RoundedRectangle:
                    size:self.size
                    pos: self.pos
                    radius: [6]
        
    
'''


class WeatherApp(MDApp):

    api_key = "1b1808bdd8f04314bc300119242708"


    def on_start(self):
        try:
            soup = BeautifulSoup(requests.get(f"https://www.google.com/search?q=weather+at+my+current+location").text, "html.parser")
            temp = soup.find("span", class_= "BNeawe tAd8D AP7Wnd")
            location = "".join(filter(lambda item:not item.isdigit(), temp.text)).split(",",1)
            self.get_weather(location[0])
        except requests.ConnectionError:
            self.root.ids.location.text = "No internet connection"


    def build(self):
        return Builder.load_string(kv)

    def get_weather(self, city_name):
       try:
           url = f"https://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city_name}"
           response = requests.get(url)
           data = response.json()

           print(data)

           # Check for errors in the response
           if "error" not in data:
               # Extract useful information
               location = data["location"]["name"]
               region = data["location"]["region"]
               country = data["location"]["country"]
               condition_id = data["current"]["condition"]["code"]
               temperature = data["current"]["temp_c"]
               condition = data["current"]["condition"]["text"]
               humidity = data["current"]["humidity"]
               wind_speed = data["current"]["wind_kph"]
               self.root.ids.temperature.text = f"[b]{temperature}°C[/b]"
               self.root.ids.weather.text = str(condition)
               self.root.ids.humidity.text = f"{humidity}%"
               self.root.ids.wind_speed.text = f"{wind_speed}km/h"
               self.root.ids.location.text = location
               if condition_id == 1000:
                   self.root.ids.weather_image.source = "assets/sun.png"

               elif condition_id == 1003:
                   self.root.ids.weather_image.source = "assets/partlycloudy.png"

               elif condition_id == 1006 or condition_id == 1009:
                   self.root.ids.weather_image.source = "assets/cloudy.png"

               elif condition_id in [1030, 1135, 1147]:
                   self.root.ids.weather_image.source = "assets/mist.png"

               elif condition_id in [1150, 1153, 1168, 1171]:
                   self.root.ids.weather_image.source = "assets/drizzle.png"

               elif condition_id in [1063, 1180, 1183, 1186, 1189, 1192, 1195, 1198, 1201, 1240, 1243, 1246]:
                   self.root.ids.weather_image.source = "assets/rain.png"

               elif condition_id in [1069, 1204, 1207, 1249, 1252]:
                   self.root.ids.weather_image.source = "assets/sleet.png"

               elif condition_id in [1066, 1114, 1117, 1210, 1213, 1216, 1219, 1222, 1225, 1237, 1255, 1258]:
                   self.root.ids.weather_image.source = "assets/snow.png"

               elif condition_id in [1087, 1273, 1276, 1279, 1282]:
                   self.root.ids.weather_image.source = "assets/thunderstorm.png"



           else:
               print('City not Found')
       except requests.ConnectionError:
           print("No internet Connection")



    def search_weather(self):
        city_name = self.root.ids.city_name.text
        if city_name != "":
            self.get_weather(city_name)


if __name__ == "__main__":
    LabelBase.register(name="Poppins", fn_regular="assets/Poppins/Poppins-Medium.ttf")
    LabelBase.register(name="Poppins", fn_regular="assets/Poppins/Poppins-Bold.ttf")
    WeatherApp().run()



