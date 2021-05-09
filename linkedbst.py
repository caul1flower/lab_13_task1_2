"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import random
from time import time


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            while True:
                if node is None:
                    return None
                elif item == node.data:
                    return node.data
                elif item < node.data:
                    node = node.left
                else:
                    node = node.right

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            while True:
                if item < node.data:
                    if node.left == None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                elif node.right == None:
                    node.right = BSTNode(item)
                    break
                else:
                    node = node.right
                    # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            else:
                return 1 + max(height1(top.left), height1(top.right))
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        size = self._size
        return height < (2*log(size+1, 2)-1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = []
        item = self.successor(low)
        if self.find(low):
            lst.append(low)
        while low <= item <= high:
            lst.append(item)
            item = self.successor(item)
            if item == None:
                break
        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        lst = sorted(self.inorder())
        self.clear()

        def recursive_add(lst):
            length = len(lst)
            middle = length // 2

            if lst == []:
                return
            self.add(lst[middle])
            recursive_add(lst[:middle])
            recursive_add(lst[middle+1:])
        recursive_add(lst)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def recurse(node, item, success=None):
            """Recursive function"""
            if node != None:
                if node.data <= item:
                    return recurse(node.right, item, success)
                elif node.data > item:
                    if node.left == None or node.left.data <= item:
                        success = node.data
                        return success
                    return recurse(node.left, item, success)
        return recurse(self._root, item)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def recurse(node, item, success=None):
            """Recursive function"""
            if node != None:
                if node.data >= item:
                    return recurse(node.left, item, success)
                elif node.data < item:
                    if node.right == None or node.right.data >= item:
                        success = node.data
                        return success
                    return recurse(node.right, item, success)
        return recurse(self._root, item)

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as inp_file:
            num_words = sum(1 for line in inp_file)

        def random_words_generator(path):
            """
            Generate 10000 random words from the given file.
            """
            with open(PATH, 'r', encoding='utf-8') as inp_file:
                random_words_lst = []
                counter = 0
                random_nums_lst = [random.randrange(0, num_words) for _ in range(10000)]
                for line in inp_file:
                    if counter in random_nums_lst:
                        random_words_lst.append(*line.split()) 
                    counter += 1
            return random_words_lst

        def text_to_list(PATH):
            """
            Return a list of words from the file.
            """
            with open(PATH, 'r', encoding='utf-8') as inp_file:
                words_lst = []
                for line in inp_file:
                    words_lst.append(*line.split()) 
            return words_lst

        def search_in_lst(lst_file, random_words):
            """
            Return time needed for a search in a list.
            """
            start = time()
            for word in random_words:
                lst_file.index(word)
            fnsh = time()
            return fnsh-start

        def generate_tree_with_already_sorted_words(PATH):
            """
            Return binary tree with the words that are sorted in the alphabet way.
            """
            bin_tree = LinkedBST()
            with open(PATH, 'r') as inp_file:
                for line in inp_file:
                    line = line.strip()
                    bin_tree.add(line)
            return bin_tree

        def search_in_bin_tree(bin_tree, random_words):
            """
            Return time needed for a search in a binary tree.
            """
            start = time()
            for word in random_words:
                bin_tree.find(word)
            fnsh = time()
            return fnsh-start

        def generate_tree_with_unsorted_words(PATH, lst_file):
            """
            Return tree with words that are given randomly.
            """
            bin_tree = LinkedBST()
            unsorted_words = sorted(lst_file, key=lambda k: random.random())
            for word in unsorted_words:
                bin_tree.add(word)
            return bin_tree

        random_words = random_words_generator(path)
        lst_file = text_to_list(path)
        bin_tree_sorted = generate_tree_with_already_sorted_words(path)
        bin_tree_unsorted = generate_tree_with_unsorted_words(PATH, lst_file)

        # first test 
        fir_result = search_in_lst(lst_file, random_words)
        print(f'Time needed for a search in a list: {fir_result}')

        # second test
        sec_result = search_in_bin_tree(bin_tree_sorted, random_words)
        print(f'Time needed for a search in the binary tree that was already sorted: {sec_result}')

        # third test
        th_result = search_in_bin_tree(bin_tree_unsorted, random_words)
        print(f'Time needed for a search in the binary tree with not sorted words: {th_result}')

        bin_tree_unsorted.rebalance()
        # forth test
        forth_result = search_in_bin_tree(bin_tree_unsorted, random_words)
        print(f'Time needed for a search in the binary tree that is balanced: {forth_result}')


if __name__ == "__main__":
    bst = LinkedBST()
    PATH = 'words.txt'
    for el in [2, -1, 3, 4, 5, 6, -3]:
        bst.add(el)
    bst.demo_bst(PATH)
