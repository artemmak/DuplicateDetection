from PIL import Image
import numpy as np

'''
pHash method
Perceptual hashing
using DCT - discrete cosine transform
'''


#Resize image and read in black color
def changeImage_d_Hash(img, size=(9, 8)):
    return np.array(img.resize(size).convert('L')).T


def changeImage(img, size=(8, 8)):
    return np.array(img.resize(size).convert('L')).T


def get_d_HashCode(array, size=(9, 8)):
    result = []
    for i in range(size[0] - 1):
        for j in range(size[1]):
            curent_pixel = array[i][j]
            next_pixel = array[i + 1][j]
            if curent_pixel > next_pixel:
                result.append(1)
            else:
                result.append(0)
    return result


def get_a_HashCode(array):
    mean = np.mean(array)

    size = array.shape

    result = []

    for i in range(size[0]):
        for j in range(size[1]):
            if array[i][j] > mean:
                result.append(1)
            else:
                result.append(0)

    return result


def findSimilarParts(hash1, hash2):
    number = 0
    for i, j in zip(hash1, hash2):
        if i == j:
            number += 1

    return number / len(hash1) * 100


def getResult_d_Hash(img1, img2):
    img1 = changeImage_d_Hash(img1)
    img2 = changeImage_d_Hash(img2)
    hash1 = get_d_HashCode(img1)
    hash2 = get_d_HashCode(img2)
    return findSimilarParts(hash1, hash2)


def getResult_a_Hash(img1, img2):
    img1 = changeImage(img1)
    img2 = changeImage(img2)
    hash1 = get_a_HashCode(img1)
    hash2 = get_a_HashCode(img2)
    return findSimilarParts(hash1, hash2)

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

    #Black list for file who don't  need  to check now
    black_list = []
    threshold = 90
    for i in range(len(files)):
        for j in range(len(files)):
            if (files[i] != files[j]) & (files[j] not in black_list):
                res = getResult_d_Hash(Image.open(files[i]), Image.open(files[j]))
                if res > threshold:
                    print(files[i], files[j])

        black_list.append(files[i])
    input('Press ENTER to exit')

if __name__ == "__main__":
    main(sys.argv[1:])
