const fs = require('fs');

function range(start = 0, end) {
    const arr = [];
    for (let i = start; i < end; i++) {
        arr.push(i);
    }
    return arr;
}

function loadPgm(filename) {
    // Load an ASCII PGM (P2) into a 2D array.
    const lines = fs.readFileSync(filename, 'utf8')
        .split('\n')
        .filter(line => line.trim() && !line.startsWith('#'));

    if (lines[0].trim() !== 'P2') {
        throw new Error("Only ASCII PGM (P2) supported");
    }

    const [width, height] = lines[1].split(' ').map(Number);
    const pixels = lines.slice(3).join(' ').split(/\s+/).map(Number);

    const image = [];
    for (let i = 0; i < height; i++) {
        image.push(pixels.slice(i * width, (i + 1) * width));
    }

    return image;
}

/**
 * @Note Creates a list of [x-step, ..., x, ..., x+step]
 * @Assume @param step is a number, @param x can be a string
 */
function lrRange(x, step) {
  const res = Array.from({length: step*2 + 1}, (_,i) => {
    return i + Number(x)-step
  })
  return res
}

function avgPixel(img, y, x, sz) {
  const half = Math.floor(sz/2)

  let sumWindow = []

  let xlo = Math.max(x-half, 0)
  let xhi = Math.min(x+half+1, img[y].length)
  let row;          
  for (let irow of lrRange(y,half)) {
    if (irow < 0 || irow >= img.length) {
      row = []
    } 
    else {
      row = img[irow].slice(xlo, xhi)
    }
    sumWindow.push(row)
  if (sumWindow.length == 0) {
    return img[y][x]
  }
  let total = 0;

for (const row of sumWindow) {
    for (const value of row) {
        total += value;
    }
}
  return total / sumWindow.length**2
  }
}

function gaussianMultiplier(sz) {
  const half = Math.floor(sz/2)
  let weights = []
  let value = 1
  
  for (let i = 0; i < sz; i++) {
    weights.push(value)
    if (i < half) {
      value *= 2
    }  
    else {
      value = Math.floor(value/2)
    }
  }
  return weights
  
  }

function gaussianPixel(img, y, x, sz) {
  const half = Math.floor(sz/2)
  const weights = gaussianMultiplier(sz)
  const wd = img[0].length
  const ht = img.length
  let total = 0
  let weightSum = 0

  for (let dy of range(-half, half + 1)) {
    let imgy = y+dy
    if (imgy >= 0 && imgy < ht) {
      let wy = weights[dy + half]
      for (let dx of range (-half, half + 1)) {
        let imgx = x + dx
        if (ny >= 0 && ny < ht && nx >= 0 && nx < wd) {
          let wx = weights[dx + half]
          let w = wy * wx
          total += img[imgy][imgx] * w
          weightSum += w 
        }
      }
    }
  }
  let res = 0
  if (weightSum != 0) {
    return total / weightSum
  }
  else {
    return img[y][x]
  }
}

function pixeleval(img, template, y, x) {
  const sz = template.length
  const half = Math.floor(sz/2 )
  const ht = img.length
  const wd = img[0].length
  let res = 0
  let temp_sum = 0

  for (let yT of range(0, sz)) {
    for (let xT of range(0, sz)){

      let ny = y + yT - half
      let nx = x +xT - half

      if (ny >= 0 && ny < ht && nx >= 0 && nx < wd) {
        let w = template[yT][xT]
        res += img[ny][nx] * w
        temp_sum += w

      }
    }
  }
  if (temp_sum != 0) {
    return res / temp_sum
  } else { 
    return 0
  }
}

function imgProc(img, sz, operation = "avg", template=null) {
  let method = 0
  let res = []
  const ht = img.length
  const wd = img[0].length

  for (y in range(0, ht)) {
    res.push([])
    for (x in range(0, wd)) {
      if (template == null) {
        if (operation == "gaussian") {
         method = gaussianPixel(img, y, x, sz)
        }
        else if (operation == "avg") {
        method = avgPixel(img, y, x, sz)
  } 
}
        else {
         method = pixeleval(img, template, y, x)
}

        res[y].push(method);
      }
    }
    return res
  }
  


const readline = require('readline-sync')

function main() {

    const filename = readline.question("Enter PGM filename: ")
    const img = loadPgm(filename)

    while (true) {

        console.log("\n=== IMAGE PROCESSING MENU ===")
        console.log("1. Average Blur")
        console.log("2. Gaussian Blur")
        console.log("3. Custom Template")
        console.log("4. Quit")
        const choice = readline.question("Choose an option: ")

        if (choice === "1") {
            const sz = parseInt(readline.question("Kernel size: "))
            const result = imgProc(img, sz, "avg")
            console.log("\nProcessed Image:")
            console.log(result)
        }

        else if (choice === "2") {

            const sz = parseInt(readline.question("Kernel size: "))
            const result = imgProc(img, sz, "gaussian")
            console.log("\nProcessed Image:")
            console.log(result)
        } 

        else if (choice === "3") {
            const sz = parseInt(readline.question("Template size: "))
            console.log(`\nEnter ${sz * sz} numbers separated by spaces:`)
            let vals = readline.question("").split(" ").map(Number)
            // console.log('vals',vals)
            // vals = vals.split(" ").map(Number)
            const template = []

            for (let i = 0; i < sz; i++) {
                const row = vals.slice(i * sz, (i + 1) * sz)
                template.push(row)
            }

            console.log("\nTemplate:")
            for (const row of template) {
                console.log(row)
            }
            const result = imgProc(img, sz, "avg", template)
            console.log("\nProcessed Image:")
            console.log(result)
        }
        else if (choice === "4") {

            console.log("Goodbye")
            break
        }
        else {
            console.log("Invalid option")
        }
    }
}
main()