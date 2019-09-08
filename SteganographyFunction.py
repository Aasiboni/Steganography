import os
import numpy as np
import cv2
from matplotlib import pyplot as plt

def filesList(userSelection):
    # 1 - if we want to decode
    if userSelection == '1':

        Path = 'encoded/'
        if len(os.listdir(Path)) == 0:
            print('Folder is empty! no files for decode')
            exit(0)

        imageName = os.listdir(Path)
        for name in imageName:
            print(name)
        imageName = raw_input('\nSelect image name for decode from above: ')
        if os.path.isfile(Path+'\\%s' %imageName):
            return imageName
        else:
            print ('The file you selected in not exist')
            exit(0)
    # 2 - if we want to encode
    else:

        Path = 'images/'
        if len(os.listdir(Path)) == 0:
            print('Folder is empty! no files for encode')
            exit(0)

        imageName = os.listdir(Path)
        for name in imageName:
            print(name)
        imageName = raw_input('\nSelect image name for encode from above list: ')
        if os.path.isfile(Path+'\\%s' % imageName):
            return imageName
        else:
            print ('he file you selected in not exist')
            exit(0)

def binUpdate(decimalNum, bitToChange):
    redChannelUpdate = bin(decimalNum)
    redChannelUpdate = redChannelUpdate[:-1] + bitToChange
    backToInt = int(redChannelUpdate, 2)

    return backToInt

def decodeImage(inputForDecode):

    imageForDecode = 'encoded/%s'%inputForDecode
    encodedImage = cv2.imread(imageForDecode)
    encodedImage_RGB = cv2.cvtColor(encodedImage, cv2.COLOR_BGR2RGB)
    redChannel, G, B = cv2.split(encodedImage_RGB)

    x_size, y_size, dim = encodedImage_RGB.shape

    decoded_image = np.zeros((x_size, y_size, 3), np.uint8)

    for i in range(x_size):
        for j in range(y_size):
            if bin(redChannel[i, j])[-1] == '0':
                decoded_image[i, j] = (255, 255, 255)
            else:
                decoded_image[i, j] = (0, 0, 0)

    cv2.imwrite("decoded/decoded_" + inputForDecode, decoded_image)
    print("Decoding succeeded!\nThe decoded file is saved under decoded folder in the root folder\n")

    plt.subplot(121), plt.imshow(encodedImage_RGB), plt.title('Encoded')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(decoded_image), plt.title('Decoded\nIf its a large scale picture, please use a magnifying glass to see the hidden text')
    plt.xticks([]), plt.yticks([])
    plt.show()

def writeText(text_to_write, X_size, Y_size):

    textToImage = np.zeros((X_size, Y_size, 3), np.uint8)

    cv2.putText(textToImage, text_to_write, (10, 30), cv2.FONT_ITALIC, 0.8, (255, 255, 255))

    ret, BWImage = cv2.threshold(textToImage, 1, 255, cv2.THRESH_BINARY_INV)

    return BWImage

def encodeImage(text_to_encode, imageForEncode):

    imputImagePath = 'images/%s'%imageForEncode
    imputImage = cv2.imread(imputImagePath)

    imputImage_RGB = cv2.cvtColor(imputImage, cv2.COLOR_BGR2RGB)
    # plt.imshow(imputImage_RGB)
    # plt.show()
    R, G, B = cv2.split(imputImage_RGB)

    x_size, y_size, dim = imputImage.shape

    image_text = writeText(text_to_encode, x_size, y_size)

    encodedImage = np.zeros((x_size, y_size, 3), np.uint8)

    for i in range(x_size):
        for j in range(y_size):
            imageChannels = R[i, j]

            bitTest = image_text[i, j]
            blackOrWhiteBit = bin(bitTest[1])

            if blackOrWhiteBit[-1] == '1':
                redChannelVal = binUpdate(imageChannels, '1')
            else:
                redChannelVal = binUpdate(imageChannels, '0')

            encodedImage[i, j] = [B[i, j], G[i, j], redChannelVal]



    cv2.imwrite("encoded/" +
                os.path.splitext(imageForEncode)[0] + ".png", encodedImage)
    print("Encoding succeeded!\nThe encoded file is saved under encoded folder in the root folder")
    encodedImage = cv2.cvtColor(encodedImage,cv2.COLOR_BGR2RGB)


    plt.subplot(121), plt.imshow(imputImage_RGB), plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(encodedImage), plt.title('Encoded')
    plt.xticks([]), plt.yticks([])
    plt.show()