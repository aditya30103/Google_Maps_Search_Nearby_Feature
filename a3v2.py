"""
    Refer -
    Chapter 5: Orthogonal Range Searching [pg 102]
    Book: Berg, Mark de - Computational Geometry
    
    PointDatabase:
    Time Complexity: O(n logn)
    Space Complexity: O(n logn)
    
    Query:
    Time Complexity: O(k + (logn)(logn))
    
    k is the number of query outputs
    n is total number of searchable points in database
"""

class PointDatabase:
    class _Node1D:
        __slots__ = '_key', '_left', '_right'
        def __init__(self, k):
            self._key = k
            self._left = None
            self._right = None

    class _Node2D:
        __slots__ = '_key', '_tree', '_left', '_right'
        def __init__(self, k, t):
            self._key = k
            self._tree = t
            self._left = None
            self._right = None

    def builder1D(self, Y):
        """Build a balanced 1D tree."""
        if len(Y) == 1:
            return self._Node1D(Y[0])
        else: 
            mid = len(Y) // 2
            if(len(Y) % 2 == 0):
                mid = mid - 1   
            root = self._Node1D(Y[mid])
            root._left = self.builder1D(Y[:mid + 1])
            root._right = self.builder1D(Y[mid + 1:])
            return root

    def builder2D(self, X, Y):
        """Build a balanced 2D tree."""
        if len(X) == 1:
            return self._Node2D(X[0], self.builder1D([X[0]]))
        else:
            mid = len(X) // 2
            if(len(X) % 2 == 0):
                mid = mid - 1
                 
            median_x = X[mid][0]

            X_left = X[:mid + 1]
            X_right = X[mid + 1:]
            
            Y_left = [p for p in Y if p[0] <= median_x]
            Y_right = [p for p in Y if p[0] > median_x]

            root = self._Node2D(X[mid], self.builder1D(Y))
            root._left = self.builder2D(X_left, Y_left)
            root._right = self.builder2D(X_right, Y_right)
            return root

    def __init__(self, pointlist):
        """PointDatabase Constructor"""
        if len(pointlist) == 0:
            self._root = None
            return

        pointlist_x = sorted(pointlist)
        pointlist_y = sorted(pointlist, key=lambda x: x[1])

        self._root = self.builder2D(pointlist_x, pointlist_y)

    def SplitNode1D(self, pointer, a, b):
        """Find the split node in 1D tree."""
        v = pointer
        while v._left is not None and v._right is not None and (b < v._key[1] or a > v._key[1]):
            if b < v._key[1]: 
                v = v._left
            else: 
                v = v._right
        return v

    def SplitNode2D(self, a, b):
        """Find the split node in 2D tree."""
        v = self._root
        while v._left is not None and v._right is not None and (b < v._key[0] or a > v._key[0]):
            if b < v._key[0]: 
                v = v._left
            else: 
                v = v._right
        return v

    def AddLeaves(self, root, leaves):
        """Add all leaves of the tree rooted at 'root' to 'leaves' list."""
        if root is None: 
            return leaves
        if root._right is None and root._left is None:
            leaves.append(root._key)
            return leaves
        self.AddLeaves(root._left, leaves)
        self.AddLeaves(root._right, leaves)
        return leaves

    def RangeQuery1D(self, pointer, a, b, Out):
        """Perform 1D Range Query."""
        v = self.SplitNode1D(pointer, a, b)
        if v._left is None and v._right is None: 
            if a <= v._key[1] <= b:
                Out.append(v._key)
        else:
            v1 = v._left
            v2 = v._right

            while v1._left is not None and v1._right is not None:
                if a <= v1._key[1]: 
                    self.AddLeaves(v1._right, Out)
                    v1 = v1._left
                else: 
                    v1 = v1._right
            if v1 is not None and a <= v1._key[1]: 
                Out.append(v1._key)

            while v2._left is not None and v2._right is not None:
                if v2._key[1] <= b: 
                    self.AddLeaves(v2._left, Out)
                    v2 = v2._right
                else: 
                    v2 = v2._left
            if v2 is not None and v2._key[1] <= b: 
                Out.append(v2._key)
        return Out

    def searchNearby(self, q, d):
        """2D Range Query Search Function"""
        Points = []
        xl = q[0] - d
        xu = q[0] + d
        yl = q[1] - d
        yu = q[1] + d

        if self._root is None: 
            return Points

        v = self.SplitNode2D(xl, xu)
        if v._left is None and v._right is None: 
            if xl <= v._key[0] <= xu and yl <= v._key[1] <= yu: 
                Points.append(v._key)
        else:
            v1 = v._left
            v2 = v._right

            while v1._left is not None and v1._right is not None:
                if xl <= v1._key[0]: 
                    self.RangeQuery1D(v1._right._tree, yl, yu, Points)
                    v1 = v1._left
                else: 
                    v1 = v1._right
            if v1 is not None and xl <= v1._key[0] <= xu and yl <= v1._key[1] <= yu: 
                Points.append(v1._key)

            while v2._left is not None and v2._right is not None:
                if v2._key[0] <= xu: 
                    self.RangeQuery1D(v2._left._tree, yl, yu, Points)
                    v2 = v2._right
                else: 
                    v2 = v2._left
            if v2 is not None and xl <= v2._key[0] <= xu and yl <= v2._key[1] <= yu: 
                Points.append(v2._key)

        return Points


pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10), (9,2), (10,5)])
print(pointDbObject.searchNearby((4,8), 2))

