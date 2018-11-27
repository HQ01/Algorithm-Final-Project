import random
import numpy as np
class Queue:
    """
    Implement the queue abstract data type for breathfirst use.
    Support: enqueue, dequeue, ieEmpty and front.
    """
    class _Node:
        """
        _Node is a private class used to represent nodes in the linked list
        that is implenting the type.
        """
        __slots__ = 'data', 'next'

        def __init__(self, data=None, next=None):
            """
            A node constructor for implementing the queue
            """
            self.data = data
            self.next = next
    def __init__(self):
        """
        Queue constructor
        """
        self._head = None
        self._tail = None
        self._size = 0
    def enqueue(self, item):
        """
        enqueue: adds the item at the tail of the list.
        """
        if self._head is None:
            self._head = self._tail = self._Node(item)
            self._size +=1
        else:
            self._tail.next = self._Node(item)
            self._tail = self._tail.next
            self._size +=1
    def dequeue(self):
        """
        dequeue: remove and return the next item.
        """
        if self._head is None:
            raise ValueError
        result = self._head.data
        self._head = self._head.next
        self._size -=1
        if self._head is None:
            self.tail = None
        return result

    def is_empty(self):
        """
        isEmpty: a queue is empty iff its _head is None.
        """
        return self._head is None

    def front(self):
        """
        Returns a reference to the data item
        in the first node.
        """
        if self is None:
            raise ValueError
        return self._head.data
    def __len__(self):
        """
        length method, return the length of the queue
        """
        return self._size

class Tree:

    # ------------------------ nested Position class --------------------------
    class Position:
        """
        Abstraction representing the location of a single element within a tree
        """

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node._element
        def score(self):
            """
            Return the score of the board representing by this position
            """
            return self._node._score

        def __eq__(self, other):
            """
            Return True iff other is a Position representing the same location.
            """
            return type(other) is type(self) and other._node is self._node

    # -------------------------- nested _Node class --------------------------
    class _Node:
        """
        Lightweight, nonpublic class for storing a node.
        _element stores the board, _parent stores parent's position, _score stores board's score, _children is a list storing
        all the positions node's children's
        """
        __slots__ = '_element', '_parent', '_children', '_score'
        def __init__(self, element, parent=None, children = None,score=None):
            self._element = element
            self._parent = parent
            self._score = score
            if children == None:
                # default value of children
                self._children = []
            else:
                self._children = children
    # --------------------------tree constructor ----------------------
    def __init__(self):
        """Create an initially empty tree."""
        self._root = None
        self._size = 0

    # -------------------------- public accessors --------------------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root position of the tree (or None if tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p):
        """Return the position of p's parent (or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def num_children(self, p):
        """Return the number of children of position p."""
        node = self._validate(p)
        return len(node._children)

    def sibling(self, p):
        """
        Return a Position representing p s sibling (or None if no sibling).
        """
        parent = self.parent(p)
        result = []
        if parent is None:  # p must be the root
            return None    # root has no sibling
        else:
            for child in self.children(self,parent):
                if child != p:
                    result.append(child)
                else:
                    continue# possibly None
        return result

    def children(self, p):
        """
        A generator yielding every single child of position P 's position
        """
        node = self._validate(p)
        if len(node._children) != 0:
            for child in node._children:
                yield self._make_position(child)

    def is_root(self, p):
        """Return True if position P represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if position P does not have any children."""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root."""
        return 0 if self.is_root(p) else 1 + self.depth(self.parent(p))


    # ------------------------------- utility methods -------------------------------
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

    # -------------------------- nonpublic mutators --------------------------
    def _add_root(self, e):
        """
        Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_child(self, p, e):
        """
        Adding a new child for position P, storing element e
        Retrn the position of the latest added child
        """
        node = self._validate(p)
        self._size += 1
        node._children.append(self._Node(e, node))                  # node is its parent
        return self._make_position(node._children[-1])

    def _add_score(self,p,score):
        """
        Adding a score to position P
        Return the score added
        """
        node = self._validate(p)
        node._score = score
        return node._score

    def _replace(self, p, e):
        """
        Replace the element at position p with e, and return the current element.
        """
        node = self._validate(p)
        node._element = e
        return e


    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.positions():            # use same order as positions()
            yield p                          # but yield each element

    def positions(self):
        """Generate an iterable of the tree's positions."""
        #return self.preorder()     # return entire preorder iteration
        return self.breadthfirst()
    def breadthfirst(self):
        """Generate a breadth-first iteration of the positions of the tree."""
        if not self.is_empty():
            fringe = Queue()                  # known positions not yet yielded
            fringe.enqueue(self.root())       # starting with the root
            while not fringe.is_empty():
                p = fringe.dequeue()          # remove from front of the queue
                yield p                       # report this position
                for c in self.children(p):
                    fringe.enqueue(c)         # add children to back of queue


def game_constructor(unroll_depth):
    counter = 0
    board = Tree()
    board._add_root("X")
    cur_pos = board.root()
    gen_board(board,cur_pos,counter,unroll_depth)
    return board


def gen_board(board,pos,counter,unroll_depth,score_init = True):
    cur_val = pos.element()
    if counter < unroll_depth:
        new_pos_1 = board._add_child(pos,cur_val+"0")
        new_pos_2 = board._add_child(pos,cur_val+"1")
        gen_board(board,new_pos_1,counter+1,unroll_depth)
        gen_board(board,new_pos_2,counter+1,unroll_depth)
    else:
        if score_init:
            score = np.random.normal(0, 1)
            # score = np.random.uniform(-1.0,1.0)
            #score = np.random.poisson()
            #score = np.random.exponential()
            board._add_score(pos,score)

def scoring_master(board, ORDER):
    if ORDER == "minmax":
        scoring_min_max_master(board)
    elif ORDER == "maxmin":
        scoring_max_min_master(board)
    return
def scoring_min_max_master(board):
    choice = []
    for child in board.children(board.root()):
        score = scoring_min_max_second(board,child)
        choice.append(score)
    minvalue = min(choice)
    board._add_score(board.root(),minvalue)
    return
def scoring_max_min_master(board):
    choice = []
    for child in board.children(board.root()):
        score = scoring_max_min_second(board,child)
        choice.append(score)
    maxvalue = max(choice)
    board._add_score(board.root(),maxvalue)
    return
def scoring_min_max_first(board,position):
    if board.is_leaf(position):
        return position.score()
    else:
        choice = []
        for child in board.children(position):
            score = scoring_min_max_second(board,child)
            choice.append(score)
        minvalue = min(choice)
        board._add_score(position,minvalue)
        return position.score()
def scoring_min_max_second(board,position):
    if board.is_leaf(position):
        return position.score()
    else:
        choice = []
        for child in board.children(position):
            score = scoring_min_max_first(board,child)
            choice.append(score)
        maxvalue = max(choice)
        board._add_score(position,maxvalue)
        return position.score()
def scoring_max_min_first(board,position):
    if board.is_leaf(position):
        return position.score()
    else:
        choice = []
        for child in board.children(position):
            score = scoring_max_min_second(board,child)
            choice.append(score)
        maxvalue = max(choice)
        board._add_score(position,maxvalue)
        return position.score()
def scoring_max_min_second(board,position):
    if board.is_leaf(position):
        return position.score()
    else:
        choice = []
        for child in board.children(position):
            score = scoring_max_min_first(board,child)
            choice.append(score)
        minvalue = min(choice)
        board._add_score(position,minvalue)
        return position.score()
