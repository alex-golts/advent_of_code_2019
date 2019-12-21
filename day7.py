f = open('input7.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

from itertools import permutations 
l = list(permutations(range(0, 5))) 
    
# intcode computer function - from Day 5 with small change 
# to account for two input values
def intcode_computer(input_val1, input_val2, program):
    halt = False
    firstInputUsed = False
    cnt = 0
    output_vals = []
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            pointer_increase = 2
            if not firstInputUsed:
                program[program[cnt+1]] = input_val1
                firstInputUsed=True
            else:
                program[program[cnt+1]] = input_val2
            
            
        elif optcode%10 == 4:
            pointer_increase = 2
            if str(optcode).zfill(2)[0]=='1':
                # immediate mode
                output_vals.append(program[cnt+1])
            else:
                # parameter mode
                output_vals.append(program[program[cnt+1]])
            
        elif optcode%10 in (1, 2):
            pointer_increase = 4
            if str(optcode).zfill(4)[1]=='0':
                first = program[program[cnt+1]]
            else:
                first = program[cnt+1]
            
            if str(optcode).zfill(4)[0]=='0':
                second = program[program[cnt+2]]
            else:
                second = program[cnt+2]
            
            if optcode%10 == 1:
                program[program[cnt+3]] = first + second
            else:
                program[program[cnt+3]] = first*second
    
        # part 2:    
        elif optcode%10 in (5, 6, 7, 8):
            if str(optcode).zfill(4)[1]=='0':
                first = program[program[cnt+1]]
            else:
                first = program[cnt+1]
            if str(optcode).zfill(4)[0]=='0':
                second = program[program[cnt+2]]
            else:
                second = program[cnt+2]
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
                    program[program[cnt+3]] = 1
                else:
                    program[program[cnt+3]] = 0
            else:
                if first == second:
                    program[program[cnt+3]] = 1
                else:
                    program[program[cnt+3]] = 0
        
        elif optcode == 99:
            halt = True
            
        else:
            print('Bad opt code')
            break
        cnt += pointer_increase
    
    return output_vals[0]


out_max = 0
for p in l:
    out = intcode_computer(int(p[0]), 0, puzzle_input)
    out = intcode_computer(int(p[1]), out, puzzle_input)
    out = intcode_computer(int(p[2]), out, puzzle_input)
    out = intcode_computer(int(p[3]), out, puzzle_input)
    out = intcode_computer(int(p[4]), out, puzzle_input)
    
    if out>out_max:
        out_max = out
print(out_max)