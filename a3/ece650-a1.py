#!/usr/bin/env python3
import re
import sys


# YOUR CODE GOES HERE

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return '(' + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))


def pp(x):
    if isinstance(x, float):
        if x.is_integer():
            return "{0:.2f}".format(x)
        else:
            return "{0:.2f}".format(x)
    return "{0:.2f}".format(x)


class Line(object):
    """A line between two points"""

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __repr__(self):
        return '[' + pp(self.src) + '-->' + pp(self.dst) + ']'

def isIntersected(l1, l2):
    start = l1.src
    end = l1.dst
    if float(start.x) > float(end.x):
        temp = end
        end = start
        start = temp
    if float(start.x) == float(end.x):
        if float(start.y) > float(end.y):
            temp = end
            end = start
            start = temp
    l1 = Line(start, end)
    start = l2.src
    end = l2.dst
    if float(start.x) > float(end.x):
        temp = end
        end = start
        start = temp
    if float(start.x) == float(end.x):
        if float(start.y) > float(end.y):
            temp = end
            end = start
            start = temp
    l2 = Line(start, end)
    if (l1.src == l2.dst):
        return l1.src
    if (l1.dst == l2.src):
        return l1.dst
    x1, y1 = float(l1.src.x), float(l1.src.y)
    x2, y2 = float(l1.dst.x), float(l1.dst.y)

    x3, y3 = float(l2.src.x), float(l2.src.y)
    x4, y4 = float(l2.dst.x), float(l2.dst.y)

    xNum = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    xDen = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    yNum = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    yDen = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if xDen == 0 or yDen == 0:
        return None

    Px = xNum / xDen
    Py = yNum / yDen

    if (
            min(x1, x2) <= Px <= max(x1, x2)
            and min(y1, y2) <= Py <= max(y1, y2)
            and min(x3, x4) <= Px <= max(x3, x4)
            and min(y3, y4) <= Py <= max(y3, y4)
    ):
        return Point(Px, Py)

    return None


class StreetOperation:
    def __init__(self):
        self.points = []
        self.names = []
        self.street = {}

    def add(self, street):
        if street is not None:
            flag = False
            for st in self.names:
                if st == street[0]:
                    flag = True
            if flag:
                print("Error: the street has already existed", file=sys.stderr)
            else:
                self.names.append(street[0])
                self.points.append(street[1])
                line = []

                p = self.points[len(self.points) - 1]
                for i in range(1, len(p)):
                    parts1 = p[i - 1].split(',')
                    parts2 = p[i].split(',')
                    p1 = Point(parts1[0].replace("(", ""), parts1[1].replace(")", ""))
                    p2 = Point(parts2[0].replace("(", ""), parts2[1].replace(")", ""))
                    l = Line(p1, p2)
                    line.append(l)
                self.street.setdefault(street[0], line)
        else:
            print("Error: input wrong street", file=sys.stderr)

    def remove(self, street):
        if street is not None:
            index = 0
            j: int = 0
            flag = False
            removedName = ""
            for st in self.names:
                if st == street[0]:
                    flag = True
                    index = j
                    removedName = st
                j += 1
            if flag:
                self.names.pop(index)
                self.points.pop(index)
                self.street.pop(removedName)
            else:
                print("Error: street does not exist", file=sys.stderr)
        else:
            print("Error: input wrong street ", file=sys.stderr)

    def modify(self, street):
        if street is not None:
            index = 0
            j: int = 0
            flag = False
            removedName = ""
            for st in self.names:
                if st == street[0]:
                    flag = True
                    index = j
                    removedName = st
                j += 1
            if flag:
                self.points[index] = street[1]
                self.street.pop(removedName)
                line = []
                p = self.points[index]
                for i in range(1, len(p)):
                    parts1 = p[i - 1].split(',')
                    parts2 = p[i].split(',')
                    p1 = Point(parts1[0].replace("(", ""), parts1[1].replace(")", ""))
                    p2 = Point(parts2[0].replace("(", ""), parts2[1].replace(")", ""))
                    l = Line(p1, p2)
                    line.append(l)
                self.street.setdefault(street[0], line)
            else:
                print("Error: street does not exist", file=sys.stderr)
        else:
            print("Error: input wrong street ", file=sys.stderr)

    def generate(self):
        id = 0
        vertices = {}

        vertice = []
        edgeList = []

        intersectionlist = set()
        intersection_dict = {}

        for i in range(len(self.street) - 1):
            for j in range(i + 1, len(self.street)):
                l1 = self.street[self.names[i]]
                l2 = self.street[self.names[j]]
                for fistL in l1:
                    for secondL in l2:
                        ttt = isIntersected(fistL, secondL)

                        if ttt is not None:
                            intersection_dict.setdefault(ttt, []).append(fistL)
                            intersection_dict.setdefault(ttt, []).append(secondL)
                            intersectionlist.add(ttt)

                        if ttt is not None:
                            if str(fistL.dst) not in vertice:
                                id = id + 1
                                vertices[id] = fistL.dst
                                vertice.append(str(fistL.dst))
                            if str(secondL.dst) not in vertice:
                                id = id + 1
                                vertices[id] = secondL.dst
                                vertice.append(str(secondL.dst))
                            if str(fistL.src) not in vertice:
                                id = id + 1
                                vertices[id] = fistL.src
                                vertice.append(str(fistL.src))
                            if str(secondL.src) not in vertice:
                                id = id + 1
                                vertices[id] = secondL.src
                                vertice.append(str(secondL.src))

                        if str(ttt) not in vertice and ttt is not None:
                            id = id + 1
                            vertices[id] = ttt
                            vertice.append(str(ttt))

        # print('V = {', file=sys.stdout)
        # for key, value in vertices.items():
        #     px = pp(value.x)
        #     py = pp(value.y)
        #     x = Point(px, py)
        #     print(f"{key}: {x}")
        # print('}', file=sys.stdout)
        sys.stdout.write('V {}\n'.format(len(vertices)))
        sys.stdout.flush()

        temp = sorted(intersectionlist, key=lambda p: (p.x, p.y))
        intersection_list = temp
        edgeList = []
        for k in range(len(self.street)):
            for line1 in self.street[self.names[k]]:
                start = line1.src
                end = line1.dst
                if float(start.x) > float(end.x):
                    temp = end
                    end = start
                    start = temp
                if float(start.x) == float(end.x):
                    if float(start.y) > float(end.y):
                        temp = end
                        end = start
                        start = temp

                edgePoint = []
                for intersectionPoint in intersection_list:
                    for intersectionPointCorrespondingLine in intersection_dict[intersectionPoint]:
                        if intersectionPointCorrespondingLine == line1:
                            if str(start) not in edgePoint:
                                edgePoint.append(str(start))
                            if str(intersectionPoint) not in edgePoint:
                                edgePoint.append(str(intersectionPoint))
                if str(end) not in edgePoint:
                    edgePoint.append(str(end))

                for i in range(len(edgePoint) - 1):
                    if Line(edgePoint[i], edgePoint[i + 1]) not in edgeList:
                        edgeList.append(Line(edgePoint[i], edgePoint[i + 1]))

        verticesLookUp = {}
        for i in range(len(vertices)):
            verticesLookUp[str(list(vertices.values())[i])] = list(vertices.keys())[i]
        # print('E = {', file=sys.stdout)
        sys.stdout.write('E {')
        sys.stdout.flush()
        for edge in range(len(edgeList) - 1):
            a = verticesLookUp[edgeList[edge].src]
            b = verticesLookUp[edgeList[edge].dst]
            sys.stdout.write(str('<') + str(a) + str(',') + str(b) + str('>') + str(','))
            sys.stdout.flush()

        if (len(edgeList) >= 1):
            sys.stdout.write(str('<') + str(verticesLookUp[edgeList[(len(edgeList) - 1)].src]) + str(',') + str(
                verticesLookUp[edgeList[(len(edgeList) - 1)].dst]) + str('>'))
            sys.stdout.flush()
        # print('}', file=sys.stdout)
        sys.stdout.write('}\n')
        sys.stdout.flush()


def main():
    streetData = StreetOperation()

    while True:
        line = sys.stdin.readline().strip('\n')
        if not line or line == "":
            break
        if line.isspace():
            print("Error: cannot input all spaces", file=sys.stderr)
            continue
        command = re.compile(r'\w+')
        streetName = re.compile(r'\s"([^"]*)"\s*')
        point = re.compile(r'(\(\s*[-+]?\d+\s*,\s*[-+]?\d+\s*\))')
        Nop0 = re.compile(r'(\(\s*[-+]?\w+\s*,\s*[-+]?\w+\s*,\s*[-+]?\w+\s*\))')  # (1,1,1)
        Nop1 = re.compile(r'(\(\s*[-+]?\d+\s*\))')  # (10)
        Nop2 = re.compile(r'(\(\s*[-+]?\w+\s*\))')  # (1a)
        Nop3 = re.compile(r'(\(\s*[-+]?\d+\D*\s*,\s*[-+]?\d+\D+\s*\))')
        Nop4 = re.compile(r'(\(\s*[-+]?\d+\D+\s*,\s*[-+]?\d+\D*\s*\))')
        Nop5 = re.compile(r'(\s*\),\s*\()')

        Nop6 = re.compile(r'(\(\s*[-+]?\w+\s*,\s*[-+]?\w+\s*,\s*[-+]?\w+\s*,\s*[-+]?\w+\s*\))')
        Nop7 = re.compile(r'(\(\s*[-+]?\D+\d+\s*,\s*[-+]?\D*\d+\s*,\s*[-+]?\w+\s*,\s*[-+]?\w+\s*,\s*[-+]?\w+\s*\))')
        Nop8 = re.compile(r'(\(\s*[-+]?\D+\s*,\s*[-+]?\D+\s*,\s*[-+]?\w+\s*,\s*[-+]?\w+\s*,\s*[-+]?\w+\s*,'
                          r'\s*[-+]?\w+\s*\))')


        i = 0
        for chars in line:
            if chars == "(":
                i += 1
            if chars == ")":
                i -= 1
        if i != 0:
            print("Error: check your input missing bracket", file=sys.stderr)
            continue
        try:
            c = command.findall(line)
        except EOFError:
            return
        if len(c) == 0:
            print('Error: please input command', file=sys.stderr)
            continue
        if c[0] in ("add","add ", "gg ", "gg", "mod ", "mod", "rm ", "rm"):
            if c[0] == "add" or c[0] == "mod":
                pattern = r'\w+\s+"[^"]*"\s+(( ?\(\-?\s*\d+\s*,\-?\s*\d+\s*\))+)\s*$'
                if re.match(pattern, line) == None:
                    print(line)
                    print('Error: input format is wrong', file=sys.stderr)
                    continue
            if c[0] == "rm":
                pattern = r'\w+\s+"[^"]*"\s*'
                if re.match(pattern, line) == None:
                    print(line)

                    print('Error: input format is wrong', file=sys.stderr)
                    continue
            s = streetName.findall(line)
            points = point.findall(line)
            nopoint0 = Nop0.findall(line)
            nopoint1 = Nop1.findall(line)
            nopoint2 = Nop2.findall(line)
            nopoint3 = Nop3.findall(line)
            nopoint4 = Nop4.findall(line)
            nopoint5 = Nop5.findall(line)
            nopoint6 = Nop6.findall(line)
            nopoint7 = Nop7.findall(line)
            nopoint8 = Nop8.findall(line)
            if len(nopoint0) != 0 or len(nopoint1) != 0 or len(nopoint2) != 0 or len(nopoint3) != 0 \
                    or len(nopoint4) != 0 or len(nopoint5) != 0  or len(nopoint6)!= 0 \
                    or len(nopoint7)!= 0 or len(nopoint8)!= 0:
                print("Error: invalid point format only (number, number) will be accepted", file=sys.stderr)
                continue
            if c[0] == "add":
                if len(points) > 1 and len(s) != 0:
                    streetData.add([s[0], points])
                    # print(streetData.names)
                    # print(streetData.points)
                    # print(streetData.street)
                else:
                    print("Error: points value are not correct must larger than 1 or input correct the street name", file=sys.stderr)
                    continue
            if c[0] == "mod":
                i = 0
                if len(points) > 1 and len(s) != 0:
                    streetData.modify([s[0], points])
                    # print(streetData.names)
                    # print(streetData.points)
                    # print(streetData.street)
                else:
                    print("Error: points value are not correct must larger than 1 or input correct the street name", file=sys.stderr)
                    continue
            if c[0] == "rm":
                if len(s) == 1 and len(points) == 0:
                    streetData.remove([s[0], points])
                    # print(streetData.names)
                    # print(streetData.points)
                    # print(streetData.street)
                else:
                    print("Error: street name error or input point", file=sys.stderr)
                    continue

            if c[0] == "gg":
                if (len(points) == 0 and len(s) == 0):
                    streetData.generate()
                else:
                    print("Error: gg does not accept input", file=sys.stderr)
                    continue
        else:
            print("Error: command does not exist", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
