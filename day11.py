import numpy as np

# intcode computer function - from Day 9
# with changing input_val according to 
# robot position and grid status
def intcode_computer(input_val, program):
    
    GRID_SIZE = 100
    grid = np.zeros((GRID_SIZE,GRID_SIZE))
    grid_painted = np.zeros((GRID_SIZE,GRID_SIZE))
    
    pos = [int(GRID_SIZE/2), int(GRID_SIZE/2)] # row,col
    orientation = 'up'
    
    halt = False
    cnt = 0
    output_vals = []
    relative_base = 0
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            
            # change input value according to current panel color
            if grid[pos[0], pos[1]] == 0:
                input_val = 0
            else:
                input_val = 1
                    
            pointer_increase = 2
            
            if str(optcode).zfill(2)[0] == '2':
                program[program[cnt+1] + relative_base] = input_val
            else:
                program[program[cnt+1]] = input_val
            
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
            
            # received two outputs - update robot position, panel color and input_val
            if len(output_vals)>=2 and len(output_vals)%2==0:
                    
                if output_vals[-2]==0:
                    grid[pos[0], pos[1]] = 0
                else:
                    grid[pos[0], pos[1]] = 1
                    
                grid_painted[pos[0], pos[1]] = 1
                
                    
                if (output_vals[-1] == 0 and orientation == 'up') or (output_vals[-1] == 1 and orientation == 'down'):
                    pos[1]-=1
                    orientation = 'left'
                elif (output_vals[-1] == 0 and orientation == 'down') or (output_vals[-1] == 1 and orientation == 'up'):
                    pos[1]+=1
                    orientation = 'right'
                elif (output_vals[-1] == 0 and orientation == 'left') or (output_vals[-1] == 1 and orientation == 'right'):
                    pos[0]+=1
                    orientation = 'down'
                elif (output_vals[-1] == 0 and orientation == 'right') or (output_vals[-1] == 1 and orientation == 'left'):
                    pos[0]-=1
                    orientation = 'up'
                
                
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
    return output_vals, program, grid_painted, pos


f = open('input11.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

output, program, grid_painted, pos = intcode_computer(0, puzzle_input)

print('part 1 answer = ' + str(int(np.sum(grid_painted))))