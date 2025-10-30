# Summary: Doubly Linked List that updates both FIFO items and LILO
# items from both ends of a list of nodes.
class DLLNode:
    """Setup Class for a node in a doubly linked list
    ...
    Attributes
    ----------
    data: any
        Represents any inserted data type in a node list
    next: DLLNode
        The next item in a node list.
    prev: DLLNode
        The previous item in a node list
    """
    def __init__(self, data = None, node = None, prev = None):
        self.data = data
        self.next = node
        self.prev = prev

class DoublyLinkedList:
    """Class for a doubly linked list logic
    ...
    Attributes
    ----------
    head: DLLNode
        Represents the first item in a node list
    tail: DLLNode
        Represents the last item in a node list
    data: any
        Represents any inserted data type in a node list
    size: int
        The length of the node list

    Methods
    ---------
    Mutators
        insert_at_begin(data):
            Insert a node at the beginning of the DLL. Return boolean
        insert_at_index(data, index):
            Insert a node at the specified index in the DLL. Return boolean
        insert_at_end(data):
            Insert a node at the end of the DLL
        remove_first_node:
            Remove the first node in the DLL
        remove_at_index(index):
            Remove the node at the specified index in the DLL. Return boolean
        remove_last_node:
            Remove the last node in the DLL and return
        remove_node:
            Searches and removes node with specified data from the DLL
        update_node:
            Update the node at the specified index with the specified data
    Accessors
        size_of_DLL():
            Calculate and return the size of DLL
        validate_head_exists():
            Check if the head exists and return boolean
        validate_tail_exists():
            Check if the tail exists and return boolean
        print_errors():
            Print errors if the head or tail are not set when they should be (
            removal, insertion in middle of DLL, etc.)
        print_DLL():
            Default print method for the DLL
        rev_print_DLL():
            Prints the DLL in reverse
    """
    def __init__(self, data = None, head = None, tail = None):
        super().__init__()
        self.head = head
        self.tail = tail
        self.data = data
        self.size = 0

    # mutators ------------------------------------
    def insert_at_begin(self, data):
        """Insert a node at the beginning of the DLL. Return boolean"""
        # create new node
        new_node = DLLNode(data)
        if not self.validate_head_exists():
            self.head = new_node
            if not self.validate_tail_exists():
                self.tail = new_node
            return True
        else:
            # set the new node's pointer to the head
            new_node.next = self.head
            # set the current head's pointer to the new node (pushing head to
            # the 1st index)
            self.head.prev = new_node
            # set the node to the head position
            self.head = new_node
            return True

    def insert_at_index(self, data, index):
        """Insert a node at the specified index in the DLL. Return boolean"""
        if index == 0:
            self.insert_at_begin(data)
            return
        # if index is the end of the list
        if index == self.size_of_DLL():
            self.insert_at_end(data)
            return

        position = 0
        current_node = self.head
        while current_node is not None and position + 1 != index:
            position = position + 1
            current_node = current_node.next

        if current_node is not None and position + 1 == index:
            new_node = DLLNode(data)
            new_node.next = current_node.next
            new_node.prev = current_node

            if current_node.next:
                current_node.next.prev = new_node
            current_node.next = new_node
            return
        else:
            print("Index not present")

    def insert_at_end(self, data):
        """Insert a node at the end of the DLL"""
        # create a new node and set the node pointer.next to None
        new_node = DLLNode(data)
        new_node.next = None

        # If there is nothing in the list, set the head and tail to the new node
        if not self.validate_head_exists() and not self.validate_tail_exists():
            self.head = new_node
            self.tail = new_node
            return False
        # else set the tail's next pointer to the new node
        self.tail.next = new_node
        # set the new node's previous pointer to the tail
        new_node.prev = self.tail
        # set the tail equal to the new node
        self.tail = new_node
        return True

    def remove_first_node(self):
        """Remove the first node in the DLL"""
        # check if the head exists
        # check if the size of the list is 1, if so then simply delete the
        # node which points to both the head and tail
        if self.size_of_DLL() == 1:
            self.head = None
            self.tail = None
        else:
            # set the head to the next node in the list
            self.head = self.head.next
            # set new head's pointer to none
            self.head.prev = None
            return True
        return False

    def remove_at_index(self, index):
        """Remove the node at the specified index in the DLL. Return boolean"""
        # if the list is empty, return
        if not self.validate_head_exists() and not self.validate_tail_exists():
            self.print_errors()
            return False

        # else set the current node to the head and initialize position counter
        current_node = self.head
        position = 0

        # check if the node is actually at the beginning
        if index == 0:
            # if so use the remove_first_node function
            self.remove_first_node()
            return True
        # check if the node is at the end of the list
        elif index == (self.size_of_DLL() - 1):
            # if so use the remove_last_node function
            self.remove_last_node()
            return True
        else:
            # traverse the list as long as there are items left in the list
            # and we haven't reached the item before the index we want to remove
            while current_node is not None and position < index:
                # add 1 to the position so we can keep advancing through the
                # list
                position += 1
                # set the current node to the next node
                current_node = current_node.next

            # if we've exhausted the list print "Index not present"
            if current_node is None:
                return False
            else: # if we found the index and the data matches
                if current_node.prev:
                # set the previous node's next pointer to the item after the
                # one we want to delete
                    current_node.prev.next = current_node.next
                    # set the next nodes's previous pointer to the previous
                    # pointer's next
                if current_node.next:
                    current_node.next.prev = current_node.prev

            # remove node from the list
            current_node.next = None
            current_node.prev = None
            return True

    def remove_last_node(self):
        """Remove the last node in the DLL and return"""
        # if the list is empty, return
        if not self.validate_head_exists() and not self.validate_tail_exists():
            return False

        if self.size_of_DLL() == 1:
            self.head = None
            self.tail = None
            return True
        # else set the current node to the tail
        current_node = self.tail
        # set the tail to the previous node
        self.tail = current_node.prev
        # set the new tail's next pointer to none (so it no longer
        # points to the tail we want to delete
        self.tail.next = None
        return True

    def remove_node(self, data):
        """Searches and removes node with specified data from the DLL"""
        # check if the head is empty aka the list is empty
        if not self.validate_head_exists():
            self.print_errors()
            return False
        # set current_node to head
        current_node = self.head

        # Check if the head node contains the specified data
        if current_node.data == data:
            self.remove_first_node()
            return True
        # else
        # if the current Node exists and it's data doesn't match our search
        while current_node is not None:
            if current_node.data == data:
                break
            # move the current_node pointer to the next node
            current_node = current_node.next

        # if the current node is None (reached end of the list, return False to
        # exit
        if current_node is not None:
            # check if the next node is None, if so, that means the current
            # node is the tail
            if current_node.next is None:
                # using the remove_last_node function instead
                self.remove_last_node()
                return True
            # if the next node exists and the node before it exists
            elif (current_node.next is not None \
                  and current_node.prev is not None):
                # set the next node to the next node's 'next' pointer to the
                # the next node
                current_node.next.prev = current_node.prev
                # set the next node's previous pointer to the previous node
                current_node.prev.next = current_node.next
                return True
        #else
        return False

    def update_node(self, data, index):
        """Update the node at the specified index with the specified data"""
        # set the current node to the head
        current_node = self.head
        # initialize the position to 0
        position = 0
        # if the position is equal to the index update the data
        if position == index:
            current_node.data = data
        else: # begin traversing the list as long as the node is not None and
            # position is not equal to the index
            while current_node is not None and position != index:
                # advance position counter and node to next item in node list
                position += 1
                current_node = current_node.next

            # if the node is not None set the data and return True
            if current_node is not None:
                current_node.data = data
                return True
            # else
            return False
        # if the 0th index was updated return True
        return True

    # accessor  -----------------------------------------------------------
    def size_of_DLL(self):
        """Calculate and return the size of DLL"""
        size = 0
        # Check if the head exists
        if self.head:
            # set the pointer to the head
            current_node = self.head
            # While there are still nodes in the list
            while current_node:
                # add one in the node add 1 to the size
                size += 1
                # advance to the next node in the list
                current_node = current_node.next
            # return the size
            return size
        else:
            return 0 # return if the head doesn't exist

    # instance helpers --------------------------------------------------

    def validate_head_exists(self):
        """Check if the head exists and return boolean"""
        # check if the head is empty
        if self.head is None:
            # return because the list is empty!
            return False
        # else
        return True

    def validate_tail_exists(self):
        """Check if the tail exists and return boolean"""
        # check if the head is empty
        if self.tail is None:
            # return because the list is empty!
            return False
        # else
        return True

    def print_errors(self):
        """Print errors if the head or tail are not set when they should be (
        removal, insertion in middle of DLL, etc.)"""
        if not self.validate_head_exists():
            print("Error: Head is not set")
        if not self.validate_tail_exists():
            print("Error: Tail is not set")
        return

    # display  ------------------------------------------------------------
    def print_DLL(self):
        """Default print method for the DLL"""
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next
        return

    def rev_print_DLL(self):
        """Prints the DLL in reverse"""
        current_node = self.tail
        while current_node:
            print(current_node.data)
            current_node = current_node.prev
        return


def main():
    # create a new linked list
    dllist = DoublyLinkedList()

    # add nodes to the linked list
    dllist.insert_at_end('a')
    dllist.insert_at_end('b')
    dllist.insert_at_begin('c')
    dllist.insert_at_end('d')
    dllist.insert_at_index('x', 4)
    dllist.insert_at_index('z', 4)
    dllist.insert_at_index('g', 2)

    # print the doubly linked list
    print("Node Data:")
    dllist.print_DLL()

    # print the doubly linked list in reverse
    print("Reverse Node Data:")
    dllist.rev_print_DLL()

    print("\nSize of linked list:", dllist.size_of_DLL())

    # remove nodes from the linked list
    print("\nAfter Removing First Node:")
    dllist.remove_first_node()
    dllist.print_DLL()

    print("\nAfter Removing Last Node:")
    dllist.remove_last_node()
    dllist.print_DLL()

    print("\nAfter Removing Node at Index 1:")
    dllist.remove_at_index(1)
    dllist.print_DLL()

    print("\nAfter Removing Node at Index 2:")
    dllist.remove_at_index(2)
    dllist.print_DLL()

    print("\nUpdate node Value to 'z' at Index 0:")
    dllist.update_node('z', 0)
    dllist.print_DLL()

    print("\nSize of linked list:", dllist.size_of_DLL())

    print("\nAttempt to Remove Node with data 'g':")
    dllist.remove_node('g')
    dllist.print_DLL()

    print("\nAfter Removing Node with data 'z':")
    dllist.remove_node('z')
    dllist.print_DLL()


if __name__ == "__main__":
    main()

"""
Node Data:
c
a
g
b
d
z
x
Reverse Node Data:
x
z
d
b
g
a
c

Size of linked list: 7

After Removing First Node:
a
g
b
d
z
x

After Removing Last Node:
a
g
b
d
z

After Removing Node at Index 1:
a
b
d
z

After Removing Node at Index 2:
a
b
z

Update node Value to 'z' at Index 0:
z
b
z

Size of linked list: 3

Attempt to Remove Node with data 'g':
z
b
z

After Removing Node with data 'z':
b
z
"""
