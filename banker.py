from copy import deepcopy

"""
An iteration of banker's algorithm. Contains:
    - the state of resources after the iteration
    - boolean flags indicating which customers have had their requests done
    - the possible customer requests grantable in that iteration.
        This implementation always grants the 1st possible request found regardless
        if there other options
    - a boolean indicating whether the algorithm is done and thus, there is no need
        to iterate. True if there are no grantable requests remaining.
The state is safe if and only if all the customer requests were granted.
"""
class BankerIteration:
    def __init__(self, num, state):
        self.num = num
        self.state = state.copy()
        self.customer_done = [False] * state.num_customers
        self.possible_requests = None
        self.isDone = False
    def copy(self):
        iter_copy = BankerIteration(self.num, self.state)
        iter_copy.customer_done = deepcopy(self.customer_done)
        iter_copy.possible_requests = deepcopy(self.possible_requests)
        iter_copy.isDone = deepcopy(self.isDone)
        return iter_copy
    def __str__(self):
        return f'iter={self.num} requests={self.possible_requests} isDone={self.isDone}'

def get_possible_requests(iter):
    state = iter.state
    needs = state.needs
    available = state.available

    # loop through needs
    possible_requests = []
    for i in range(0, state.num_customers):
        # skip if customer was already done
        if iter.customer_done[i]:
            continue
        
        # check if available resources can accomodate needs
        if all([need <= available for (need, available) in zip(needs[i], available)]):
            possible_requests.append(i)

    return possible_requests

"""
Takes an iteration and returns the next iteration of banker's algorithm
"""
def run_banker_iteration(iter):
    iter = iter.copy() # create a copy so as not to modify the past iteration

    iter.num += 1
    iter.possible_requests = get_possible_requests(iter)

    # do 1st request if there is one
    if len(iter.possible_requests) > 0:
        customer = iter.possible_requests[0]
        iter.state.release_resources(customer)
        iter.customer_done[customer] = True

        if all(iter.customer_done):
            iter.isDone = True
    else:
        # no doable requests
        iter.isDone = True

    return iter

"""
Run Banker's Algorithm on the given state
Returns a tuple where:
    tuple[0] = the list of iterations
    tuple[1] = a boolean indicating whether the state was in a safe state
"""
def start_banker(state):
    # list of iterations
    iters = [BankerIteration(0, state)]

    # while last iteration is not done
    # run algorithm on last iteration and append it to the list
    while not iters[-1].isDone:
        iters.append(run_banker_iteration(iters[-1]))
    
    return (
        iters, 
        all(iters[-1].customer_done),   # are all customers done in last iteration?
    )
