import numpy as np
from matplotlib import pyplot as plt

f = open('input8.txt','r')
txt = f.read()
txt=txt[:-1]

cols = 25
rows = 6
channels = int(len(txt)/rows/cols)
img = np.zeros((rows, cols, channels))
cnt = 0
min_zeros = rows*cols
img_decoded = 5*np.ones((rows,cols)) # for part 2
for ch in range(channels):
    for r in range(rows):
        for c in range(cols):
            img[r, c, ch] = int(txt[cnt])
            # for part 2:
            if img_decoded[r,c]==5 and img[r,c,ch]==1:
                img_decoded[r,c] = 1
            elif img_decoded[r,c]==5 and img[r,c,ch]==0:
                img_decoded[r,c] = 0
            cnt += 1
    cur_zeros = np.sum(img[:,:,ch]==0)
    if cur_zeros<min_zeros:
        min_zeros = cur_zeros
        min_zeros_channel = ch

num_ones = np.sum(img[:,:,min_zeros_channel]==1)
num_twos = np.sum(img[:,:,min_zeros_channel]==2)
print(f'part 1 answer: {num_ones*num_twos}')

# part 2 answer:
plt.figure()
plt.imshow(img_decoded)
plt.show()
    