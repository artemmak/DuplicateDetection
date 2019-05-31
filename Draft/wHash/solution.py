from PIL import Image, ImageOps
import numpy as np



def resizeMatrix(image):
    return np.asarray(ImageOps.crop(image, (60,60,60,60)).resize((64, 64)))


def getHashLayers(layers):
    Hash = []
    k=3
    for l in range(layers.shape[2]):
        T = k*np.std(layers[:,:,l])
        for i in range(layers.shape[0]):
            for j in range(layers.shape[1]):
                if layers[i,j,l] > T:
                    Hash.append(1)
                else:
                    Hash.append(0)
    return Hash

def compHashCode(hc1, hc2):
    cnt = 0
    for i, j in zip(hc1, hc2):
        if i == j:
            cnt += 1
    return cnt/len(hc1)*100



def HashSimilariti(img1, img2):
    return compHashCode(getHashLayers(resizeMatrix(img1)),getHashLayers(resizeMatrix(img2)))


def input_check(argv):
    '''
        Check if what input and is it correct
    '''
    if len(argv) == 1 and (argv[0] == '--help' or argv[0] == 'h'):
        print('''usage: solution.py [-h] --path PATH
First test task on images similarity.
optional arguments:
  -h, --help            show this help message and exit
  --path PATH           folder with images
'''
)
        return None

    if len(argv) == 2 and (argv[0] == '--path' or argv[1] == 'PATH'):
        return argv[1]
    print('usage: solution.py [-h] --path PATH\nsolution.py: error: the following arguments are required: --path')
    return None


import os, sys
def main(argv):
    path = input_check(argv)
    if path == None:
        return

    if path[-1]  != '/':
        path += '/'

    #read files from dir  listed  formats in formats list
    formats = ['jpg', 'png', 'tif', 'jpeg']
    files = []
    for fil in os.listdir():
        if fil.split('.')[-1].lower() in formats:
            files.append(fil)

    black_list = []#Black list for file who don't  need  to check now
    threshold = 91
    for i in range(len(files)):
        for j in range(len(files)):
            if (files[i] != files[j]) & (files[j] not in black_list):
                res = HashSimilariti(Image.open(files[i]), Image.open(files[j]))
                if res > threshold:
                    print(files[i], files[j])

        black_list.append(files[i])
    input('Press ENTER to exit')

if __name__ == "__main__":
    main(sys.argv[1:])
