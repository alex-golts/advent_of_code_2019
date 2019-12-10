import numpy as np

# day 1

def calc_module_fuel(module_weight):
    total = module_weight
    cur = module_weight
    while True:
        cur = int(np.floor(cur/3)-2)
        if cur<=0:
            break
        total+=cur
    return total

# part 1:
    
f=open('input1.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]
total = sum([int(np.floor(int(item)/3)-2) for item in txt])

# part 2:

total_with_fuel = sum([calc_module_fuel(int(np.floor(int(item)/3)-2)) for item in txt])


# day 2

# part 1:
f=open('input2.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[0].split(',')
nums = [int(item) for item in txt]


nums[1]=12
nums[2]=2

for i in range(0, len(nums), 4):
    if nums[i]==99:
        break
    if nums[i]==1:
        nums[nums[i+3]] = nums[nums[i+1]]+nums[nums[i+2]]
    if nums[i]==2:
        nums[nums[i+3]] = nums[nums[i+1]]*nums[nums[i+2]]
    

# part 2:

for noun in range(100):
    for verb in range(100):
        nums = [int(item) for item in txt]
        nums[1] = noun
        nums[2] = verb
        for i in range(0, len(nums), 4):
            if nums[i]==99:
                break
            if nums[i]==1:
                nums[nums[i+3]] = nums[nums[i+1]]+nums[nums[i+2]]
            if nums[i]==2:
                nums[nums[i+3]] = nums[nums[i+1]]*nums[nums[i+2]]
        if nums[0]==19690720:
            print('noun=' + str(noun))
            print('verb=' + str(verb))
            break
        
        
# day 3:
            
# part 1:

def calc_wire_path(wire):
    path = [(0,0)] # x,y convention
    for item in wire:
        if item[0] == 'L':
            path.append((path[-1][0]-int(item[1:]), path[-1][1]))
        elif item[0] == 'R':
            path.append((path[-1][0]+int(item[1:]), path[-1][1]))
        elif item[0] == 'U':
            path.append((path[-1][0], path[-1][1]+int(item[1:])))
        elif item[0] == 'D':
            path.append((path[-1][0], path[-1][1]-int(item[1:])))
        
    return path  

f=open('input3.txt','r')
txt=f.read()
txt = txt.split('\n')
txt=txt[:-1]
wire1 = txt[0].split(',')
wire2 = txt[1].split(',')

wire1_path = calc_wire_path(wire1)
wire2_path = calc_wire_path(wire2)

inter_points = calc_inter_points(wire1_path, wire2_path)
min_dist = closest_point(inter_points)