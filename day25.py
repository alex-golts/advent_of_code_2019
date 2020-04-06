# intcode computer function - from Day 9
# but modified to print ascii messages
import random
import numpy as np
def intcode_computer(input_commands, program):
    halt = False
    cnt = 0
    output_vals = []
    relative_base = 0
    cntInputs = 0
    cntInputCommands = 0
    movement_commands = ['north', 'south', 'east', 'west']
    itemListAhead = False
    sensitiveFloorAhead = False
    gotFeedback = False
    pickedAllItems = False
    availableItems = []
    items = []
    goodItems = []
    cntPickedItems = 0
    badItems = ['giant electromagnet', 'molten lava', 'escape pod', 'infinite loop', 'photons']
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            if len(input_commands) == 0: # if no input command, move randomly
                ind = random.randint(0,3)  
                input_commands = [str2ascii(movement_commands[ind])]
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
                if len(goodItems)>=8 and ascii2str(output_vals).startswith('In the next room, a pressure-sensitive'):
                    sensitiveFloorAhead = True
                if sensitiveFloorAhead == True and ascii2str(output_vals).startswith('Command?'):
                    pickedAllItems = True
                    if len(goodItems)==8:
                        if len(availableItems) == 0:
                            # drop all items here
                            input_commands = []
                            for item in goodItems:
                                input_commands.append(str2ascii('drop ' + item))
                                availableItems.append(item)
                        else:
                            # pick up a random item until finished
                            itemToPick = np.random.choice(availableItems, 1)[0]
                            availableItems.remove(itemToPick)
                            cntPickedItems += 1
                            input_commands = [str2ascii('take ' + itemToPick)]
                            if len(availableItems)==0:
                                cntPickedItems = 0
                    sensitiveFloorAhead = False
                if ascii2str(output_vals).startswith('Items here:') and not pickedAllItems:
                    itemListAhead = True
                if itemListAhead and ascii2str(output_vals).startswith('- ') and not pickedAllItems:
                    items.append(ascii2str(output_vals)[2:-1])
                    if items[-1] not in badItems:
                        goodItems.append(items[-1])
                        input_commands = [str2ascii('take ' + goodItems[-1])]
                if itemListAhead and ascii2str(output_vals).startswith('Command?') and not pickedAllItems:
                    itemListAhead = False

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

f = open('input25.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

# part 1 
# this takes a while to finish...
output, program = intcode_computer([], puzzle_input)
