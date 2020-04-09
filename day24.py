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
    



