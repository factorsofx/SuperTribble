from typing import Dict

import numpy as np

# code to make dealing with a system of linear equations easier

class LinRelation(object):
    def __init__(self, relation : Dict[object, float], sum):
        self.sum = sum
        self.relation = relation

class LinEqSys(object):
    def __init__(self):
        self.vars = set()
        self.relations = set()
    
    def solve(self):
        column_order = list(self.vars)
        eqs = []
        sums = []
        
        for relation in self.relations:
            sums.append(relation.sum)
            eq = []
            for key in column_order:
                if key in relation.relation:
                    eq.append(relation.relation[key])
                else:
                    eq.append(0)
            eqs.append(eq)
        
        matrix = np.array(eqs)
        sum_mat = np.array(sums)

        solution_array = np.linalg.lstsq(matrix, sum_mat, rcond=None)

        return {obj:solution_array[0][index] for index, obj in enumerate(column_order)}
    
    def add_relation(self, relation : LinRelation):
        self.relations.add(relation)
        for obj in relation.relation:
            self.vars.add(obj)