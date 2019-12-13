import numpy as np

f = open('input5.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]
puzzle_output = puzzle_input.copy()

 
#input_val = 1
input_val = 5
halt = False
cnt = 0
output_vals = []
while halt == False:
    optcode = puzzle_output[cnt]
    if optcode%10 == 3:
        pointer_increase = 2
        puzzle_output[puzzle_output[cnt+1]] = input_val
        
    elif optcode%10 == 4:
        pointer_increase = 2
        if str(optcode).zfill(2)[0]=='1':
            # immediate mode
            output_vals.append(puzzle_output[cnt+1])
        else:
            # parameter mode
            output_vals.append(puzzle_output[puzzle_output[cnt+1]])
        
    elif optcode%10 in (1, 2):
        pointer_increase = 4
        if str(optcode).zfill(4)[1]=='0':
            first = puzzle_output[puzzle_output[cnt+1]]
        else:
            first = puzzle_output[cnt+1]
        
        if str(optcode).zfill(4)[0]=='0':
            second = puzzle_output[puzzle_output[cnt+2]]
        else:
            second = puzzle_output[cnt+2]
        
        if optcode%10 == 1:
            puzzle_output[puzzle_output[cnt+3]] = first + second
        else:
            puzzle_output[puzzle_output[cnt+3]] = first*second

    # part 2:    
    elif optcode%10 in (5, 6, 7, 8):
        if str(optcode).zfill(4)[1]=='0':
            first = puzzle_output[puzzle_output[cnt+1]]
        else:
            first = puzzle_output[cnt+1]
        if str(optcode).zfill(4)[0]=='0':
            second = puzzle_output[puzzle_output[cnt+2]]
        else:
            second = puzzle_output[cnt+2]
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
            if first<second:
                puzzle_output[puzzle_output[cnt+3]] = 1
            else:
                puzzle_output[puzzle_output[cnt+3]] = 0
        else:
            if first == second:
                puzzle_output[puzzle_output[cnt+3]] = 1
            else:
                puzzle_output[puzzle_output[cnt+3]] = 0
    
    elif optcode == 99:
        halt = True
        
    else:
        print('Bad opt code')
        break
    cnt += pointer_increase
print(output_vals)