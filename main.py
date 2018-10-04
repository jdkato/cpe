import folium

# NOTE: Ran into 'Python not installed as a framework' issues.
#
# https://github.com/JuliaPy/PyCall.jl/issues/218#issuecomment-267558858
import matplotlib.pyplot as plt
import geopandas as gpd

shape = gpd.read_file('data/Dept_23-00089/23-00089_Shapefiles/Indianapolis_Police_Zones.shp')

mapa = folium.Map([39.81, -86.26060805912148], height=400, zoom_start=10)
folium.GeoJson(shape).add_to(mapa)

mapa.save('vis.html')
