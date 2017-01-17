# coding: utf-8

import argparse
from pyparsing import OneOrMore, nestedExpr
from progressbar import ProgressBar, Percentage, Bar
from time import time
from collections import defaultdict
import platform

last_val = -1
checked = False

mark_val = "0.1u"


class KiCAD_PCB:
    def __init__(self, filename):
        self.ast = self._parsePCB(filename)
        mark_comps = self.generate_mark_components_coordinate(self.ast)
        self.mark_pcb(mark_comps, filename)

    def mark_pcb(self, mark_comps, filename):
        coordinates, drawing_num = mark_comps

        with open(filename, 'r') as f:
            data = f.read()

        old_drawings = "(drawings %d)" % (drawing_num)
        now_drawings = "(drawings %d)" % (drawing_num + len(coordinates))
        data = data.replace(old_drawings, now_drawings)
        data = data.replace("\n)", "\n")

        for x,y in coordinates:
            data += "  (gr_circle(center {x} {y}) (end {xx} {y}) (layer F.Fab) (width 0.20066))\n".format(
                x=x, y=y, xx=x+1)
        data += ")"

        writefilename = filename.split(".")[0] + mark_val +".kicad_pcb"
        with open(writefilename, 'w') as wf:
            wf.write(data)

    def generate_mark_components_coordinate(self, ast):
        coordinate = []
        for i in ast[0]:
            token = i[0]
            if token == 'general':  # find drawings
                attr = self.pick(i[1:], 'drawings')
                drawings = int(attr['drawings'][0])
            elif token == 'module':  # a module!
                footprint = i[1]
                lst = i[2:]
                attr = self.pick(lst, 'at', 'fp_text value', 'fp_text reference')
                x, y = float(attr['at'][0]), float(attr['at'][1])
                reference = attr['fp_text reference'][0]
                value = attr['fp_text value'][0]
                package = None
                if reference[0].lower() in ['r', 'l', 'c']:
                    # is resistor, capacitor or inductor
                    if value == mark_val:
                        coordinate.append((float(x), float(y)))

        return coordinate, drawings

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
