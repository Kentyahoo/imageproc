import argparse

def load_pgm(filename):
    """Load an ASCII PGM (P2) into a 2D list."""
    with open(filename) as f:
        lines = [l for l in f if l.strip() and not l.startswith('#')]
    if lines[0].strip() != 'P2':
        raise ValueError("Only ASCII PGM (P2) supported")
    
    width, height = map(int, lines[1].split())
    pixels = list(map(int, ' '.join(lines[3:]).split()))
    return [pixels[i*width:(i+1)*width] for i in range(height)]

# def lr_range(x, step):
#     '''Creates a list of [x-step, ..., x, ..., x+step]'''
#     res = []

#     for i in range(-step, step+1):
#         res.append(x + i)
#     return res

# def make_list(lowest, sz):
#     nums = []
#     for i in range(sz):
#         nums.append(lowest + i)
#     return nums

# def shift_list(nums):
#     if min(nums) < 0:
#         shift = abs(min(nums))
#         nums = [x + shift for x in nums]
#     return nums


# def weight_multiplier(sz, row):
#     res = []
#     half = sz//2
#     for i in len(row)-1:
#         res.append(og_multiplier[i]*row[i])


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


# def weight_multiplier(sz, row):
#     '''first part returns eg. [1,2,4,2,1], second part matches and multiplies with row. weights the numbers in (row)'''
#     weights = gaussian_multiplier(sz)

#     res = []
#     for i in range(len(row)):
#         res.append(row[i] * weights[i])
#     return res


# def gaussian_denominator(sz):
#     '''first part makes eg. [1,2,4,2,1], second part adds 1,2,4,2,1, third part does that with the whole window'''
#     weights = gaussian_multiplier(sz)
#     sum_row = sum(weights)
#     return sum_row**2

def avg_pixel(img, y, x, sz):
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

    
'''command line interface how to read command line inputs and outputs
'''

def new_img(img,sz):
    res = []
    for y in range(len(img)):
        res.append([])
        for x in range(len(img[y])):
            res[y].append(avg_pixel(img,y,x,sz))
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Gaussian blur to a PGM image")

    parser.add_argument("image", help="PGM image filename")
    parser.add_argument("size", type=int, help="Gaussian kernel size (odd number like 3,5,7)")

    args = parser.parse_args()

    img = load_pgm(args.image)
    sz = args.size

    blurred = new_img(img, sz)

    print(blurred) 