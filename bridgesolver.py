import numpy
import json
import svgwrite

# load bridge data

with open('bridges/180_bridge.json') as bridge_file:
    bridge_json = json.load(bridge_file)



# generate system of equations for bridge

# solve system of equations for bridge

# generate diagram of bridge

drawing = svgwrite.Drawing(filename='bridge.svg', profile='tiny', viewBox="0 -100 100 100")

for beam in bridge_json['beams']:
    start = (bridge_json['nodes'][beam[0]-1][0] * 10, -bridge_json['nodes'][beam[0]-1][1] * 10)
    end   = (bridge_json['nodes'][beam[1]-1][0] * 10, -bridge_json['nodes'][beam[1]-1][1] * 10)

    drawing.add(drawing.line(start=start, end=end, stroke='green'))

for node in bridge_json['nodes']:
    drawing.add(drawing.circle((node[0] * 10, -node[1] * 10), r=2))


drawing.save()