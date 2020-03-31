import numpy as np
from copy import deepcopy
# intcode computer function - from Day 9 but modified 
# to account for two inputs
def intcode_computer(input_val1, input_val2, program):
    halt = False
    cnt = 0
    output_vals = []
    relative_base = 0
    cntInputs = 0
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            pointer_increase = 2
            if cntInputs==0:
                input_val = input_val1
            else:
                input_val = input_val2
            cntInputs += 1 
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
f = open('input19.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

# part 1
if False:
    im = np.zeros((50,50))
    # slow...
    for i in range(50):
        for j in range(50):
            print(i,j)
            inp_prog = deepcopy(puzzle_input)
            output, _ = intcode_computer(j, i, inp_prog)
            im[i, j] = output[0]
     
    print('part 1 answer = ' + str(int(np.sum(im==1))))


# part 2:

# for each row, use binary search to efficiently find the first occupied column
# found manually that 1000 is a "good" row to start the search and go up


# My modification based on binary search implementation - from https://www.geeksforgeeks.org/python-program-for-binary-search/
def binarySearchMod(func, l, r, const): 
  
    # Check base case 
    if r >= l: 
  
        mid = l + (r - l)//2
  
        # If element is present at the middle itself 
        if func(mid, const)==1: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif func(mid, const) > 1: 
            return binarySearchMod(func, l, mid-1, const) 
  
        # Else the element can only be present in right subarray 
        else: 
            return binarySearchMod(func, mid+1, r, const) 
  
    else: 
        # Element is not present in the array 
        return -1

def checkFirstCol(col, row):
    # check if current col is the first column that is occupied
    # in a given row. This is the objective function for the binary search
    inp_prog = deepcopy(puzzle_input)
    output1, _ = intcode_computer(col, row, inp_prog)
    inp_prog = deepcopy(puzzle_input)
    output2, _ = intcode_computer(col-1, row, inp_prog)
    return output1[0]+output2[0]


start_line = 1000
success = False

cnt=0
while not success:
    row=start_line+cnt
    print(f'row={row}')
    
    col = binarySearchMod(checkFirstCol, row//2, row, row)

    # check top-right corner:
    inp_prog = deepcopy(puzzle_input)
    output1, _ = intcode_computer(col+100-1, row-100+1, inp_prog)
    
    inp_prog = deepcopy(puzzle_input)
    output2, _ = intcode_computer(col+100, row-100+1, inp_prog)
    
    print(f'col={col}, test sum = {output1[0]+output2[0]}')
    if output1[0]+output2[0]==1:
        print('Success')
        success = True
        print(f'x={col},y={row-100+1}')
        print(f'part 2 answer={col*10000+row-100+1}')
        break
    cnt+=1
    


    
