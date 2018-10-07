import geopandas
import pandas

from util import data_for_dept, plot_dist_composition


dist_data = data_for_dept("Dept_37-00049", "**/*EPIC.shp")[0]
tract_data = data_for_dept("Dept_37-00049", "**/*_500k.shp")[0]

plot_dist_composition(dist_data, tract_data, 0)
