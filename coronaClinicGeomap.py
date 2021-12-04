import folium
import pandas as pd
import webbrowser
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


fontpath = 'C:/Windows/Fonts/malgun.ttf'
font = fm.FontProperties(fname=fontpath, size=9)
plt.rc('font', family='malgun')
# mpl.font_manager._rebuild()

clinicGeoData = pd.read_csv('./resources/clinic_geo.shp.csv',
            encoding='cp949',
            engine='python')

print(clinicGeoData.head())

clinic_map = folium.Map(location=[37.560284, 126.975334], zoom_start= 8)

for (index, row) in clinicGeoData.iterrows():
    iframe = folium.IFrame('<h4>' + '<b>' + row.loc["name"] + '</b>' + '<h4>' + '운영시간(평일): ' + row.loc["Working_Time"] +
                           '<br>' + '운영시간(토): ' + row.loc["WorkingTime_Sat"] + '<br>' + '운영시간(일/공휴일): ' + row.loc["Sunday_holiday"] +
                           '<br>' + '전화번호: ' + row.loc["phone"])

    popup = folium.Popup(iframe, min_width=300, max_width=300)
    folium.Marker(location=[row['위도'], row['경도']],
                                     popup=popup,
                                     icon=folium.Icon(color='green',icon='medkit',prefix="fa")).add_to(clinic_map)


clinic_map.save('C:/chh_scraping/map/clinic_map.html')

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

url = 'C:/chh_scraping/map/clinic_map.html'

webbrowser.get(chrome_path).open(url)