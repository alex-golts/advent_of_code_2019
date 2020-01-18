import numpy as np

pos = np.array(([-2,9,-5], [16,19,9], [0,3,6], [11,0,11])).astype('float32')
vel = np.zeros((4, 3)).astype('float32')

pos_start = pos.copy()
vel_start = vel.copy()

for i in range(1000):
    # apply gravity
    for k in range(len(pos)):
        for l in range(len(pos)):
            if k == l:
                continue
            vel[k] += -1*(pos[k]>pos[l]) +1*(pos[k]<pos[l])
    # apply velocity
    for k in range(len(pos)):
        pos[k] += vel[k]

total_energy = int(np.sum(np.sum(np.abs(vel), 1) * np.sum(np.abs(pos), 1), 0))
print('part 1 answer = ' + str(total_energy))

# Part 2:

# x,y,z are independent, so find when each of them satisfies 
# condition, and then find the least common multiple

pos = pos_start.copy()
vel = vel_start.copy()
stop_iter = np.zeros(3).astype('int')
cnt = 0
while True:
    cnt+=1
    # apply gravity
    for k in range(len(pos)):
        for l in range(len(pos)):
            if k == l:
                continue
            vel[k] += -1*(pos[k]>pos[l]) +1*(pos[k]<pos[l])
    # apply velocity
    for k in range(len(pos)):
        pos[k] += vel[k]
     
    if stop_iter[0]==0 and np.array_equal(pos[:,0], pos_start[:,0]) and np.array_equal(vel[:,0], vel_start[:,0]):
        stop_iter[0] = cnt
    if stop_iter[1]==0 and np.array_equal(pos[:,1], pos_start[:,1]) and np.array_equal(vel[:,1], vel_start[:,1]):
        stop_iter[1] = cnt
    if stop_iter[2]==0 and np.array_equal(pos[:,2], pos_start[:,2]) and np.array_equal(vel[:,2], vel_start[:,2]):
        stop_iter[2] = cnt

    if stop_iter.all():
         break
     
print('part 2 answer = ' + str(np.lcm.reduce(stop_iter.tolist())))

