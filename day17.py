import numpy as np
from scipy.ndimage.filters import convolve
from copy import deepcopy

def ascii2str(lst):
    res = ''
    for item in lst:
        res += chr(item)
    return res

# intcode computer function - from Day 9 
def intcode_computer(input_command, program):
    halt = False
    cnt = 0
    output_vals = []
    relative_base = 0
    cnt_inputs=0
    while halt == False:
        optcode = program[cnt]
        if optcode%10 == 3:
            pointer_increase = 2
            input_val = input_command[cnt_inputs]
            if str(optcode).zfill(2)[0] == '2':
                program[program[cnt+1] + relative_base] = input_val
            else:
                program[program[cnt+1]] = input_val
            cnt_inputs+=1
            #print(cnt_inputs)
            
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

def draw_map(prog):
    out_map = []
    cur_line = ''
    for item in prog:

        if item == 35:
            cur_line += '#'
        elif item == 46:
            cur_line += '.'
        elif item == 60:
            cur_line += '<'
        elif item == 62:
            cur_line += '>'
        elif item == 94:
            cur_line += '^'
        elif item == 118:
            cur_line += 'v'
        elif item == 10:
            out_map.append(cur_line)
            cur_line = ''
        else:
            pass
    return out_map[:-1]

def map2img(out_map):
    img = np.zeros((len(out_map), len(out_map[0])))
    for i in range(len(out_map)):
        for j in range(len(out_map[0])):
            if out_map[i][j] == '#':
                img[i,j] = 1
            else:
                img[i,j] = 0
    return img

        

f = open('input17.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
puzzle_input = [int(a) for a in txt]

# increase memory:
puzzle_input += [0 for i in range(100000)]

# part 1:
output, program = intcode_computer([1], deepcopy(puzzle_input))
#print('part 1 output = ' + str(output))

out_map = draw_map(output)

# debug example - from question:

# out_map = ['..#..........',
#            '..#..........',
#            '#######...###',
#            '#.#...#...#.#',
#            '#############',
#            '..#...#...#..',
#            '..#####...^..']

bin_img = map2img(out_map)

# find intersections using filtering:
filt = np.array([[0, 1, 0],
                 [1, 1, 1],
                 [0,1, 0]])
filt = filt/np.sum(filt)
out_img = convolve(bin_img, filt)

xx,yy = np.where(out_img==1)

print('part 1 answer = ' + str(np.sum(xx*yy)))

# part 2:
puzzle_input[0]=2

def str2ascii(cmd):
    res = []
    for c in cmd:
        res.append(ord(c))
    return res

# I solved it manually by drawing the full path and discovering repeating patterns
# probably not as intended but this was my last puzzle and I'm tired...

full_path = 'L,12,R,4,R,4,R,12,R,4,L,12,R,12,R,4,L,12,R,12,R,4,L,6,L,8,L,8,R,12,R,4,L,6,L,8,L,8,L,12,R,4,R,4,L,12,R,4,R,4,R,12,R,4,L,12,R,12,R,4,L,12,R,12,R,4,L,6,L,8,L,8'

main_prog = 'A,B,B,C,C,A,A,B,B,C\n'
A_func = 'L,12,R,4,R,4\n'
B_func = 'R,12,R,4,L,12\n'
C_func = 'R,12,R,4,L,6,L,8,L,8\n'
yes_no = 'n\n'

cmd = main_prog + A_func + B_func + C_func + yes_no

inp = str2ascii(cmd)

output, program = intcode_computer(inp, deepcopy(puzzle_input))

print(f'part 2 answer = {output[-1]}')