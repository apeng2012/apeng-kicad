# coding: utf-8

import argparse
from pyparsing import OneOrMore, nestedExpr
from progressbar import ProgressBar, Percentage, Bar
from time import time
import sys
from collections import defaultdict
import platform

last_val = -1
checked = False


class KiCAD_PCB:
    def __init__(self, filename):
        self.ast = self._parsePCB(filename)
        coordinate, bom = self.generate_coordinate_and_bom(self.ast)
        self.write_bom(bom, "SMT_BOM.csv")
        self.write_coordinate(coordinate, "SMT_Coordinate.csv")

    def write_bom(self, bom, filename):
        with open(filename, 'w') as f:
            f.write("Comment,Designator,Footprint,Quantity\n")
            for key, value in bom.iteritems():
                val, package = key
                refs = [x[0] for x in value]
                f.write('{},"{}",{},{}\n'.format(val, ','.join(refs), package.split(':')[-1], len(value)))

    def write_coordinate(self, coordinate, filename):
        with open(filename, 'w') as f:
            f.write("Designator,Mid X, Mid Y,Layer,Rotation\n")
            f.write("\n".join(coordinate))

    def generate_coordinate_and_bom(self, ast):
        coordinate = []
        bom = defaultdict(list)
        for i in ast[0]:
            token = i[0]
            if token == 'setup':  # find grid_origin
                attr = self.pick(i[1:], 'grid_origin')
                origin_x = float(attr['grid_origin'][0])
                origin_y = float(attr['grid_origin'][1])
            elif token == 'module':  # a module!
                footprint = i[1]
                lst = i[2:]
                attr = self.pick(lst, 'layer', 'at',
                                 'fp_text value', 'fp_text reference')
                layer = attr['layer'][0]
                x, y = float(attr['at'][0]), float(attr['at'][1])
                r = float(attr['at'][2]) if len(attr['at']) > 2 else 0
                reference = attr['fp_text reference'][0]
                value = attr['fp_text value'][0]

                if 'P' in reference or 'W' in reference: # 'TP' 'P' 'W'
                    continue

                coordinate.append("{ref},{x}mil,{y}mil,{layer},{rotation}".format(
                    ref=reference,
                    x= (float(x) - origin_x)/0.0254,
                    y= (origin_y - float(y))/0.0254,
                    layer='T' if layer[0] == 'F' else 'B',
                    rotation=r))
                bom[(value, footprint)].append((reference, 2))

        return coordinate, bom

    def pick(self, lst, *attribute_names):
        attr_pool = defaultdict(list)
        for i in attribute_names:
            values = i.split()
            attr_pool[values[0]].append(values)
        obj = {}
        for item in lst:
            if item[0] in attr_pool:
                token_len = len(attr_pool[item[0]][0])
                if token_len == 1:  # simple case, direct match
                    obj[item[0]] = item[1:]
                else:  # complex, try matching tail tokens
                    for tokens in attr_pool[item[0]]:
                        if item[:len(tokens)] == tokens:  # match
                            obj[' '.join(tokens)] = item[len(tokens):]
                            break

        return obj
        
    def _parsePCB(self, filename):
        with open(filename) as f:
            data = f.read()

        start_time = time()
        total_len = len(data)
        bar = ProgressBar(widgets=['Parsing...', Percentage(), ' ', Bar('=', '|')], maxval=100).start()

        def cb(locn, tokens):
            global last_val, checked
            val = locn * 100 / total_len
            if last_val != val:
                cur_time = time()
                if not checked and cur_time - start_time > 3:  # takes too long, check if pypy enabled
                    if not platform.python_implementation().startswith('PyPy'):
                        print "Parsing too slow? Consider using PyPy to accelerate the progress."
                    checked = True
                bar.update(locn * 100 / total_len)
                last_val = val
        ast = OneOrMore(nestedExpr().setParseAction(cb)).parseString(data, parseAll=True)
        bar.finish()

        return ast


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='KiCAD pcb filename')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = init_argparse()

    filename = KiCAD_PCB(args.filename)
