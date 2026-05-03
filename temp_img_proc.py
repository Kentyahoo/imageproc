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

def avg_pixel(img, y, x, sz):
    half = sz // 2

    sum_window = []
    # xs = list(range(-half, half+1))

    xlo = max(x-half, 0)
    xhi = min(x+half+1, len(img[y]))

    for irow in lr_range(y,half):
        if irow < 0 or irow >= len(img):
            row = []
        else:
            row = img[irow][xlo:xhi]

        sum_window = sum_window + row

    if len(sum_window) == 0:
        return img[y][x]

    return sum(sum_window)/len(sum_window)


def gaussian_multiplier(sz):
    '''returns eg. [1,2,4,2,1]'''
    half = sz // 2
    weights = []
    value = 1
    
    for i in range(sz):
        weights.append(value)
        if i < half:
            value *= 2
        else:
            value //= 2
            
    return weights

def gaussianpixel(img, y, x, sz):
    #Gaussian
    half = sz // 2
    weights = gaussian_multiplier(sz)
    # weights will be the same for x & y
    wd = len(img[0])
    ht = len(img)
    total = 0
    weight_sum = 0

    for dy in range(-half, half + 1):
        imgy = y + dy #range of y 
        if 0 <= imgy < ht:
            wy = weights[dy + half]  # vertical weight
            for dx in range(-half, half + 1):
                imgx = x + dx #range of x
                if 0 <= imgx < wd:
                    wx = weights[dx + half]  # horizontal weight
                    w = wy * wx
                    total += img[imgy][imgx] * w
                    weight_sum += w

    return total / weight_sum if weight_sum != 0 else img[y][x]

def pixeleval(img, template, y, x):
    #template
    sz = len(template)
    half = sz // 2
    ht = len(img)
    wd = len(img[0])
    
    res = 0
    temp_sum = 0
    
    for yT in range(sz):
        for xT in range(sz):
            ny = y + yT - half
            nx = x + xT - half
            if 0 <= ny < ht and 0 <= nx < wd:
                res += img[ny][nx] * template[yT][xT]
                temp_sum += template[yT][xT]
    
    return round(res / temp_sum) if temp_sum != 0 else 0
def img_proc(img,sz, operation="avg", template=None):
    method = 0
    res = []
    ht = len(img)-1
    wd = len(img[0])-1
    for y in range(ht):
        res.append([])
        for x in range(wd):
            if template == None:
                if operation == "gaussian":
                    method = gaussianpixel(img,sz,x,y,)
                elif operation == 'avg':
                    method = avg_pixel(img,y,x,sz)
            else:
                method == pixeleval(img, template,y,x,)
            res[y].append(method)
    return res

print(img_proc(load_pgm("feep.ascii.pgm"),3))


# def img_proc(img, template):
#     ht = len(img)
#     wd = len(img[0])
    
#     res = []
#     for y in range(ht):
#         res.append([])
#         for x in range(wd):
#             res[y].append(pixeleval(img, template, y, x))
#     return res