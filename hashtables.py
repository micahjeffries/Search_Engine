class HashTableLinear:
    """Class for linear implementation for hash table
    Attributes:
        num_items (int): number of items in the hash table
        capacity (int): size of the hash table
        num_collisions (int): number of collisions in the hash process
        hash_table (HashTableLinear): hash table containing values
        keys (HashTableLinear): hash table containing keys
    """
    def __init__(self, table_size=11):
        """Create the attributes of the HashTableLinear
        """
        self.num_items = 0
        self.capacity = table_size
        self.num_collisions = 0
        self.hash_table = [None]*table_size
        self.keys = [None]*table_size

    def __repr__(self):
        """Define the string representation of HashTableLinear
        Returns:
            string: string representation of HashTableLinear
        """
        return "HashTableLinear{hash_table: %s, keys: %s, num_items: %d, capacity: %d, num_collisions: %d}"\
            %(self.hash_table, self.keys, self.num_items, self.capacity, self.num_collisions)

    def __eq__(self, other):
        """Determine if two hash tables are equal to each other
        Returns:
            boolean: True if hash tables are equal and false if they are not
        """
        return isinstance(other, HashTableLinear)\
            and self.num_items == other.num_items\
            and self.capacity == other.capacity\
            and self.num_collisions == other.num_collisions\
            and self.hash_table == other.hash_table\
            and self.keys == other.keys

    def __getitem__(self,key):
        """get an item in the hash table
        Args:
            key (str): key
        Returns:
            *: key-value pair associated with the key
        """
        return self.get(key)

    def __setitem__(self,key,data):
        """put item in the hash table
        Args:
            key (str): key
            data (int): data associated with key
        """
        self.put(key,data)

    def __contains__(self,key):
        """determine if a hash table contains the given key
        Args:
            key (str): key
        Returns:
            boolean: true if the key is in the hash table; false otherwise
        """
        return self.contains(key)

    def keys(self):
        """Returns a list of keys in your hash table
        Returns:
            list: list of keys in the hash table
        """
        return self.keys

    def put(self,key,data=0):
        """put item in the hash table
        Args:
            key (str): key
            data (int): data associated with key
        """
        # Calculate the position in the hash table based on the key
        # If there is nothing at the given key, insert the key-value pair in the hash table
        # Else
            # Increment number of collisions
            # If the key is the same in the current position, replace the value in the hash table
            # Else
                # Rehash the position using the linear rehash technique
                # While the slot in the hash table is not empty and not equal to the key
                    # Rehash the position using the linear rehash technique
                    # Increment the number of collisions
                # If there is nothing at the rehashed position, insert the key-value pair
                # Else, replace the value in the hash table
        # Increase the number of items by 1
        # If the new load factor is over 0.75
            # Store the capacity, and key/value hash tables in temporary variables
            # Erase the these values with a new capacity of 2*old_size + 1
            # For each key in the hash table
                # Calculate the position in the hash table based on the key
                # If there is nothing at the given key, insert the key-value pair in the hash table
                # Else
                    # Increment number of collisions
                    # If the key is the same in the current position, replace the value in the hash table
                    # Else
                        # Rehash the position using the linear rehash technique
                        # While the slot in the hash table is not empty and not equal to the key
                            # Rehash the position using the linear rehash technique
                            # Increment the number of collisions
                        # If there is nothing at the rehashed position, insert the key-value pair
                    # Else, replace the value in the hash table
        key = str(key)
        position = hash_string(key)%self.capacity
        
        if self.keys[position] is None:
            self.keys[position] = key
            self.hash_table[position] = data
        else:
            self.num_collisions += 1
            if self.keys[position] == key:
                self.hash_table[position] = data
            else:
                position = self.linear_rehash(position)
                while self.keys[position] and self.keys[position] != key:
                    position = self.linear_rehash(position)
                    self.num_collisions += 1

                if self.keys[position] == None:
                    self.keys[position] = key
                    self.hash_table[position] = data
                else:
                    self.hash_table[position] = data

        self.num_items += 1
        if self.load_factor() > 0.75:
            temp_capacity = self.capacity
            self.capacity = self.capacity*2 + 1
            temp_keys = self.keys
            temp_hash = self.hash_table
            self.keys = [None]*self.capacity
            self.hash_table = [None]*self.capacity

            for key in temp_keys:
                if key:
                    key = str(key)
                    position = hash_string(key)%temp_capacity
                    data = temp_hash[position]
                    position = hash_string(key)%self.capacity

                    if self.keys[position] is None:
                        self.keys[position] = key
                        self.hash_table[position] = data
                    else:
                        self.num_collisions += 1
                        if self.keys[position] == key:
                            self.hash_table[position] = data
                        else:
                            position = self.linear_rehash(position)
                            while self.keys[position] and self.keys[position] != key:
                                position = self.linear_rehash(position)
                                self.num_collisions += 1
                            
                            if self.keys[position] == None:
                                self.keys[position] = key
                                self.hash_table[position] = data
                            else:
                                self.hash_table[position] = data


    def linear_rehash(self, old_position):
        """helper function that gets a new index in the hash table via linear rehashing
        Returns:
            int: index in the hash table
        """
        # Return new position in hash table using linear rehashing technique
        return (old_position + 1)%self.capacity

    def get(self,key):
        """get an item in the hash table
        Args:
            key (str): key
        Returns:
            *: key-value pair associated with the key
        Raises:
            LookupError: if the key is not in the hash table
        """
        # Calculate the starting position
        # While the value is not none and not found and not stop
            # If the key is at the given position, you found it!
                # Retrieve the data value
            # Else, rehash the position
                # If the new rehashed position is equal to the starting position, stop the search
        # Return the data value
        key = str(key)
        start = hash_string(key)%self.capacity

        data = None
        stop = found = False
        position = start
        while self.keys[position] != None and not found and not stop:
            if self.keys[position] == key:
                found = True
                data = self.hash_table[position]
            else:
                position = self.linear_rehash(position)
                if position == start:
                    stop = True
        return data
        
    def contains(self,key):
        """determine if a hash table contains the given key
        Args:
            key (str): key
        Returns:
            boolean: true if the key is in the hash table; false otherwise
        """
        # Calculate the starting position
        # While the value is not none and not found and not stop
            # If the key is at the given position, you found it!
            # Else, rehash the position
                # If the new rehashed position is equal to the starting position, stop the search
        # If you found it, return True
        # Else, return False
        key = str(key)
        start = hash_string(key)%self.capacity

        found = stop = False
        position = start
        while self.keys[position] != None and not found and not stop:
            if self.keys[position] == key:
                found = True
            else:
                position = self.linear_rehash(position)
                if position == start:
                    stop = True
        if found:
            return True
        return False

    def remove(self,key):
        """Remove a key-value pair from the hash table
        Args:
            key (str): key
        Returns:
            *: key value pair associated with given key
        Raises:
            LookupError: if the key is not in the hash table
        """
        # Use the contains function to determine if the key is in the hash table
        # If the key is in the hash table, return the data value
        # Else raise LookupError
        key = str(key)
        if self.contains(key):
            position = hash_string(key)%self.capacity
            self.keys[position] = None
            data = self.hash_table[position]
            self.hash_table[position] = None
            return data
        raise LookupError()

    def size(self):
        """Determine number of items in the hash table
        Returns:
            int: number of items in the hash table
        """
        return self.num_items

    def load_factor(self):
        """Determine the load facotr of the hash table
        Returns:
            int: load factor
        """
        return self.num_items/self.capacity

    def collisions(self):
        """Determine the number of collisions during the rehashing process
        Returns:
            int: number of collisions
        """
        return self.num_collisions

def import_stopwords(filename, hashtable):
    """returns mutable hash table object with stop words
    Args:
        filename (file): stop words text file
        hashtable (*): mutable hash table object
    Returns:
        hashtable (*): mutable hash table object
    """
    # Open the given input file
    # For each word in the file, insert it into a hash table
    # Return the hash table
    stop_words = open(filename, 'r')
    for line in stop_words:
        words = line.split(" ")
        for word in words:
            hashtable.put(word, 0)
    return hashtable

def hash_string(string):
    """Determine the hash number of a string
    Args:
        string (str): string
    Returns:
        hash (int): hash number of given string
    """
    # For each character in the string
        # Calculate the new hash value
    # Return the hash table
    hash = 0
    for c in string:
        hash = (hash * 31 + ord(c))
    return hash
