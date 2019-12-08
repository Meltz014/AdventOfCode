import numpy
from matplotlib import pyplot as plt
from matplotlib import colors

def main():
    shape = (-1, 6, 25)
    data = numpy.genfromtxt('day8\\input.txt', delimiter=1, dtype=numpy.int8)
    data = data.reshape(shape)

    # part 1
    fewest = min([(len(layer[layer==0]), i) for (i, layer) in enumerate(data)], key=lambda x: x[0])
    fewest_layer = data[fewest[1]]
    ans = len(fewest_layer[fewest_layer == 1]) * len(fewest_layer[fewest_layer == 2])
    print(f'Part 1: {ans}')

    # part 2
    BLACK = 0
    WHITE = 1
    TRANS = 2

    # add layers
    img = numpy.ones((6, 25), dtype=numpy.int8) * TRANS

    for layer in data:
        img[img==TRANS] = layer[img==TRANS]

    # display
    # make a color map of fixed colors
    cmap = colors.ListedColormap(['black', 'white', 'gray'])
    bounds=[-1,0.5,1.5,2.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    # tell imshow about color map so that only set colors are used
    img = plt.imshow(img, interpolation='nearest', origin='upper',
                     cmap=cmap, norm=norm)

    # make a color bar
    plt.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=bounds)

    #plt.savefig('redwhite.png')
    plt.show()

if __name__ == '__main__':
    main()
