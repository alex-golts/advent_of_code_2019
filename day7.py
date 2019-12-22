f = open('input7.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

from itertools import permutations 
l = list(permutations(range(0, 5))) 
    
# intcode computer function - from Day 5 with small change 
# to account for two input values
def intcode_computer(input_val1, input_val2, program, \
                     feedback_mode=False, cnt=0, \
                         firstInputUsed=False):
    halt = False
    #firstInputUsed = False
    secondInputUsed = False
    #cnt = 0
    output_vals = []
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            pointer_increase = 2
            if not firstInputUsed:
                program[program[cnt+1]] = input_val1
                firstInputUsed = True
            else:
                program[program[cnt+1]] = input_val2
                secondInputUsed = True
            
        elif optcode%10 == 4:
            pointer_increase = 2
            if str(optcode).zfill(2)[0]=='1':
                # immediate mode
                output_vals.append(program[cnt+1])
            else:
                # parameter mode
                output_vals.append(program[program[cnt+1]])
            #if secondInputUsed:
            return output_vals[0], cnt+pointer_increase, program, halt
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
            output_vals.append(input_val2) # dummy return value
            pointer_increase=0
        else:
            print('Bad opt code')
            break
        cnt += pointer_increase
    return output_vals[0], cnt, program, halt


out_max = 0
for p in l:
    out, _, _, _ = intcode_computer(int(p[0]), 0, puzzle_input, feedback_mode=False, cnt=0)
    out, _, _, _ = intcode_computer(int(p[1]), out, puzzle_input, feedback_mode=False, cnt=0)
    out, _, _, _ = intcode_computer(int(p[2]), out, puzzle_input, feedback_mode=False, cnt=0)
    out, _, _, _ = intcode_computer(int(p[3]), out, puzzle_input, feedback_mode=False, cnt=0)
    out, _, _, _ = intcode_computer(int(p[4]), out, puzzle_input, feedback_mode=False, cnt=0)
    
    if out>out_max:
        out_max = out
print('part 1 result = ' + str(out_max))

# part 2:
l = list(permutations(range(5, 10)))

out_max = 0

for p in l:
    out = 0
    cnt1 = cnt2 = cnt3 = cnt4 = cnt5 = 0
    prog1 = prog2 = prog3 = prog4 = prog5 = puzzle_input.copy()
    firstInputUsed = False
    halt = False
    while not halt:
        out, cnt1, prog1, halt = intcode_computer(int(p[0]), out, prog1, feedback_mode=True, cnt=cnt1, firstInputUsed=firstInputUsed)
        if halt:
            continue
        out, cnt2, prog2, halt = intcode_computer(int(p[1]), out, prog2, feedback_mode=True, cnt=cnt2, firstInputUsed=firstInputUsed)
        out, cnt3, prog3, halt = intcode_computer(int(p[2]), out, prog3, feedback_mode=True, cnt=cnt3, firstInputUsed=firstInputUsed)
        out, cnt4, prog4, halt = intcode_computer(int(p[3]), out, prog4, feedback_mode=True, cnt=cnt4, firstInputUsed=firstInputUsed)
        out, cnt5, prog5, halt = intcode_computer(int(p[4]), out, prog5, feedback_mode=True, cnt=cnt5, firstInputUsed=firstInputUsed)        
        firstInputUsed = True
    if out>out_max:
        out_max=out
print('part 2 result = ' + str(out_max))