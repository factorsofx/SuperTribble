import numpy as np
import json
import svgwrite

from bridge import TrussBeam, TrussNode
from eqsys import LinEqSys, LinRelation

from math import cos, sin
from random import random

# load bridge data

with open('bridges/simple_bridge.json') as bridge_file:
    bridge_json = json.load(bridge_file)

nodes = []
for index, json_node in enumerate(bridge_json['nodes']):
    nodes.append(TrussNode(json_node[0], json_node[1], index + 1 in bridge_json['anchors']))

beams = []
for index, json_beam in enumerate(bridge_json['beams']):
    beams.append(TrussBeam(nodes[json_beam[0] - 1], nodes[json_beam[1] - 1], 1))

# generate system of equations for bridge
sys = LinEqSys()

for node in nodes:
    # generate sum of forces relations for x and y for the node
    x_relation = {}
    y_relation = {}
    load_relation = {}
    load_obj = "node load {}".format(random())
    load_magnitude = 0

    for beam in node.beams:
        angle = beam.get_force_angle_to_node(node)
        x_relation[beam] = cos(angle)
        y_relation[beam] = sin(angle)
        load_magnitude += beam.weight / 2

    if node.anchor:
        anchor_obj = "anchor {}".format(random())
        y_relation[anchor_obj] = 1

    y_relation[load_obj] = -1
    load_relation[load_obj] = 1
    sys.add_relation(LinRelation(load_relation, load_magnitude))

    sys.add_relation(LinRelation(x_relation, 0))
    sys.add_relation(LinRelation(y_relation, 0))

solution = sys.solve()
print(solution)
for beam in beams:
    beam.tension = solution[beam]

# get the tension in each beam from the equation and use it as the color when generating a diagram

drawing = svgwrite.Drawing(filename='bridge.svg', profile='tiny', viewBox="-10 -110 120 120")

for beam in beams:
    start = (beam.node1.x * 10, -beam.node1.y * 10)
    end   = (beam.node2.x * 10, -beam.node2.y * 10)

    r = 128 - beam.tension * 2
    g = 128 - abs(beam.tension) * 2
    b = 128 + beam.tension * 2

    drawing.add(drawing.line(start=start, end=end, stroke=svgwrite.rgb(r, g, b)))

for node in nodes:
    drawing.add(drawing.circle((node.x * 10, -node.y * 10), r=2, fill='red' if node.anchor else 'black'))


drawing.save()