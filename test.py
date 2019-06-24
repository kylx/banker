import argparse

import numpy as np

from state import State
from banker import start_banker
from prettyprint import print_system_state, init_pretty_print, print_banker_iterations, clear_screen


parser = argparse.ArgumentParser()
parser.add_argument('total', type=int, nargs='+')
total = parser.parse_args().total




allocated = [
    [1, 2, 2, 1],
    [1, 0, 3, 3],
    [1, 2, 1, 0],
]
# allocated = [[0]*4]*3
state = State.create_from_file('max.txt', total, allocated)
init_pretty_print(state.num_resources)
# state.set_total_resources(total)

print(f'\n  State info:')
print(f'    - num_costumers    = {state.num_customers}')
print(f'    - num_resources    = {state.num_resources}')
print(f'    - total_resources  = {str(state.total)}')

banker = None
past_cmd = None
past_result = None
past_iterations = None
past_state = False
show_past_iterations = False

# (iters, isSafe) = start_banker(state)

# TODO: print command/input

while True:
    clear_screen()

    if past_iterations is not None:
        print_system_state
        print_banker_iterations(past_iterations)

    print_system_state(state)
    print()
    if past_cmd:
        print(f'    previous_command = {past_cmd}')
        print(f'    result = {past_result}')
    else:
        print()
    cmd = input("\n\n            Enter command >> ")
    if cmd == 'exit':
        break;


    if cmd == 'show past iterations':
        show_past_iterations = True
    else:
        tokens = cmd.split(' ')
        print(tokens)
        type = tokens[0]
        cust_num = int(tokens[1])
        array = [int(x) for x in tokens[2:]]
        # print(f'type={type}')
        # print(f'cust_num={cust_num}')
        # print(f'array={array}')

        if type == 'rq':
            past_state = state_copy = state.copy()
            state_copy.request_resources(cust_num, array)
            past_iterations, past_state_safe = start_banker(state_copy)
            if past_state_safe:
                state = state_copy
                past_result = 'request granted'
            else:
                past_result = 'request denied'
            past_cmd = cmd
        if type == 'rl':
            state.release_resources(cust_num, array)
            past_result = 'resources deallocated'

    

    
# for iter in iters:
#     print(iter)
#     print_iteration(iter)
# print(f'isSafe? {isSafe}')


print(Style.RESET_ALL)


    