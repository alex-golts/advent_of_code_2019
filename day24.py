import numpy as np
from scipy.ndimage.filters import convolve

f = open('input24.txt','r')
txt = f.read()
txt = txt.split('\n')
txt = txt[:-1]

# example:
#txt = ['....#', '#..#.', '#..##', '..#..', '#....']

def txt2im(txt):
    im = np.zeros((5,5))
    for i in range(5):
        for j in range(5):
            im[i,j] = 1 if txt[i][j]=='#' else 0
    return im

    
def evolve(im):
    im_new = np.zeros_like(im)
    filt = np.array([[0, 1, 0],
                    [1, 0, 1],
                    [0,1, 0]])
    adjacent_count = convolve(im, filt, mode='constant', cval=0)
    
    im_new[im==1] = adjacent_count[im==1]==1 
    im_new[im==0] = np.logical_or(adjacent_count[im==0]==1, adjacent_count[im==0]==2)
    
    return im_new
    
def check_duplicate_ims(im_list, im):
    dup_inds = []
    for i in range(len(im_list)):
        if np.array_equal(im_list[i], im):
            dup_inds.append(i)
    return dup_inds

def calc_biodiversity_rate(im):
    calc = 0
    cnt = 0
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i,j]==1:
                calc += 2**cnt
            cnt+=1
            
    return calc


im = txt2im(txt)

# part 1: 
success = False
cnt = 0
ims = [im]
while not success:
    cnt+=1
    ims.append(evolve(ims[-1]))
    dup_inds = check_duplicate_ims(ims[:-1], ims[-1])
    if len(dup_inds)>0:
        success = True
        dup_im = ims[-1]
        print(f'part 1 answer = {calc_biodiversity_rate(dup_im)}')
    

# part 2:
total_depths = 105
ims = {i:np.zeros_like(im) for i in range(-total_depths, total_depths+1)}
ims[0] = im

def evolve_recursive(ims):
    ims_new = {i:np.zeros_like(ims[0]) for i in range(-total_depths, total_depths+1)}

    filt = np.array([[0, 1, 0],
                    [1, 0, 1],
                    [0,1, 0]])

    for i in range(-total_depths+1, total_depths):
            
        adjacent_count = convolve(ims[i], filt, mode='constant', cval=0)
        # only 4 pixels from this map should be kept. the rest are replaced by:
        adjacent_count[0,0] = ims[i-1][2,1]+ims[i-1][1,2]+ims[i][0,1]+ims[i][1,0]
        adjacent_count[0,1] = ims[i][0,0]+ims[i-1][1,2]+ims[i][0,2]+ims[i][1,1]
        adjacent_count[0,2] = ims[i][0,1]+ims[i-1][1,2]+ims[i][0,3]+ims[i][1,2]
        adjacent_count[0,3] = ims[i][0,2]+ims[i-1][1,2]+ims[i][0,4]+ims[i][1,3]
        adjacent_count[0,4] = ims[i][0,3]+ims[i-1][1,2]+ims[i-1][2,3]+ims[i][1,4]
        adjacent_count[1,0] = ims[i-1][2,1]+ims[i][0,0]+ims[i][1,1]+ims[i][2,0]
        adjacent_count[1,2] = ims[i][1,1]+ims[i][0,2]+ims[i][1,3]+np.sum(ims[i+1][0,:])
        adjacent_count[1,4] = ims[i][1,3]+ims[i][0,4]+ims[i-1][2,3]+ims[i][2,4]
        adjacent_count[2,0] = ims[i-1][2,1]+ims[i][1,0]+ims[i][2,1]+ims[i][3,0]
        adjacent_count[2,1] = ims[i][2,0]+ims[i][1,1]+np.sum(ims[i+1][:,0])+ims[i][3,1]
        adjacent_count[2,2] = 0
        adjacent_count[2,3] = np.sum(ims[i+1][:,4])+ims[i][1,3]+ims[i][2,4]+ims[i][3,3]
        adjacent_count[2,4] = ims[i][2,3]+ims[i][1,4]+ims[i-1][2,3]+ims[i][3,4]
        adjacent_count[3,0] = ims[i-1][2,1]+ims[i][2,0]+ims[i][3,1]+ims[i][4,0]
        adjacent_count[3,2] = ims[i][3,1]+np.sum(ims[i+1][4,:])+ims[i][3,3]+ims[i][4,2]
        adjacent_count[3,4] = ims[i][3,3]+ims[i][2,4]+ims[i-1][2,3]+ims[i][4,4]
        adjacent_count[4,0] = ims[i-1][2,1]+ims[i][3,0]+ims[i][4,1]+ims[i-1][3,2]
        adjacent_count[4,1] = ims[i][4,0]+ims[i][3,1]+ims[i][4,2]+ims[i-1][3,2]
        adjacent_count[4,2] = ims[i][4,1]+ims[i][3,2]+ims[i][4,3]+ims[i-1][3,2]
        adjacent_count[4,3] = ims[i][4,2]+ims[i][3,3]+ims[i][4,4]+ims[i-1][3,2]
        adjacent_count[4,4] = ims[i][4,3]+ims[i][3,4]+ims[i-1][2,3]+ims[i-1][3,2]
        
        ims_new[i][ims[i]==1] = adjacent_count[ims[i]==1]==1 
        ims_new[i][ims[i]==0] = np.logical_or(adjacent_count[ims[i]==0]==1, adjacent_count[ims[i]==0]==2)
        
    return ims_new
        

for i in range(200):
    ims = evolve_recursive(ims)


total_bugs = 0
for key in ims:
    total_bugs += np.sum(ims[key])
    
print(f'part 2 answer = {int(total_bugs)}')
    
    

