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

def lr_range(x, step):
    '''Creates a list of [x-step, ..., x, ..., x+step]'''
    res = []

    for i in range(-step, step+1):
        res.append(x + i)
    return res


def avg_pixel(img, y, x, sz, template):
    half = sz // 2

    total = 0
    weight_sum = 0

    for dy in range(-half, half + 1):
        ny = y + dy #range of y 
        if 0 <= ny < len(img):
            for dx in range(-half, half + 1):
                nx = x + dx #range of x
                if 0 <= nx < len(img[0]):
                    total += template[ny][nx]*(ny+nx)

    return total / weight_sum if weight_sum != 0 else img[y][x]

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