# intcode computer function - from Day 25
# but modified for springscript
import random
import numpy as np
from copy import deepcopy
def intcode_computer(input_commands, program):
    halt = False
    cnt = 0
    output_vals = []
    relative_base = 0
    cntInputs = 0
    cntInputCommands = 0
    itemListAhead = False
    sensitiveFloorAhead = False
    cntPickedItems = 0
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            input_val = input_commands[cntInputCommands][cntInputs]
            pointer_increase = 2
            if str(optcode).zfill(2)[0] == '2':
                program[program[cnt+1] + relative_base] = input_val
            else:
                program[program[cnt+1]] = input_val
            cntInputs += 1
            if input_val == 10:
                print('Input command: ' + ascii2str(input_commands[cntInputCommands]))
                cntInputCommands += 1 
                cntInputs = 0
                if cntInputCommands >= len(input_commands):
                    input_commands = []
                    cntInputCommands = 0
        elif optcode%10 == 4:
            pointer_increase = 2
            if str(optcode).zfill(2)[0]=='1':
                # immediate mode
                output_vals.append(program[cnt+1])
            elif str(optcode).zfill(2)[0]=='0':
                # parameter mode
                output_vals.append(program[program[cnt+1]])
            elif str(optcode).zfill(2)[0]=='2': 
                # relative mode
                #output_vals.append(program[cnt+1] + relative_base)
                output_vals.append(program[program[cnt+1] + relative_base])
            else:
                print('bad mode ' + str(optcode).zfill(2)[0])
            if output_vals[-1]==10:
                print(ascii2str(output_vals))


                output_vals = []
        elif optcode%10 in (1, 2):
            pointer_increase = 4
            if str(optcode).zfill(5)[2]=='0':
                first = program[program[cnt+1]]
            elif str(optcode).zfill(5)[2]=='1':
                first = program[cnt+1]
            elif str(optcode).zfill(5)[2]=='2':
                # relative mode
                first = program[program[cnt+1] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[1])
            if str(optcode).zfill(5)[1]=='0':
                second = program[program[cnt+2]]
            elif str(optcode).zfill(5)[1]=='1':
                second = program[cnt+2]
            elif str(optcode).zfill(5)[1]=='2':
                # relative mode
                second = program[program[cnt+2] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[0])
            if optcode%10 == 1:
                if str(optcode).zfill(5)[0]=='2':
                    program[program[cnt+3] + relative_base] = first+second
                else:
                    program[program[cnt+3]] = first + second
            else:
                if str(optcode).zfill(5)[0]=='2':
                    program[program[cnt+3] + relative_base] = first*second
                else:
                    program[program[cnt+3]] = first*second
    
        # part 2:    
        elif optcode%10 in (5, 6, 7, 8):
            if str(optcode).zfill(5)[2]=='0':
                first = program[program[cnt+1]]
            elif str(optcode).zfill(5)[2]=='1':
                first = program[cnt+1]
            elif str(optcode).zfill(5)[2]=='2':
                first = program[program[cnt+1] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[1])
            if str(optcode).zfill(5)[1]=='0':
                second = program[program[cnt+2]]
            elif str(optcode).zfill(5)[1]=='1':
                second = program[cnt+2]
            elif str(optcode).zfill(5)[1]=='2':
                second = program[program[cnt+2] + relative_base]
            else:
                print('bad mode ' + str(optcode).zfill(4)[0])
            if optcode%10 == 5:
                if first!=0:
                    cnt = second
                    continue
                else:
                    pointer_increase = 3
            elif optcode%10 == 6:
                if first==0:
                    cnt = second
                    continue
                else:
                    pointer_increase = 3
            elif optcode%10 == 7:
                pointer_increase = 4
                if first<second:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 1
                    else:
                        program[program[cnt+3]] = 1
                else:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 0
                    else:
                        program[program[cnt+3]] = 0
            else:
                pointer_increase = 4
                if first == second:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 1
                    else:
                        program[program[cnt+3]] = 1
                else:
                    if str(optcode).zfill(5)[0]=='2':
                        program[program[cnt+3] + relative_base] = 0
                    else:   
                        program[program[cnt+3]] = 0
        
        elif optcode%10==9 and optcode !=99:
            
            #relative_base += program[cnt+1]
            pointer_increase = 2
            
            if str(optcode).zfill(2)[0] == '2':
                relative_base += program[program[cnt+1] + relative_base]
            elif str(optcode).zfill(2)[0] == '1':
                relative_base += program[cnt+1]
            else:
                relative_base += program[program[cnt+1]]
            
            
        elif optcode == 99:
            halt = True
            
        else:
            print('Bad opt code ' + str(optcode) + \
                  ' at position ' + str(cnt))
            break
        cnt += pointer_increase
    return output_vals, program

def ascii2str(lst):
    res = ''
    for item in lst:
        res += chr(item)
    return res
def str2ascii(cmd):
    res = []
    for c in cmd:
        res.append(ord(c))
    res.append(10) # end with newline char
    return res

f = open('input21.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

# part 1 

def gen_random_cmd():
    readable_reg = ['A', 'B', 'C', 'D']
    writeable_reg = ['T', 'J']
    instructions = ['NOT', 'OR', 'AND']
    
    
    cmd_list = []
    for i in range(4):
        inst = np.random.choice(instructions)
        first_reg = np.random.choice(readable_reg + writeable_reg)
        second_reg = np.random.choice(writeable_reg)
        cmd_list.append(inst + ' ' + first_reg + ' '+ second_reg)
    cmd_list.append('WALK')
    return cmd_list


# exhaustive search for 4 command sequences:
def exhaustive_search():
    readable_reg = ['A', 'B', 'C', 'D']
    writeable_reg = ['T', 'J']
    instructions = ['NOT', 'OR', 'AND']
    total_runs = (len(instructions)**4)*((len(readable_reg)+len(writeable_reg))**4)*(len(writeable_reg)**4)
    cnt=0
    for c1 in instructions:
        for c1in1 in readable_reg+writeable_reg:
            for c1in2 in writeable_reg:
                
                for c2 in instructions:
                    for c2in1 in readable_reg+writeable_reg:
                        for c2in2 in writeable_reg:
                            
                            for c3 in instructions:
                                for c3in1 in readable_reg+writeable_reg:
                                    for c3in2 in writeable_reg:
                                        
                                        for c4 in instructions:
                                            for c4in1 in readable_reg+writeable_reg:
                                                for c4in2 in writeable_reg:
                                                    cnt+=1
                                                    prog = puzzle_input.copy()
                                                    #prog = deepcopy(puzzle_input)
                                                    cmd_list = [c1 + ' ' + c1in1 + ' ' + c1in2, c2 + ' ' + c2in1 + ' ' + c2in2, c3 + ' ' + c3in1 + ' ' + c3in2, c4 + ' ' + c4in1 + ' ' + c4in2, 'WALK']
                                                    output, program = intcode_computer([str2ascii(item) for item in cmd_list], prog)
                                                    print(str(cnt) + '/' + str(total_runs))
                                                    if len(output)>0:                    
                                                        print('***** DONE *****')
                                                        print(str(output[0]))
                                                        return output[0]
                                            
part1answer = exhaustive_search()
