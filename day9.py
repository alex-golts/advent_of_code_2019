
# intcode computer function - from Day 5 but modified 
# to account for new relative parameter mode and
# large program memory
def intcode_computer(input_val, program):
    halt = False
    cnt = 0
    output_vals = []
    relative_base = 0
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
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


f = open('input9.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

# part 1:
output, program = intcode_computer(1, puzzle_input)
print('part 1 output = ' + str(output))

# part 2:
output, program = intcode_computer(2, puzzle_input)
print('part 2 output = ' + str(output))