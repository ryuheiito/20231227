import folium
from folium import FeatureGroup, LayerControl
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd


# CSVファイルのパス
csv_path = 'input/input.csv'

# CSVファイルの読み込み
data = pd.read_csv(csv_path,encoding="cp932")


# 地図の初期設定
# 日本を中心とした地図の初期設定（緯度約36.5度、経度約138度）
map = folium.Map(location=[36.5, 138], zoom_start=6)




# ポップアップのスタイルを定義するCSS
popup_css_style = """
<style>
    .popup-info-container {
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        color: #333333;
        background-color: #f9f9f9;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.2);
        max-width: 300px;
    }
    .popup-info-header {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .popup-info-row {
        margin-bottom: 3px;
    }
</style>
"""


# CSVデータの行数分ループ
for index, row in data.iterrows():
    # 緯度経度の取得
    lat = row[0]
    lng = row[1]
    
     # Google Mapsへのリンクを作成
    google_maps_link = f"<a href='https://www.google.com/maps?q={lat},{lng}' target='_blank'>Google Mapsで開く</a>"

    # その他情報の取得
    info = "<div style='font-size: 14px; font-family: Arial, sans-serif;'>"
    for column in data.columns[2:]:
        info += f"<b>{column}:</b> {row[column]}<br>"
    info += google_maps_link + "</div>"
    
    # マーカーの作成
    marker = folium.Marker(
        location=[lat, lng],
        popup=folium.Popup(info, max_width=300, min_width=200),  # マーカーをクリックしたときに表示する情報を設定
        )

    # マーカーを地図に追加
    marker.add_to(map)


# ヒートマップレイヤー
heat_data = [[row[0], row[1]] for index, row in data.iterrows()]
heatmap_group = FeatureGroup(name='ヒートマップ', show=False)
HeatMap(heat_data).add_to(heatmap_group)
map.add_child(heatmap_group)

folium.raster_layers.TileLayer(
    tiles = 'https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg',
    fmt = 'image/png',
    attr = '&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html">国土地理院</a>',
    name = '国土地理院地図_全国最新写真（シームレス）'
).add_to(map)

folium.raster_layers.TileLayer(
    tiles = 'https://cyberjapandata.gsi.go.jp/xyz/relief/{z}/{x}/{y}.png',
    fmt = 'image/png',
    attr = '&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html">国土地理院</a>',
    name = '国土地理院地図_色別標高図'
).add_to(map)

# レイヤーコントロールの追加
LayerControl().add_to(map)

# 地図をHTMLファイルとして保存
map.save('output/map.html')
