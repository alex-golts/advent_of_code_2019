from copy import deepcopy
# intcode computer function - from Day 9 but modified for networking
def intcode_computer(comp_id, input_vals, program, cnt, packet_queue):
    halt = False
    output_vals = []
    relative_base = 0
    cntInputs = 0
    cntOutputs = 0
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            if cntInputs<len(input_vals):
                input_val = input_vals[cntInputs]
            else:
                if len(packet_queue[comp_id])>0:
                    input_vals = packet_queue[comp_id].pop(0)
                    cntInputs = 0
                    input_val = input_vals[0]
                else:
                    input_val = -1
            cntInputs+=1
            pointer_increase = 2
            if str(optcode).zfill(2)[0] == '2':
                program[program[cnt+1] + relative_base] = input_val
            else:
                program[program[cnt+1]] = input_val
            
        elif optcode%10 == 4:
            cntOutputs+=1
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
        if cntOutputs==3:
            #mode = 'output'
            return output_vals, program, cnt
        
        if cntInputs>0 and input_val==-1:
            return [], program, cnt 
    return output_vals, program

f = open('input23.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

packet_queue = [[] for i in range(50)]

# boot computers:
programs = []
pointers = []

for i in range(50):
    inp_prog = deepcopy(puzzle_input)  
    print('booting computer #' + str(i))
    output, prog, pnt = intcode_computer(i, [i], inp_prog, 0, packet_queue)
    programs.append(prog)
    pointers.append(pnt)
    if len(output)>0:
        packet_queue[output[0]].append(output[1:])

# normal network operation:
success = False
while not success:
    for i in range(50):
        output, prog, pnt = intcode_computer(i, [], programs[i], pointers[i], packet_queue)
        programs[i] = prog
        pointers[i] = pnt
        if len(output)>0:
            print(f'computes #{i} sends packet {str(output[1:])} to computer #{output[0]}.')
            if output[0]==255:
                print(f'part 1 answer = {str(output[2])}')
                success = True
                break
            packet_queue[output[0]].append(output[1:])

    

    