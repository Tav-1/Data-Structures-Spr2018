class Empty(BaseException):
    def __init__(self, message):
        self.message = message


class LinkedStack:
    """LIFO Stack implementation using a singly linked list for storage."""

    # -------------------------- nested _Node class --------------------------
    class _Node:
        """Lightweight, nonpublic class for storing a singly linked node."""
        __slots__ = '_element', '_next'         # streamline memory usage

        def __init__(self, element, next):      # initialize node's fields
            self._element = element               # reference to user's element
            self._next = next                     # reference to next node

    # ------------------------------- stack methods ---------------------------
    def __init__(self):
        """Create an empty stack."""
        self._head = None                       # reference to the head node
        self._size = 0                          # number of stack elements

    def __len__(self):
        """Return the number of elements in the stack."""
        return self._size

    def is_empty(self):
        """Return True if the stack is empty."""
        return self._size == 0

    def top(self):
        """Return (but do not remove) the element at the top of the stack.

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._head._element  # top of stack is at head of list

    def push(self, e):
        """Add element e to the top of the stack."""
        # Create a new link node and link it
        node = self._Node(e, self._head)
        self._head = node
        self._size += 1

    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).

        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():
            raise Empty('Stack is empty')
        toReturn = self.top()
        self._head = self._head._next
        self._size -= 1
        return toReturn

    def unOrderedSearch(self, target):
            # Search for the target element in the Stack
        currentNode = self._head
        while currentNode._element is not target and currentNode is not None:
            currentNode = currentNode._next
        else:
            return currentNode is not None

    def printAll(self):
        # print the contents of the Stack
        output = []
        currentNode = self._head
        while currentNode is not None:
            output.append(str(currentNode._element))
            currentNode = currentNode._next
        return " ".join(output)


linkedStack1 = LinkedStack()
linkedStack1.push(5)
linkedStack1.push(10)
linkedStack1.push(22)
linkedStack1.push(35)

print(linkedStack1.unOrderedSearch(10))
print("Stack contents: " + linkedStack1.printAll())   # head --> 35 22 10 5
print(linkedStack1.pop())
print(linkedStack1.pop())
print("Stack contents: " + linkedStack1.printAll())   # head --> 10 5
