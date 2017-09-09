
# 1) Landuse coverage

# 2) Landuse share

# Select the landuse layer in QGIS toc and then run:
layer = iface.activeLayer()

tot_area = 0
area_forest = 0
area_meadow = 0
area_residential = 0
area_farmland = 0

for f in layer.getFeatures():
  # sum all areas
  tot_area = tot_area + f['area']
  # sum forested areas
  if f['type'] == "forest":
     area_forest = area_forest + f['area']
  if f['type'] == "meadow":
     area_meadow = area_meadow + f['area']
  if f['type'] == "residential":
     area_residential = area_residential + f['area']
  if f['type'] == "farmland":
     area_farmland = area_farmland + f['area']

print area_forest/tot_area
print area_meadow/tot_area
print area_residential/tot_area
print area_farmland/tot_area
