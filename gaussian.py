def load_pgm(filename):
    """Load an ASCII PGM (P2) into a 2D list."""
    with open(filename) as f:
        lines = [l for l in f if l.strip() and not l.startswith('#')]
    if lines[0].strip() != 'P2':
        raise ValueError("Only ASCII PGM (P2) supported")
    
    width, height = map(int, lines[1].split())
    pixels = list(map(int, ' '.join(lines[3:]).split()))
    return [pixels[i*width:(i+1)*width] for i in range(height)]

def lr_range(x, step):
    '''Creates a list of [x-step, ..., x, ..., x+step]'''
    res = []

    for i in range(-step, step+1):
        res.append(x + i)
    return res

def gaussian_pixel(img, y, x, sz):
    half = sz // 2
    sum_window = []

    for irow in lr_range(y, half):
        for icol in lr_range(x, half):

            if 0 <= irow < len(img) and 0 <= icol < len(img[y]):
                
    

# def avg_pixel(img, y, x, sz):
#     half = sz // 2
#     sum_window = []

#     # xs = list(range(-half, half+1))

#     xlo = max(min(lr_range(x,half)), 0)
#     xhi = min(max(lr_range(x,half))+1, len(img[y]))

#     for irow in lr_range(y,half):
#         if irow < 0 or irow >= len(img):
#             row = []
#         else:
#             row = img[irow][xlo:xhi]

#         sum_window = sum_window + row

#     if len(sum_window) == 0:
#         return img[y][x]

#     return sum(sum_window)/len(sum_window)

def new_img(img,sz):
    res = []
    for y in range(len(img)):
        res.append([])
        for x in range(len(img[y])):
            res[y].append(avg_pixel(img,y,x,sz))
    return res

print(new_img(load_pgm("feep.ascii.pgm"),3))