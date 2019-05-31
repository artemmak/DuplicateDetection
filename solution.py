from PIL import Image
import numpy as np
import math

'''
pHash method
Perceptual hashing
using DCT - discrete cosine transform
'''


#Resize image and read in black color
def regularizeImage(img, size=(16, 16)):
    return img.resize(size).convert('L')


# Computation coefficient matrix(
def getCoefficient(length):
    matrix = []
    sqr = 1.0 / math.sqrt(length)
    value = []
    for i in range(length):
        value.append(sqr)
    matrix.append(value)
    for i in range(1, length):
        value = []
        for j in range(0, length):
            value.append(math.sqrt(2.0 / length) * math.cos(i * math.pi * (j + 0.5) / length))
        matrix.append(value)
    return np.asarray(matrix)


# DCT algoritm
def DCT(matrix):
    '''

    :param matrix: Image matrix
    :return: Image matrix after DCT
    '''
    length = matrix.shape[0]
    A = getCoefficient(length)
    AT = A.T
    temp = np.multiply(A, matrix)
    DCT_matrix = np.multiply(temp, AT)
    return DCT_matrix


#Make binary hash list
def getHashCode(list_for_hash):
    length = len(list_for_hash)
    mean = sum(list_for_hash) / length

    result = []
    for i in list_for_hash:
        if i > mean:
            result.append(1)
        else:
            result.append(0)

    return result


# Compare hash values
def compHashCode(hc1, hc2):
    '''

    :param hc1: Hash code first image
    :param hc2: Hash code second image
    :return: Percentage of similarity
    '''
    cnt = 0
    for i, j in zip(hc1, hc2):
        if i == j:
            cnt += 1
    return cnt / len(hc1) * 100 #Calculate the percentage of similarity


# Calculate the similarity of perceptual hash algorithm
def calpHashSimilarity(img1, img2):
    '''

    :param img1: Name of image 1
    :param img2: Name of image 2
    :return: percent of similarity

    1. Reading image, resize and convert to matrix
    '''
    matrix1 = np.asarray(regularizeImage(img1))
    matrix2 = np.asarray(regularizeImage(img2))
# Calculate DCT matrix
    DCT1 = DCT(matrix1)
    DCT2 = DCT(matrix2)
#Get hash
    hc1 = getHashCode(np.reshape(DCT1, -1))
    hc2 = getHashCode(np.reshape(DCT2, -1))
    return compHashCode(hc1, hc2)#Сomparison and conclusion



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

    black_list = [] #Black list for file who don't  need  to check now
    threshold = 84.5
    #Сompare each file with each
    for i in range(len(files)):
        for j in range(len(files)):
            if (files[i] != files[j]) & (files[j] not in black_list):
                if calpHashSimilarity(Image.open(files[i]), Image.open(files[j])) > threshold:
                    print(files[i], files[j]) #Print detected files

        black_list.append(files[i])
    input('Press ENTER to exit')

if __name__ == "__main__":
    main(sys.argv[1:])
