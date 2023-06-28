# Range Tree Approach!
# Change Function Names and Comment Time Complexity

class PointDatabase:

    class _Node1D:
        __slots__ = '_key', '_left', '_right'
        def __init__ (self, k):
            self._key = k
            self._left = None
            self._right = None

    class _Node2D:
        __slots__ = '_key', '_tree', '_left', '_right'
        def __init__ (self, k, t):
            self._key = k
            self._tree = t
            self._left = None
            self._right = None
    
    def Preorder(self, pointer, Output):
        v = pointer
        if v is not None:
            Output.append(v._key)
            self.Preorder(v._left, Output)
            self.Preorder(v._right, Output)
        return Output
    
    def builder1D(self, Y):
        if len(Y) == 1: return self._Node1D(Y[0])
        mid = len(Y)//2
        Y1 = []
        Y2 = []
        for i in range(0, len(Y)):
            if (i < mid): Y1.append(Y[i])
            else: Y2.append(Y[i])
        root = self._Node1D(Y[mid-1])
        root._left = self.builder1D(Y1)
        root._right = self.builder1D(Y2)
        return root

    # X, Y are pointlists presorted in x, and y respectively
    def builder2D(self, X, Y):
        if (len(X) == 1): 
            temp = self._Node1D(X[0])
            return self._Node2D(X[0], temp)
            # I have evaded the problem!!!
        mid = len(X)//2
        X1 = []
        X2 = []
        Y1 = []
        Y2 = []
        for i in range(0, len(X)):
            if (i < mid): X1.append(X[i])
            else: X2.append(X[i]) 
        for i in range(0, len(Y)):
            if (Y[i][0] < X[mid][0]): Y1.append(Y[i])
            else: Y2.append(Y[i])
        root = self._Node2D(X[mid-1], self.builder1D(Y))
        root._left = self.builder2D(X1, Y1)
        root._right = self.builder2D(X2, Y2)
        return root

    def __init__(self, pointlist):
        if (len(pointlist) != 0):
            pointlistX = [0]*len(pointlist)
            pointlistY = [0]*len(pointlist)
            Y = [(0,0)]*len(pointlist)
            for i in range(0, len(pointlist)):
                Y[i] = (pointlist[i][1], i)
            Y.sort()
            for j in range(0, len(Y)):
                pointlistY[j] = pointlist[Y[j][1]]
            pointlist.sort()
            for k in range(0, len(pointlist)):
                pointlistX[k] = pointlist[k]
            self._root = self.builder2D(pointlistX, pointlistY)
        else:
            self._root = None

    def SplitNode1D(self, pointer, a, b):
        v = pointer
        while (v._left is not None and v._right is not None and (b < v._key[1] or a > v._key[1])):
            if (b <= v._key[1]): v = v._left
            else: v = v._right
        return v
                # Equals ka kya karna hai?
    def SplitNode2D(self, a, b):
        v = self._root
        while (v._left is not None and v._right is not None and (b < v._key[0] or a > v._key[0])):
            if (b <= v._key[0]): v = v._left
            else: v = v._right
        return v

    def AddLeaves(self, root, l):
        if root is None: return l
        if root._right is None and root._left is None:
            l.append(root._key)
            return l
        self.AddLeaves(root._left, l)
        self.AddLeaves(root._right, l)
        return l

    def RangeQuery1D(self, pointer, a, b, Out):
        v = self.SplitNode1D(pointer, a, b)
        # L = []
        # print(self.Preorder(v, L))
        # print("Y Split Node: ", v._key)
        if (v._left is None and v._right is None): 
            if (a <= v._key[1] and v._key[1] <=b): 
                Out.append(v._key)
                # print("Y Split Node is Leaf: ", v._key)
        else:
            v1 = v._left
            v2 = v._right

            # print("Y v1 update: ", v1._key)
            while (v1._left is not None and v1._right is not None):
                if a <= v1._key[1]: 
                    self.AddLeaves(v1._right, Out)
                    # print(Out)
                    v1 = v1._left
                    # print("Y v1 update: ", v1._key)
                else: 
                    v1 = v1._right
                    # print("Y v1 update: ", v1._key)
            if (a <= v1._key[1]): 
                Out.append(v1._key)
                # print("Y Terminating Leaf: ", v._key)

            # print("Y v2 update: ", v2._key)
            while (v2._left is not None and v2._right is not None):
                if v2._key[1] <= b: 
                    self.AddLeaves(v2._left, Out)
                    # print(Out)
                    v2 = v2._right
                    # print("Y v2 update: ", v2._key)
                else: 
                    v2 = v2._left
                    # print("Y v2 update: ", v2._key)
            if (v2._key[1] <= b): 
                Out.append(v2._key)
                # print("Y Terminating Leaf: ", v2._key)
        return Out

    def searchNearby(self, q, d):
        Points = []
        xl = q[0]-d
        xu = q[0]+d
        yl = q[1]-d
        yu = q[1]+d

        if self._root is None: return Points
        v = self.SplitNode2D(xl, xu)
        # print("Split Node: ", v._key)
        if (v._left is None and v._right is None): 
            if (xl <= v._key[0] and v._key[0] <=xu): 
                if (yl <= v._key[1] and v._key[1] <=yu): 
                    Points.append(v._key)
                    # print("Split Node is Leaf: ", v._key)
        else:
            v1 = v._left
            v2 = v._right

            # print("v1 update: ", v1._key)
            while (v1._left is not None and v1._right is not None):
                if xl <= v1._key[0]: 
                    self.RangeQuery1D(v1._right._tree, yl, yu, Points)
                    # Points.append(O)
                    # print(O)       # To search in corresponding Y-tree according to Y parameters
                    v1 = v1._left
                    # print("v1 update: ", v1._key)
                else: 
                    v1 = v1._right
                    # print("v1 update: ", v1._key)
            if (xl <= v1._key[0] and v1._key[0] <=xu): 
                if (yl <= v1._key[1] and v1._key[1] <=yu): 
                    Points.append(v1._key)
                    # print("Terminating Leaf: ", v1._key)

            # print("v2 update: ", v2._key)
            while (v2._left is not None and v2._right is not None):
                if v2._key[0] <= xu: 
                    self.RangeQuery1D(v2._left._tree, yl, yu, Points)       # To search in corresponding Y-tree according to Y parameters
                    v2 = v2._right
                    # print("v2 update: ", v2._key)
                else: 
                    v2 = v2._left
                    # print("v2 update: ", v2._key)
            if (xl <= v2._key[0] and v2._key[0] <=xu): 
                if (yl <= v2._key[1] and v2._key[1] <=yu): 
                    Points.append(v2._key)
                    # print("Terminating Leaf: ", v2._key)
        return Points

# pointDbObject = PointDatabase([])
# print(pointDbObject.searchNearby((4,8), 2))

