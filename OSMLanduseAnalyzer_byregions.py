### Landuse coverage

# work in progress! 

## Select the layers by name
osm_landusages_inter_BEregion = QgsMapLayerRegistry.instance().mapLayersByName("osm_landusages_inter_BEregion")[0]

### Belgium area
area_BE = 30528000000
### Area of the 3 regions according to the layer
area_VLG = 1358387600
area_BRU = 162094275
area_WAL = 1686091540
area_BE = area_VLG + area_BRU + area_WAL
#NB: why the sum of the 3 regions is 3206573415?

area_lu_VLG = 0
area_lu_BRU = 0
area_lu_WAL = 0

# 1) Landuse coverage
for f in osm_landusages_inter_BEregion.getFeatures():
    # still TODO: avoid overlapping landuse polygon
    if f['ISO3166-2'] == 'BE-VLG':
        area_lu_VLG = area_lu_VLG + f['area']
    if f['ISO3166-2'] == 'BE-BRU':
        area_lu_BRU = area_lu_BRU + f['area']
    if f['ISO3166-2'] == 'BE-WAL':
        area_lu_WAL = area_lu_WAL + f['area']

area_lu_BE = area_lu_VLG + area_lu_BRU + area_lu_WAL

### results
print "Country coverage: " + str(area_lu_BE/area_BE*100) + " %"
print "VL coverage: " + str(area_lu_VLG/area_VLG*100) + " %"
print "BXL coverage: " + str(area_lu_BRU/area_BRU*100) + " %"
print "WAL coverage: " + str(area_lu_WAL/area_WAL*100) + " %"


### results are (without accounting for self-intersection + recompute areas!):
# Country coverage: 842.37795119 %
# VL coverage: 970.947602699 %
# BXL coverage: 125.099081888 %
# WAL coverage: 807.753127645 %

# TODO: simply dissolve the layer entirely and compute the area by region!
# 1) dissolve landusages (dissolve all)
# 2) intersect landusages_dissolved by regions & provinces
# 3) recompute area
# 4) compute coverage
