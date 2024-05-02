import math
import numpy

FEAVector = tuple[float, float, float]

def normal(a: FEAVector, b: FEAVector, c: FEAVector) -> FEAVector:

    ab = numpy.subtract(b, a)
    ac = numpy.subtract(c, a)

    d = numpy.cross(ab, ac)
    l = numpy.linalg.norm(d)

    return (d[0] / l, d[1] / l, d[2] / l)

class FEANode:

    def __init__(self, number: int, name: str, position: FEAVector, displacement: FEAVector = (0.0, 0.0, 0.0), force: FEAVector = (0.0, 0.0, 0.0)):

        self.number = number

        self.name = name

        self.position = position
        self.displacement = displacement
        self.force = force

        self.normalList: list[FEAVector] = []
        self.normalIndex: dict[str, FEAVector] = {}

        self.angles: list[float] = []

        self.angleMin = float('inf')
        self.angleMax = float('-inf')

        self.angleAvg = 0.0

class FEAQuad:

    def __init__(self, number: int, name: str, node1: FEANode, node2: FEANode, node3: FEANode, node4: FEANode):

        self.number = number

        self.name = name

        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.node4 = node4

        self.nodeList = [node1, node2, node3, node4]

class FEAModel:

    def __init__(self):

        self.nodeList: list[FEANode] = []
        self.quadList: list[FEAQuad] = []

        self.nodeIndex: dict[str, FEANode] = {}
        self.quadIndex: dict[str, FEAQuad] = {}

        self.xMin = float('inf')
        self.xMax = float('-inf')

        self.yMin = float('inf')
        self.yMax = float('-inf')

        self.zMin = float('inf')
        self.zMax = float('-inf')

        self.xCenter: float = None
        self.yCenter: float = None
        self.zCenter: float = None

        self.xSpread: float = None
        self.ySpread: float = None
        self.zSpread: float = None

        self.displacementMin = float('inf')
        self.displacementMax = float('-inf')

        self.displacementSpread: float = None

        self.forceMin = float('inf')
        self.forceMax = float('-inf')

        self.forceSpread: float = None

        self.angleMin = float('inf')
        self.angleMax = float('-inf')

        self.angleSpread: float = None

    def node(self, name: str, position: FEAVector, displacement: FEAVector = (0.0, 0.0, 0.0), force: FEAVector = (0.0, 0.0, 0.0)):
        
        if self.forceSpread is not None:
            raise Exception("Model is already locked!")
        if name in self.nodeIndex:
            raise Exception("Node name already in use!")
        
        node = FEANode(len(self.nodeList), name, position, displacement, force)

        self.nodeList.append(node)
        self.nodeIndex[name] = node

        # Coordinate min/max

        x, y, z = position

        self.xMin = min(self.xMin, x)
        self.xMax = max(self.xMax, x)

        self.yMin = min(self.yMin, y)
        self.yMax = max(self.yMax, y)

        self.zMin = min(self.zMin, z)
        self.zMax = max(self.zMax, z)

        # Displacement min/max

        displacementCurrent = numpy.linalg.norm(displacement)

        self.displacementMin = min(self.displacementMin, displacementCurrent)
        self.displacementMax = max(self.displacementMax, displacementCurrent)

        # Force min/max

        forceCurrent = numpy.linalg.norm(force)

        self.forceMin = min(self.forceMin, forceCurrent)
        self.forceMax = max(self.forceMax, forceCurrent)
    
    def quad(self, name: str, nodeName1: str, nodeName2: str, nodeName3: str, nodeName4: str):
        
        if self.forceSpread is not None:
            raise Exception("Model is already locked!")
        if name in self.quadIndex:
            raise Exception("Quad name already in use!")
        if nodeName1 not in self.nodeIndex:
            raise Exception("Node 1 not defined!")
        if nodeName2 not in self.nodeIndex:
            raise Exception("Node 2 not defined!")
        if nodeName3 not in self.nodeIndex:
            raise Exception("Node 3 not defined!")
        if nodeName4 not in self.nodeIndex:
            raise Exception("Node 4 not defined!")
        
        node1 = self.nodeIndex[nodeName1]
        node2 = self.nodeIndex[nodeName2]
        node3 = self.nodeIndex[nodeName3]
        node4 = self.nodeIndex[nodeName4]

        quad = FEAQuad(len(self.quadList), name, node1, node2, node3, node4)

        self.quadList.append(quad)
        self.quadIndex[name] = quad

        # Calculate normals

        normal1 = normal(node1.position, node2.position, node4.position)
        normal2 = normal(node2.position, node3.position, node1.position)
        normal3 = normal(node3.position, node4.position, node2.position)
        normal4 = normal(node4.position, node1.position, node3.position)

        node1.normalList.append(normal1)
        node2.normalList.append(normal2)
        node3.normalList.append(normal3)
        node4.normalList.append(normal4)

        node1.normalIndex[name] = normal1
        node2.normalIndex[name] = normal2
        node3.normalIndex[name] = normal3
        node4.normalIndex[name] = normal4
    
    def lock(self):

        if self.forceSpread is not None:
            raise Exception("Model is already locked!")
        
        self.xSpread = self.xMax - self.xMin
        self.ySpread = self.yMax - self.yMin
        self.zSpread = self.zMax - self.zMin

        self.xCenter = self.xMin + self.xSpread / 2
        self.yCenter = self.yMin + self.ySpread / 2
        self.zCenter = self.zMin + self.zSpread / 2

        self.displacementSpread = self.displacementMax - self.displacementMin

        self.forceSpread = self.forceMax - self.forceMin

        # Calculate angles between node normals

        for node in self.nodeList:
            stop = len(node.normalList)
            count = stop * (stop - 1) / 2
            for i in range(stop):
                normal1 = node.normalList[i]
                for j in range(i + 1, stop):
                    normal2 = node.normalList[j]

                    angle = math.acos(numpy.dot(normal1, normal2))
                    
                    node.angles.append(angle)
                    node.angleMin = min(node.angleMin, angle)
                    node.angleMax = max(node.angleMax, angle)
                    node.angleAvg = node.angleAvg + angle / count
        
        # Caculate range of angles between node normals
        
        for node in self.nodeList:
            self.angleMin = min(self.angleMin, node.angleAvg)
            self.angleMax = max(self.angleMax, node.angleAvg)
        
        self.angleSpread = self.angleMax - self.angleMin
    
    def color(self, node: FEANode, angle = False):

        if self.forceSpread is None:
            raise Exception("Model is not locked yet!")

        if self.displacementSpread > 0:
            
            displacementAbsolute = numpy.linalg.norm(node.displacement)
            displacementRelative = (displacementAbsolute - self.displacementMin) / self.displacementSpread

            r = displacementRelative
            b = 1.0 - displacementRelative

        else:

            r = 1.0
            b = 1.0

        if self.angleSpread > 0:

            angleRelative = (node.angleAvg - self.angleMin) / self.angleSpread if angle else 0.0

            g = angleRelative

        else:

            g = 0.0

        return r, g, b

def makeFEAPoints(model: FEAModel, thickness = 1, displacementScale = 1.0, colorScale = 1.0):

    # Import
    
    from panda3d.core import GeomVertexFormat
    from panda3d.core import GeomVertexData
    from panda3d.core import GeomVertexWriter
    from panda3d.core import GeomPoints
    from panda3d.core import GeomNode
    from panda3d.core import Geom
    from panda3d.core import NodePath

    # Define format

    format = GeomVertexFormat.getV3n3cpt2()

    # Build data

    data = GeomVertexData('points', format, Geom.UHDynamic)

    # Write vertex data

    vertex = GeomVertexWriter(data, 'vertex')

    for node in model.nodeList:

        px, py, pz = node.position
        dx, dy, dz = node.displacement

        vertex.addData3(px + dx * displacementScale, py + dy * displacementScale, pz + dz * displacementScale)

    # Write color data

    color = GeomVertexWriter(data, 'color')

    for node in model.nodeList:

        r, g, b = model.color(node, True)

        color.addData4f(r * colorScale, g * colorScale, b * colorScale, 1.0)

    # Build points

    points = GeomPoints(Geom.UHDynamic)

    i = 0
    for node in model.nodeList:

        points.addVertex(i)

        i = i + 1
    
    geom = Geom(data)
    geom.addPrimitive(points)

    node = GeomNode("points")
    node.addGeom(geom)

    path = NodePath(node)
    path.setRenderModeThickness(thickness)

    return path

def makeFEALines(model: FEAModel, thickness = 1, displacementScale = 1.0, colorScale = 1.0):

    # Import classes
    
    from panda3d.core import GeomVertexFormat
    from panda3d.core import GeomVertexData
    from panda3d.core import GeomVertexWriter
    from panda3d.core import GeomLines
    from panda3d.core import GeomNode
    from panda3d.core import Geom
    from panda3d.core import NodePath

    format = GeomVertexFormat.getV3n3cpt2()

    # Build data

    data = GeomVertexData('points', format, Geom.UHDynamic)

    # Write vertex data

    vertex = GeomVertexWriter(data, 'vertex')

    for node in model.nodeList:

        px, py, pz = node.position
        dx, dy, dz = node.displacement

        vertex.addData3(px + dx * displacementScale, py + dy * displacementScale, pz + dz * displacementScale)

    # Write color data

    color = GeomVertexWriter(data, 'color')

    for node in model.nodeList:

        r, g, b = model.color(node, True)

        color.addData4f(r * colorScale, g * colorScale, b * colorScale, 1.0)

    # Build lines
        
    cache: dict[str, bool] = {}

    lines = GeomLines(Geom.UHDynamic)

    for quad in model.quadList:

        line1 = f"{quad.node1.number}-{quad.node2.number}"
        line2 = f"{quad.node2.number}-{quad.node3.number}"
        line3 = f"{quad.node3.number}-{quad.node4.number}"
        line4 = f"{quad.node4.number}-{quad.node1.number}"
        
        if line1 not in cache:
            lines.addVertices(quad.node1.number, quad.node2.number)
        if line2 not in cache:
            lines.addVertices(quad.node2.number, quad.node3.number)
        if line3 not in cache:
            lines.addVertices(quad.node3.number, quad.node4.number)
        if line4 not in cache:
            lines.addVertices(quad.node4.number, quad.node1.number)
        
        cache[line1] = True
        cache[line2] = True
        cache[line3] = True
        cache[line4] = True

    # Build geom
    
    geom = Geom(data)
    geom.addPrimitive(lines)

    # Build node

    node = GeomNode("lines")
    node.addGeom(geom)

    # Build path

    path = NodePath(node)
    path.setRenderModeThickness(thickness)

    return path

def makeFEATriangles(model: FEAModel, displacementScale = 1.0, colorScale = 1.0):

    # Import classes
    
    from panda3d.core import GeomVertexFormat
    from panda3d.core import GeomVertexData
    from panda3d.core import GeomVertexWriter
    from panda3d.core import GeomTriangles
    from panda3d.core import GeomNode
    from panda3d.core import Geom
    from panda3d.core import NodePath

    format = GeomVertexFormat.getV3n3cpt2()

    # Build data

    data = GeomVertexData('points', format, Geom.UHDynamic)

    # Write vertex data

    vertex = GeomVertexWriter(data, 'vertex')

    for quad in model.quadList:

        for node in quad.nodeList:

            px, py, pz = node.position
            dx, dy, dz = node.displacement

            vertex.addData3(px + dx * displacementScale, py + dy * displacementScale, pz + dz * displacementScale)

    # Write color data

    color = GeomVertexWriter(data, 'color')

    for quad in model.quadList:

        for node in quad.nodeList:

            r, g, b = model.color(node)

            color.addData4f(r * colorScale, g * colorScale, b * colorScale, 1.0)

    # Build lines

    triangles = GeomTriangles(Geom.UHDynamic)

    for quad in model.quadList:

        triangles.addVertices(quad.number * 4 + 0, quad.number * 4 + 1, quad.number * 4 + 2)
        triangles.addVertices(quad.number * 4 + 2, quad.number * 4 + 3, quad.number * 4 + 0)

    # Build geom
    
    geom = Geom(data)
    geom.addPrimitive(triangles)

    # Build node

    node = GeomNode("triangles")
    node.addGeom(geom)

    # Build path

    path = NodePath(node)
    path.setTwoSided(True)

    return path