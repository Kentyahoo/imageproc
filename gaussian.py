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

# def weight_multiplier(sz, row):
#     res = []
#     half = sz//2
#     for i in len(row)-1:
#         res.append(og_multiplier[i]*row[i])

    return res

def weight_multiplier(sz, row):
    '''first part returns eg. [1,2,4,2,1], second part matches and multiplies with row. weights the numbers in (row)'''
    half = sz // 2
    weights = []
    value = 1
    
    for i in range(sz):
        weights.append(value)
        if i < half:
            value *= 2
        else:
            value //= 2

    res = []
    for i in range(len(row)):
        res.append(row[i] * weights[i])
    return res

def gaussian_multiplier(sz):
    '''returns eg. [1,2,3,2,1]'''
    half = sz // 2
    weights = [half + 1 - abs(i - half) for i in range(sz)]
    return weights


def gaussian_denominator(sz):
    '''first part makes eg. [1,2,4,2,1], second part adds 1,2,4,2,1, third part does that with the whole window'''
    half = sz // 2
    gaussian_sum = 0
    weights = []
    value = 1
    
    for i in range(sz):
        weights.append(value)
        if i < half:
            value *= 2
        else:
            value //= 2
    sum_row = sum(weights)
    for i in gaussian_multiplier(sz):
        gaussian_sum = gaussian_multiplier(sz)[i] * sum_row + gaussian_sum
    return gaussian_sum

def avg_pixel(img, y, x, sz):
    half = sz // 2
    sum_window = []

    xlo = max(min(lr_range(x,half)), 0)
    xhi = min(max(lr_range(x,half))+1, len(img[y]))

    for irow in lr_range(y,half):
        gaussian_row = []
        if irow < 0 or irow >= len(img):
            row = []
        else:
            row = img[irow][xlo:xhi]
            for multiplier in gaussian_multiplier(sz):
                gaussian_row = [n * multiplier for n in weight_multiplier(sz, row)]

        sum_window = sum_window + gaussian_row


    if len(sum_window) == 0:
        return img[y][x]

    return sum(sum_window)/gaussian_denominator(sz)

    

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
print(gaussian_multiplier(sz=3))