import gdstk
import json
import sys
import numpy
import os

with open(sys.argv[1], 'r') as json_file:
	data = json.load(json_file)


lib = gdstk.Library()	
cell_list = []
instance = {}

for cells in data:
	cell_ref = gdstk.Cell(cells['cellname'])
	lib.add(cell_ref)
	
	cell_list.append(cells['cellname'])
	instance[cell_ref] = []
	
	for props in cells['properties']:
		if props['type'] == 'Rectangle':
			cell_ref.add(gdstk.Polygon(tuple(props['coordinates']), layer=int(props['layer']), datatype=int(props['datatype'])))
			
		elif props['type'] == 'Text':
			if props['rotation'] == None:
				props['rotation'] = 0
			cell_ref.add(gdstk.Label(props['text'], origin=tuple(props['coordinates'][0]), rotation=props['rotation']*(numpy.pi/180), layer=int(props['layer']), texttype=int(props['datatype'])))
			
		elif props['type'] == 'Instance':
			if props['text'] in cell_list:
				if props['rotation'] == None:
					props['rotation'] = 0
				cell_ref.add(gdstk.Reference(props['text'], origin=tuple(props['origin'][0]), rotation=props['rotation']*(numpy.pi/180), x_reflection=props['mirror_x']))
				
			else:
				instance[cell_ref].append(props)
	
for cell_ref, prop_list in instance.items():
	for props in prop_list:
		if props['rotation'] == None:
			props['rotation'] = 0
		cell_ref.add(gdstk.Reference(props['text'], origin=tuple(props['origin'][0]), rotation=props['rotation']*(numpy.pi/180), x_reflection=props['mirror_x']))	

lib.write_gds(os.path.splitext(sys.argv[1])[0]+".gds")
