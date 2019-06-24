import numpy as np # arrays
from banker import start_banker
from prettyprint import print_iteration

class State:
    def __init__(self, num_customers, num_resources, maximum, total, allocated):
        assert len(maximum) == num_customers, "New state maximum array size is not consistent with num_customers, num_resources"
        assert len(maximum[0]) == num_resources, "New state maximum array size is not consistent with num_customers, num_resources"
        assert len(total) == num_resources, "New state total array size is not consistent with num_customers, num_resources"
        assert len(allocated) == num_customers, "New state allocated array size is not consistent with num_customers, num_resources"
        assert len(allocated[0]) == num_resources, "New state allocated array size is not consistent with num_customers, num_resources"
        self.__num_customers = num_customers
        self.__num_resources = num_resources

        self.__maximum = np.array(maximum)
        self.__allocated = np.array(allocated)
        self.__total = np.array(total)

        self.__update_dependents()
    def copy(self):
        state = State(self.__num_customers, self.__num_resources, self.__maximum, self.__total, self.__allocated)
        return state

    @staticmethod
    def create_from_file(filename, total, allocated):
        maximum = []
        with open(filename, 'r') as maxfile:
            for line in list(maxfile):
                line = ''.join(line.split())                # remove all whitespaces
                if line == '': continue
                nums = line.split(',')                      # tokenize string by comma
                nums = [num for num in nums if num != '']   # filter out empty tokens
                nums = [int(num) for num in nums]           # convert each token to an int
                maximum.append(nums)
        
        num_customers = len(maximum)
        num_resources = len(maximum[0])

        system = State(num_customers, num_resources, maximum, total, allocated)
        return system

    def release_resources(self, cust_num, release_count=[]):
        assert 0 <= cust_num and cust_num < self.__num_customers, f'release_allocated: cust_num={cust_num} out of range'
        if len(release_count) == 0:
            # release everything
            self.__allocated[cust_num].fill(0)
        else:
            assert len(release_count) == self.__num_resources, f'release_allocated: invalid size for release_count={release_count}'
            self.__allocated[cust_num] -= np.array(release_count)
            self.__allocated[self.__allocated < 0] = 0 # convert negative results to zero
        self.__update_dependents()

    def request_resources(self, cust_num, request_count=[]):
        assert 0 <= cust_num and cust_num < self.__num_customers, f'request_resources: cust_num={cust_num} out of range'

        # old_allocated = self.__allocated.copy()

        if len(request_count) == 0:
            # request all of its needs
            self.__allocated[cust_num] += self.__needs[cust_num]
        else:
            assert len(request_count) == self.__num_resources, f'request_resources: invalid size for release_count={request_count}'
            
            request_count = np.array(request_count)
            needs = self.__needs[cust_num]
            if not np.all(request_count <= needs):
                request_count = needs
            self.__allocated[cust_num] += request_count
        self.__update_dependents()

        # iters, isSafe = start_banker(self.copy())
        # for iter in iters:
        #     print(iter)
        #     print_iteration(iter)
        # if not isSafe:
        #     print(f'NOT SAFE!')
        #     self.__allocated = old_allocated
        #     self.__update_dependents()
        #     return -1
        # return 0

    """ 
    Getters. 
    Everything returned are native python data types. 
    The returned values are all 'copies' 
    """
    @property
    def num_customers(self):
        return self.__num_customers
    @property
    def num_resources(self):
        return self.__num_resources
    @property
    def total(self):
        return self.__total.tolist()
    @property
    def allocated_total(self):
        return self.__allocated_total.tolist()
    @property
    def available(self):
        return self.__available.tolist()
    @property
    def maximum(self):
        return self.__maximum.tolist()
    @property
    def allocated(self):
        return self.__allocated.tolist()
    @property
    def needs(self):
        return self.__needs.tolist()

    
    def __update_dependents(self):
        """
        needs = maximum - allocated
        allocated_total = sum over columns of allocated array
        available = total - allocated total
        """
        self.__needs = self.__maximum - self.__allocated
        self.__allocated_total = self.__allocated.sum(axis=0)
        self.__available = self.__total - self.__allocated_total
