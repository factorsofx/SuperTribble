import numpy as np
import json
import svgwrite

from bridge import TrussBeam, TrussNode
from eqsys import LinEqSys, LinRelation

from math import cos, sin

# load bridge data

with open('bridges/180_bridge.json') as bridge_file:
    bridge_json = json.load(bridge_file)

nodes = []
for index, json_node in enumerate(bridge_json['nodes']):
    nodes.append(TrussNode(json_node[0], json_node[1], index + 1 in bridge_json['anchors']))

beams = []
for index, json_beam in enumerate(bridge_json['beams']):
    beams.append(TrussBeam(nodes[json_beam[0] - 1], nodes[json_beam[1] - 1]))

# generate system of equations for bridge
eqs = []

# for each node, generate an equation for x and y based on the angle of each beam connected
# equation structure: [Beam1, Beam2, Beam3, ..., Load1, Load2, Load3, ..., Anchor1, Anchor2, Anchor3, ...]
# Load forces and anchor forces are only vertical (for now)
columns = beams # + loads + anchors

for node in nodes:
    # generate sum of forces equations for x and y for the node
    x_eq = []
    y_eq = []
    for beam in beams:
        if beam in node.beams:
            angle = beam.get_force_angle_to_node(node)
            x_eq.append(cos(angle))
            y_eq.append(sin(angle))
        else:
            x_eq.append(0)
            y_eq.append(0)
    eqs.append(x_eq)
    eqs.append(y_eq)

for eq in eqs:
    print(eq)

# generate a matrix from the list of equations and solve

mat = np.array(eqs)

print(mat.shape)

result = np.linalg.lstsq(mat, np.array([0] * mat.shape[0]), rcond=None)[0]
print(result)

# get the tension in each beam from the equation and use it as the color when generating a diagram

drawing = svgwrite.Drawing(filename='bridge.svg', profile='tiny', viewBox="-10 -110 120 120")

for beam in beams:
    start = (beam.node1.x * 10, -beam.node1.y * 10)
    end   = (beam.node2.x * 10, -beam.node2.y * 10)

    drawing.add(drawing.line(start=start, end=end, stroke='green'))

for node in nodes:
    drawing.add(drawing.circle((node.x * 10, -node.y * 10), r=2, fill='red' if node.anchor else 'black'))


drawing.save()