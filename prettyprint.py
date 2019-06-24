
import subprocess, platform, os

from terminaltables import SingleTable
from colorama import Fore, Back, Style


table = SingleTable([])

def init_pretty_print(num_resources):
    if platform.system() == 'Windows':
        os.system('color')
    table.inner_heading_row_border = False
    table.inner_column_border = False
    table.inner_row_border = False
    table.padding_left = 2
    table.padding_right = 2
    for i in range(0, num_resources):
        table.justify_columns[i] = 'center'

def array_to_table(props):
    array, title = props
    # if array is 1 dimensional, wrap it inside another array
    if (not hasattr(array[0], "__len__")):
        array = [array] 
    # elif (hasattr(array[0][0], "__len__")):
    #     array = array.tolist() # printer knows about numpy! not good
    # else:
    #     array = array.tolist()
    #     print(f'{type(array)}')

    # print(type(array))
    table.table_data = array
    table.title = f'> {title} '
    return table.table

def print_tables(tables):
    # print(f'pt{type((tables)[0])}')
    tables = map(array_to_table, tables)

    
    # print(type(tables))
    
    splits = [table.split('\n') for table in tables]
    for i in range(0, len(splits[0])):
        str = '      '
        for x in splits:
            str += x[i] + '  '
            # print(x[i].split(' '))
        print(str)

import copy
def print_system_state(system):
    print('\n\n    Current state:\n')
    # print(f'sys{system}')
    # print(f'systotal{type(system.total)}')
    # system = system.clone()
    print_tables([
        [system.total, 'total'],
        [system.allocated_total, 'alloc_total'],
        [system.available, 'available'],
    ])

    needs = system.needs
    # print(f'{type(needs)}')
    # needs = needs.tolist()
    # print(f'sneed{type(system.needs)}')
    # print(f'need{type(needs)}')
    for c in range(0, system.num_customers):
        if all([x == 0 for x in needs[c]]):
            for r in range(0, system.num_resources):
                needs[c][r] = Fore.YELLOW+str('-')+Style.RESET_ALL

        else:
            all_green = True
            for r in range(0, system.num_resources):
                if needs[c][r] > system.available[r]:
                    needs[c][r] = Style.BRIGHT+Fore.RED+str(needs[c][r])+Style.RESET_ALL
                    all_green = False
                    # break
            if all_green:
                for r in range(0, system.num_resources):
                    needs[c][r] = Style.BRIGHT+Fore.GREEN+str(needs[c][r])+Style.RESET_ALL

    print_tables([
        [system.maximum, 'maximum'],
        [system.allocated, 'allocated'],
        [needs, 'needs'],
    ])


def print_iteration(iter, prevIter=None):
    # if iter.num == 0:
    #     return
    state = iter.state
    msg = f'\n{Fore.YELLOW}  >> ITER {iter.num}'
    if iter.num != 0:
        if len(iter.possible_requests):
            msg += f' {Fore.WHITE}granting {Style.BRIGHT+Fore.GREEN}request {iter.possible_requests[0]}'
        else:
            msg += f' {Style.BRIGHT+Fore.RED} No grantable requests remaining'
    msg += f'{Style.RESET_ALL}\n'
    print(msg)

    
    
    maximum = state.maximum
    allocated = state.allocated
    needs = state.needs
    for c in range(0, state.num_customers):
        if iter.customer_done[c]:
            for r in range(0, state.num_resources):
                needs[c][r] = Fore.YELLOW+str('-')+Style.RESET_ALL
            maximum[c] = needs[c]
            allocated[c] = needs[c]
        else:
            all_green = True
            for r in range(0, state.num_resources):
                if needs[c][r] > state.available[r]:
                    needs[c][r] = Style.BRIGHT+Fore.RED+str(needs[c][r])+Style.RESET_ALL
                    all_green = False
                    # break
            if all_green:
                for r in range(0, state.num_resources):
                    needs[c][r] = Style.BRIGHT+Fore.GREEN+str(needs[c][r])+Style.RESET_ALL
    print_tables([
        [state.allocated_total, 'alloc_total'],
        [state.available, 'available'],
    ])
    print_tables([
        # [maximum, 'maximum'],
        [allocated, 'allocated'],
        [needs, 'needs'],
    ])


    

def print_banker_iterations(iterations):
    print(f'\n\n{Style.BRIGHT+Fore.BLUE}  Banker\'s algorithm{Style.RESET_ALL}')
    # print(f'\n{Style.BRIGHT+Fore.BLUE}--------------------------------------{Style.RESET_ALL}')
    for i in range(len(iterations)):
        if i == 0:
            print_iteration(iterations[i])
        else:
            print_iteration(iterations[i], iterations[i-1])
    if all(iterations[-1].customer_done):
        print(f'\n     All customer requests were granted')
        print(f'{Fore.YELLOW}  >> Initial state {Fore.WHITE}was {Style.BRIGHT+Fore.GREEN}SAFE!{Style.RESET_ALL}')
    else:
        print(f'\n     Some customer requests can\'t be done')
        print(f'{Fore.YELLOW}  >> Initial state {Fore.WHITE}was {Style.BRIGHT+Fore.RED}NOT SAFE!{Style.RESET_ALL}')
    print(f'{Style.BRIGHT+Fore.BLUE}  ------------------------------------------{Style.RESET_ALL}')

def clear_screen():
    if platform.system()=="Windows":
        subprocess.Popen("cls", shell=True).communicate() #I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine 
    else: #Linux and Mac
        print("\033c", end="")
