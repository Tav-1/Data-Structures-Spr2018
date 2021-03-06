from linked_queue import LinkedQueue
# from math import abs
class LinkedBinaryTree():
    """Linked representation of a binary tree structure."""

    # -------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a node."""
        __slots__ = '_element', '_parent', '_left', '_right'  # streamline memory usage

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    # -------------------------- nested Position class ------------------------
    class Position():
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    # ------------------------------- utility methods -------------------------
    def _validate(self, p):
        """Return associated node, if position is valid."""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:      # convention for deprecated nodes
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        """Return Position instance for given node (or None if no node)."""
        return self.Position(self, node) if node is not None else None

    def sibling(self, p):
        """Return a Position representing p's sibling (or None if no sibling)."""
        parent = self.parent(p)
        if parent is None:                    # p must be the root
            return None                         # root has no sibling
        else:
            if p == self.left(parent):
                return self.right(parent)         # possibly None
            else:
                return self.left(parent)          # possibly None

    # ------------------------------- binary_tree methods ---------------------

    def children(self, p):
        """Generate an iteration of Positions representing p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p) is not None:  # if left child exists, traverse its subtree
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p                               # visit p between its subtrees
        if self.right(p) is not None:         # if right child exists, traverse its subtree
            for other in self._subtree_inorder(self.right(p)):
                yield other

    # override inherited version to make inorder the default
    def positions(self):
        """Generate an iteration of the tree's positions."""
        return self.inorder()

    def is_root(self, p):
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def _height2(self, p):                  # time is linear in size of subtree
        """Return the height of the subtree rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        """Return the height of the subtree rooted at Position p.

        If p is None, return the height of the entire tree.
        """
        ############################ Task 1 height ###############################
        if p is None:
            p = self.root()
        return self._height2(p)        # start _height2 recursion

    #-------------------------- binary tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    #-------------------------- public accessors --------------------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the Position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:     # left child exists
            count += 1
        if node._right is not None:    # right child exists
            count += 1
        return count

    # -------------------------- nonpublic mutators --------------------------
    def add_root(self, e):
        """Place element e at the root of an empty tree and return new Position.

        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def add_left(self, p, e):
        """Create a new left child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e, node)                  # node is its parent
        return self._make_position(node._left)

    def add_left_tree(self, p, l):
        """Insert a subtree to the left node of a node at position P
        Return the new tree.
        """
        node = self._validate(p)
        otherNode = l.root()
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += l._size
        node._left = otherNode._node
        return self

    def add_right_tree(self, p, r):
        """Insert a subtree to the left node of a node at position P
        Return the new tree.
        """
        node = self._validate(p)
        otherNode = r.root()
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += r._size
        node._right = otherNode._node
        return self

    def add_right(self, p, e):
        """Create a new right child for Position p, storing element e.

        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        node._right = self._Node(e, node)                 # node is its parent
        return self._make_position(node._right)

    def replace(self, p, e):
        """Replace the element at position p with e, and return old element."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def delete(self, p):
        """Delete the node at Position p, and replace it with its child, if any.

        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('Position has two children')
        child = node._left if node._left else node._right  # might be None
        if child is not None:
            child._parent = node._parent   # child's grandparent becomes parent
        if node is self._root:
            self._root = child             # child becomes root
        else:
            parent = node._parent
        if node is parent._left:
            parent._left = child
        else:
            parent._right = child
        self._size -= 1
        node._parent = node              # convention for deprecated node
        return node._element

    def attach(self, p, t1, t2):
        """Attach trees t1 and t2, respectively, as the left and right subtrees
        of the external Position p.
        As a side effect, set t1 and t2 to empty.
        Raise TypeError if trees t1 and t2 do not match type of this tree.
        Raise ValueError if Position p is invalid or not external.
        """
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):    # all 3 trees must be same type
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():         # attached t1 as left subtree of node
            t1._root._parent = node
            node._left = t1._root
            t1._root = None             # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():         # attached t2 as right subtree of node
            t2._root._parent = node
            node._right = t2._root
            t2._root = None             # set t2 instance to empty
            t2._size = 0

    def levelorderPrint(self):
        """Generate a breadth-first iteration of the positions of the tree."""
        if not self.is_empty():
            queue = LinkedQueue()             # known positions not yet yielded
            queue.enqueue(self.root())        # starting with the root
            while not queue.is_empty():
                p = queue.dequeue()             # remove from front of the queue
                # yield p                          # report this position
                print("from levelOrder: ", p.element())
                for c in self.children(p):
                    # add children to back of queue
                    queue.enqueue(c)

    def preorderPrint(self, p):
        if p is not None:
            print("from PreorderPrint:", p.element())
        if self.left(p) is not None:
            self.preorderPrint(self.left(p))
        if self.right(p) is not None:
            self.preorderPrint(self.right(p))

    def postorderPrint(self, p):
        if self.left(p) is not None:
            self.postorderPrint(self.left(p))
        if self.right(p) is not None:
            self.postorderPrint(self.right(p))
        if p is not None:
            print("from PostorderPrint:", p.element())

    def inorderPrint(self, p):
        if self.left(p) is not None:
            self.inorderPrint(self.left(p))
        if p is not None:
            print("from InorderPrint:", p.element())
        if self.right(p) is not None:
            self.inorderPrint(self.right(p))

    def pretty_print(self):
        levels = self.height() + 1
        self._print_internal([self._root], 1, levels)

    def _print_internal(self, this_level_nodes, current_level, max_level):
        if (len(this_level_nodes) == 0 or all_elements_are_None
                (this_level_nodes)):
            return  # Base case of recursion: out of nodes, or only None left

        floor = max_level - current_level
        endgeLines = 2 ** max(floor - 1, 0)
        firstSpaces = 2 ** floor - 1
        betweenSpaces = 2 ** (floor + 1) - 1
        print_spaces(firstSpaces)
        next_level_nodes = []
        for node in this_level_nodes:
            if (node is not None):
                print(node._element, end="")
                next_level_nodes.append(node._left)
                next_level_nodes.append(node._right)
            else:
                next_level_nodes.append(None)
                next_level_nodes.append(None)
                print_spaces(1)

            print_spaces(betweenSpaces)
        print()
        for i in range(1, endgeLines + 1):
            for j in range(0, len(this_level_nodes)):
                print_spaces(firstSpaces - i)
                if (this_level_nodes[j] == None):
                    print_spaces(endgeLines + endgeLines + i + 1)
                    continue
                if (this_level_nodes[j]._left != None):
                    print("/", end="")
                else:
                    print_spaces(1)
                print_spaces(i + i - 1)
                if (this_level_nodes[j]._right != None):
                    print("\\", end="")
                else:
                    print_spaces(1)
                print_spaces(endgeLines + endgeLines - i)
            print()

        self._print_internal(next_level_nodes, current_level + 1, max_level)

    # -------------------------- Assignment 7 functions -----------------------

    def getLevels(self, target):
        elts = []

        def _recurse(level, node):
            if level != target:
                level += 1
                if node.left():
                    _recurse(level, self._validate(node).left())
                if node.right():
                    _recurse(level, self._validate(node).right())
            else:
                elts.append(self._validate(node)._element())
        _recurse(target, self.root())
        return elts

    def print_level_line_by_line(self):
        for i in range(self.height()):
            print(self.getLevels(i))

    def heightRecurse(self, node):
        if node is None:
            return True
        leftHeight = self.height(self.left(node))
        rightHeight = self.height(self.right(node))
        if abs(leftHeight - rightHeight) > 2:
            print(leftHeight)
            print(rightHeight)
            return False
        else:
            return self.heightRecurse(self.left(node)) and \
                    self.heightRecurse(self.right(node))

    def is_height_balanced(self):
        return self.heightRecurse(self.root())

    def sameRecurse(self, other, node1, node2):
        try:
            if node1.element() != node2.element():
                return False
            else:
                return self.sameRecurse(other, self.left(node1),
                                        other.left(node2)) and \
                    self.sameRecurse(other, self.right(node1),
                                     other.right(node2))
        except AttributeError:  # node1 and node2 are NoneType
            return True

    def sameSame(self, other):  # See alternateImplementations.py for alternate
        return self.sameRecurse(other, self.root(), other.root())

    def sum_of_leaves(self):  # See alternateImplementations.py for alternate
        # Problem 4
        return sum(i.element() for i in self.positions() if self.is_leaf(i))

    def LCA(self, p1, p2):
        # Problem 5
        pass

    def evaluate(self):
        # Problem 7
        postFixList = []

        def _genPostFixList(p):
            if self.left(p) is not None:
                self.postorderPrint(self.left(p))
            if self.right(p) is not None:
                self.postorderPrint(self.right(p))
            if p is not None:
                print("P: ", p.element().element())
                postFixList.append(p.element().element())

        _genPostFixList(self.root())
        print("postFixList: ", postFixList)
        # return self.calcPostOrder(postFixList)


def build_expression_tree(postfix):
    # Problem 6
    def _buildSubtree(op1, op2, oper):
        subtree = LinkedBinaryTree()
        subtree.add_root(oper)
        if type(op1) is LinkedBinaryTree():
            subtree.add_left_tree(subtree.root(), op1)
        else:
            subtree.add_left(subtree.root(), op1)

        if type(op2) is LinkedBinaryTree():
            subtree.add_right_tree(subtree.root(), op2)
        else:
            subtree.add_right(subtree.root(), op2)

        return subtree

    operators = ["+", "-", "*", "/"]
    postfixStack = postfix.split(" ")
    numStack = []
    while(len(postfixStack) > 0):
        i = postfixStack.pop(0)
        print("i: ", i)
        if type(i) is LinkedBinaryTree:
            numStack.append(i)
            print("numStack: ", numStack)
        elif i.isdigit():
            numStack.append(i)
        elif i in operators:
            postfixStack = [_buildSubtree(numStack.pop(0), numStack.pop(0),
                            i)] + postfixStack  # insert subtree
        else:
            return postfixStack[0]


def calcPostOrder(opStack):
    # Helper function to Problem 7
    operators = ["+", "-", "*", "/"]
    opStack, evalStack = opStack, []
    while(len(opStack) > 0):
        item = opStack.pop(0)
        if item in operators:
            operand1, operand2 = evalStack.pop(), evalStack.pop()
            opStack = [eval(operand1, operand2, item)] + opStack
            if len(opStack) == 1:
                return opStack[0]
        else:
            try:
                if float(item):
                    evalStack.append(item)
            except ValueError:
                break
    return opStack[0]


def eval(operand1, operand2, operator):
    operand1, operand2 = float(operand1), float(operand2)
    if operator == "+":
        return str(operand1 + operand2)
    elif operator == "-":
        return str(operand1 - operand2)
    elif operator == "*":
        return str(operand1 * operand2)
    elif operator == "/":
        return str(operand1 / operand2)
    else:
        print("Invalid operation! Restart the program.")


print("Test 1:", calcPostOrder(list("32+4/32*4++")))
    # -------------------------- End of assignment 7 functions ----------------


def all_elements_are_None(list_of_nodes):
    for each in list_of_nodes:
        if each is not None:
            return False
    return True


def print_spaces(number):
    for i in range(number):
        print(" ", end="")



#########################################################
# Test case booleans, flip to True to enable testing
print_level_line_by_line_test = False
is_height_balanced_test = True
sameSame_test = False
sum_of_leaves_test = False
LCA_test = False
build_expression_tree_test = False
evaluate_test = False
#########################################################


def main():

    ###################### Generate sample tree 1 #######################
    T1 = LinkedBinaryTree()
    a = T1.add_root("A")
    b = T1.add_left(a, "B")
    c = T1.add_left(b, "C")
    d = T1.add_right(b, "D")
    T1.add_left(c, "E")
    T1.add_right(c, "F")
    T1.add_left(d, "G")
    x1 = T1.add_right(a, "1")
    T1.add_left(x1, "2")
    x3 = T1.add_right(x1, "3")
    T1.add_left(x3, "4")
    x5 = T1.add_right(x3, "5")
    x6 = T1.add_left(x5, "6")
    # T1.pretty_print()    #If you want to visualize sample tree, uncomment this

    ###################### Generate sample tree 2 #######################

    T = LinkedBinaryTree()
    eight = T.add_root(8)
    three = T.add_left(eight, 3)
    zero = T.add_right(eight, 0)
    one = T.add_left(three, 1)
    six = T.add_right(three, 6)
    four = T.add_left(six, 4)
    five = T.add_right(six, 5)
    seven = T.add_right(zero, 7)
    two = T.add_left(seven, 2)
    nine = T.add_left(zero, 9)
    # T.pretty_print()  #If you want to visualize this sample tree, uncomment this

    ###################### Generate sample tree 3, same as T1 #######################

    T2 = LinkedBinaryTree()
    a = T2.add_root("A")
    b = T2.add_left(a, "B")
    c = T2.add_left(b, "C")
    d = T2.add_right(b, "D")
    e = T2.add_left(c, "E")
    f = T2.add_right(c, "F")
    g = T2.add_left(d, "G")
    x1 = T2.add_right(a, "1")
    T2.add_left(x1, "2")
    x3 = T2.add_right(x1, "3")
    T2.add_left(x3, "4")
    x5 = T2.add_right(x3, "5")
    x6 = T2.add_left(x5, "6")
    # T2.pretty_print()    #If you want to visualize sample tree, uncomment this

    ###################### Test codes.............. #######################

    if (print_level_line_by_line_test):
        print("Testing problem 1.......: Print levels line by line")
        T1.print_level_line_by_line()
        # For the sample Tree:
        # A
        # B 1
        # C D 2 3
        # E F G 4 5
        # 6
    if (is_height_balanced_test):
        print("Testing problem 2.......: is the tree height balanced?")
        # Should be False for this tree
        print(T1.is_height_balanced(), "    Expected result is False")
        # Should be True for this tree
        print(T.is_height_balanced(), "    Expected result is True")

    if (sameSame_test):
        print("Testing problem 3.......: Same Tree")
        print(T1.sameSame(T2), "    Expected result is True")   # True
        print(T1.sameSame(T), "    Expected result is False")   # False

    if (sum_of_leaves_test):
        print("Testing problem 4.......: Sum of leaves")
        print(T.sum_of_leaves(), "    Expected result is 21")

    if (LCA_test):
        print("Testing problem 5.......: Lowest common ancestor")
        print(T2.LCA(g, c).element(), "    Expected result is B")
        print(T2.LCA(d, x3).element(), "    Expected result is A")

    if (build_expression_tree_test):
        print("Testing problem 6.......: Expression Tree")
        build_expression_tree("1 2 * 3 4 / +").pretty_print()
        # build_expression_tree("5 7 6 + 3 - *").pretty_print()

    if (evaluate_test):
        print("Testing problem 7.......: Evaluating Expression Tree")
        print(build_expression_tree("1 2 * 3 4 / +").evaluate(),
              "    Expected result is 2.75")
        # print(build_expression_tree("5 7 6 + 3 - *").evaluate(),
        # "    Expected result is 50")


main()
