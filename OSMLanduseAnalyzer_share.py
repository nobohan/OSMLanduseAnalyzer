### SHARE of landuse

## Select the layers by name
landuse = QgsProject.instance().mapLayersByName("osm_landusages_march18")[0]

area_total = 0
area_forest = 0
area_meadow = 0
area_residential = 0

area_farm = 0
area_farmland = 0
area_farmyard = 0
area_orchard = 0

area_forest_bl = 0
area_forest_nl = 0
area_forest_ml = 0
area_forest_dec = 0
area_forest_eve = 0
area_forest_mc = 0
area_forest_no_type = 0

area_urban = 0
area_water = 0
area_industrial = 0

# value taken from the coverage layer, ie, the fully dissolved layer (m2)
area_coverage = 24425865669.5

for f in landuse.getFeatures():
  # sum all areas
  area_total = area_total + f['area']
  # sum areas by type
  if f['type'] == "forest" or f['type'] == "wood":
     area_forest = area_forest + f['area']
     # type of forest
     if f['leaf_type'] == "broadleaved":
         area_forest_bl = area_forest_bl + f['area']
     if f['leaf_type'] == "needleleaved":
         area_forest_nl = area_forest_nl + f['area']
     if f['leaf_type'] == "mixed":
         area_forest_ml = area_forest_ml + f['area']
     if f['leaf_cycle'] == "deciduous":
         area_forest_dec = area_forest_dec + f['area']
     if f['leaf_cycle'] == "evergreen":
         area_forest_eve = area_forest_eve + f['area']
     if f['leaf_cycle'] == "mixed":
         area_forest_mc = area_forest_mc + f['area']
     if f['leaf_type'] == NULL and f['leaf_cycle'] == NULL:
         area_forest_no_type = area_forest_no_type + f['area']
  # Agri areas
  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']
  if f['type'] == "farm":
     area_farm = area_farm + f['area']
  if f['type'] == "farmland":
     area_farmland = area_farmland + f['area']
  if f['type'] == "orchard":
     area_orchard = area_orchard + f['area']
  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']

  # Urban areas
  if f['type'] == "residential" or f['type'] == "farmyard" or f['type'] == "cemetery"  or f['type'] == "college" or f['type'] == "commercial" or f['type'] == "fuel"  or f['type'] == "garden" or f['type'] == "hospital"  or f['type'] == "library"  or f['type'] == "parking"  or f['type'] == "park"  or f['type'] == "pedestrian"  or f['type'] == "pitch"  or f['type'] == "place_of_worship"  or f['type'] == "playground"  or f['type'] == "school"  or f['type'] == "scrub"  or f['type'] == "sports_centre"  or f['type'] == "stadium"  or f['type'] == "theatre"  or f['type'] == "university"  or f['type'] == "recreation_ground"  or f['type'] == "retail"  or f['type'] == "zoo":
      area_urban = area_urban + f['area']

  if f['type'] == "industrial":
      area_industrial = area_industrial + f['area']

  # Water areas
  if f['type'] == "water" or f['type'] == "riverbank" or f['type'] == "basin"  or f['type'] == "reservoir":
     area_water = area_water + f['area']

# Sum of area for agricultural types
area_agricultural = area_farm + area_farmland + area_orchard + area_meadow


# Landuse share results
print('agri : ' + str(area_agricultural/area_coverage))
print('forest : ' + str(area_forest/area_coverage))
print('urban : ' + str(area_urban/area_coverage))
print('industrial: ' + str(area_industrial/area_coverage))
print('water : ' + str(area_water/area_coverage))

# Type of forest
print('broadleaved : ' + str(area_forest_bl/area_forest))
print('needleleaved : ' + str(area_forest_nl/area_forest))
print('mixedleaved : ' + str(area_forest_ml/area_forest))
print('deciduous : ' + str(area_forest_dec/area_forest))
print('evergreen : ' + str(area_forest_eve/area_forest))
print('mixedcycle : ' + str(area_forest_mc/area_forest))
print('no_forest_type :' + str(area_forest_no_type/area_forest))

# Type of agricultural land
print('farm : ' + str(area_farm/area_agricultural))
print('farmland : ' + str(area_farmland/area_agricultural))
print('meadow : ' + str(area_meadow/area_agricultural))
print('orchard : ' + str(area_orchard/area_agricultural))
