from Node import Node

class LinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None
        
    def get_first(self):
        if self.__head != None:
            return self.__head.data
        else:
            return None
        
    def get_last(self):
        if self.__tail != None:
            return self.__tail.data
        else:
            return None
        
    def get_at(self, index):
        if self.__head == None:
            return None
        else:
            temp = self.__head
            
            # "traverse" or step down the chain
            for i in range(0, index):
                if temp == None:
                    return None
                else:
                    temp = temp.next
                
            if temp == None:
                return None
            else:
                return temp.data

    def add_first(self, data):
        # create a new node using the data
        new_node = Node(data)
        
        # add it to the front of the list
        if self.__head == None:
            self.__head = new_node
            self.__tail = new_node
        else:
            new_node.next = self.__head
            self.__head = new_node    # new_node becomes the head
            
    def add_last(self, data):
        # create a new node using the data
        new_node = Node(data)
        
        # add it to the end of the list
        if self.__head == None:
            self.__head = new_node
            self.__tail = new_node
        else:
            self.__tail.next = new_node
            self.__tail = new_node     # new_node becomes the tail

    def add_at(self, index, data):
        # if index = 0, add to front
        if index == 0:
            self.add_first(data)
            return       # end the method
        
        # create a new node
        new_node = Node(data)
        
        # traverse the list to just before the index to add
        temp = self.__head 
        
        for i in range(index - 1):    # notice the -1
            if temp.next != None:     # make sure we do not run over the end
                temp = temp.next
                
        # insert the new node
        new_node.next = temp.next
        temp.next = new_node
   
    def remove_first(self):
        # Special case, empty list so nothing to remove
        if self.__head == None:
            return        # end the method
        
        # Special case, single node in the list
        if self.__head.next == None:
            self.__head == None 
            self.__tail == None 
            
        # remove the head node from the data
        self.__head = self.__head.next 
        
    def remove_last(self):
        # Special case, empty list so nothing to remove
        if self.__head == None:
            return        # end the method
        
        # Special case, single node in the list
        if self.__head.next == None:
            self.__head == None 
            self.__tail == None 
            return        # end the method
                  
        # traverse the list and find the SECOND to last node
        temp = self.__head 
        
        while temp.next.next != None: # notice .next.next to
            temp = temp.next          #  find second to last node
            
        # delete the last node
        temp.next = None
        
    def remove_at(self, index):
        # Special case, empty list so nothing to remove
        if self.__head == None:
            return        # end the method
        
        # Special case, single node in the list
        if self.__head.next == None:
            self.__head == None 
            self.__tail == None 
            return        # end the method
            
        # traverse the list and find the NODE BEFORE the index
        temp = self.__head 
        
        for i in range(index - 1):    # notice the -1
            if temp.next.next != None:  # make sure we do not run over the end
                temp = temp.next
                
        # delete the node at that index
        temp.next = temp.next.next
        
    def is_empty(self):
        # if the head is empty, then the list is empty
        return self.__head == None 
    
    def get_length(self):
        # create count variable
        count = 0
        
        # traverse the list and count the nodes
        temp = self.__head 
        
        while temp != None:
            count += 1
            temp = temp.next
            
        return count
                
    def get_list(self):
        # create output variable
        items = ""
        
        # start at the top
        temp = self.__head
        
        # append all the data
        while temp != None:
            items += str(temp.data) + " "
            temp = temp.next
            
        # return the output variable
        return items        
                
    def contains(self, data):
        # check each node and see if it matches the data
        # start at the top with the head node
        temp = self.__head
        
        # traverse the list
        while temp != None:
            if temp.data == data:
                return True    # return True if we find the data!
            else:
                temp = temp.next
            
        # if we go through every node and do not find the data, return false
        return False
    
    def clear_list(self):
        self.__head = None
        self.__tail = None