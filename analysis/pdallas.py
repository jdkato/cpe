import folium
import geopandas

from shapely.geometry import shape
# NOTE: We have to import fiona *after* shapely or else we ran into
# an assertion error (see link below).
#
# https://github.com/Toblerity/Shapely/issues/553#issue-285332416
import fiona

from util import data_for_dept

# Test 1
dist_data = data_for_dept("Dept_37-00049", "**/*EPIC.shp")[0]
tract_data = data_for_dept("Dept_37-00049", "**/*_500k.shp")[0]

districts = geopandas.read_file(str(dist_data))
tracts = geopandas.read_file(str(tract_data))

districts = districts.to_crs(epsg=4269)


d1 = list(districts.iterrows())[0]

data = []
for idx, tract in tracts.iterrows():
    if tract['geometry'].intersects(d1[1]["geometry"]):
        area = tract['geometry'].intersection(d1[1]["geometry"]).area
        t_id = tract["GEOID"]

        fract = (area / tract['geometry'].area) * 100
        print("D1 has {0}%% of census tract {1}".format(fract, t_id))

'''
plot = folium.Map([32.7766642, -96.7969879], height=400, zoom_start=10)
for x in districts:
    folium.GeoJson(x).add_to(plot)
plot.save('vis.html')
'''

'''
import folium

from shapely.geometry import shape
# NOTE: We have to import fiona *after* shapely or else we ran into
# an assertion error (see link below).
#
# https://github.com/Toblerity/Shapely/issues/553#issue-285332416
import fiona

from util import data_for_dept

# Test 1
dist_data = data_for_dept("Dept_23-00089", "**/*_Zones.shp")[0]
tract_data = data_for_dept("Dept_23-00089", "**/*_500k.shp")[0]

districts = fiona.open(str(dist_data))
tracts = fiona.open(str(tract_data))

print(districts.crs, tracts.crs)


d1 = shape(districts[0]["geometry"])
# geom_p1 = [ shape(feat["geometry"]) for feat in list(d1) ]
geom_p8 = [ shape(feat["geometry"]) for feat in tracts ]

for j, g8 in enumerate(geom_p8):
    if g8.intersects(d1):
        tract = tracts[j]["properties"]["GEOID"]
        fract = round((g8.intersection(d1).area / g8.area) * 100, 3)
        print("D1 has {0}%% of census tract {1}".format(fract, tract))

plot = folium.Map([39.81, -86.26060805912148], height=400, zoom_start=10)
folium.GeoJson(d1).add_to(plot)
plot.save('vis.html')
'''
