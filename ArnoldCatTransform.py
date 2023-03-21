from math import log

import numpy as np
import cv2


def ArnoldCatTransform(img, num):
    rows, cols, ch = img.shape
    n = rows
    img_arnold = np.zeros([rows, cols, ch])
    for x in range(0, rows):
        for y in range(0, cols):
            img_arnold[x][y] = img[(x+y)%n][(x+2*y)%n]
    return img_arnold


class ArnoldCat:
    def __init__(self):
        self.progress = 0

    def ArnoldCatEncryption(self, imageName, key):
        img = cv2.imread(imageName)
        for i in range(0, key):
            self.progress = int(i * 100 / key)
            img = ArnoldCatTransform(img, i)
        cv2.imwrite(imageName.split('.')[0] + "_ArnoldcatEnc.png", img)
        self.progress = 100
        return img

    def ArnoldCatDecryption(self, imageName, key):
        img = cv2.imread(imageName)
        rows, cols, ch = img.shape
        dimension = rows
        decrypt_it = dimension
        if (dimension % 2 == 0) and 5**int(round(log(dimension/2, 5))) == int(dimension/2):
            decrypt_it = 3*dimension
        elif 5**int(round(log(dimension, 5))) == int(dimension):
            decrypt_it = 2*dimension
        elif (dimension % 6 == 0) and 5**int(round(log(dimension/6, 5))) == int(dimension/6):
            decrypt_it = 2*dimension
        else:
            decrypt_it = int(12*dimension/7)
        for i in range(key, decrypt_it):
            self.progress = int(i / decrypt_it)
            img = ArnoldCatTransform(img, i)
        filename = imageName.split('_')[0] + "_ArnoldcatDec.png"
        print(filename)
        cv2.imwrite(filename, img)
        self.progress = 100
        return img


if __name__ == "__main__" :
    pass
    # ArnoldCatDecryption("D:\\EncryptIt\\orig_ArnoldcatEnc.png", 20)
    # ArnoldCatEncryption()
