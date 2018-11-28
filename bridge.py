from math import atan2

class TrussNode(object):
    def __init__(self, x, y, anchor):
        self.x = x
        self.y = y
        self.anchor = anchor
        self.beams = set()
    
    def __str__(self):
        return "TrussNode({}, {}, {})".format(self.x, self.y, self.anchor)

class TrussBeam(object):
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.tension = 0

        node1.beams.add(self)
        node2.beams.add(self)
    
    def get_force_angle_to_node(self, node):
        if node == self.node1:
            other_node = self.node2
        else:
            other_node = self.node1
        
        return atan2(other_node.x - node.x, other_node.y - node.y)
