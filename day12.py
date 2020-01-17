import numpy as np
# input
pos = np.array(([-2,9,-5], [16,19,9], [0,3,6], [11,0,11])).astype('float32')
vel = np.zeros((4, 3)).astype('float32')

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
