import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def messageToBinary(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), '08b') for i in msg])
    elif type(msg) == np.ndarray:
        return([format(i, '08b') for i in msg])
    elif type(msg) == int:
        return format(msg, '08b')
    else:
        raise TypeError('Input type is not supported')   

def encodeMessage():
    img_name = input('\nEnter image name (with extension): ')
    # read the input image
    img = cv2.imread(img_name)
    
    # display the image
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()

    # calculate the maximum bytes in the image
    max_bytes = img.shape[0] * img.shape[1] * 3 // 8

    msg = input('Enter message to be encoded: ')
    if len(msg) == 0:
        raise ValueError('Message is empty')
    
    # check if the number of bytes to encode is less than the maximum bytes in the image
    if len(msg) > max_bytes:
        raise ValueError('Insufficient bytes, need bigger image or less data')

    print('\nEncoding...')
    
    # add a delimiter at the end of message
    msg += '!@#$%&'
    
    # convert message to binary format
    binary_msg = messageToBinary(msg)
    
    # find the length of message that needs to be hidden
    msg_len = len(binary_msg)
    
    msg_index = 0
    for color in img:
        for pixel in color:
            # convert RGB values to binary format
            r, g, b = messageToBinary(pixel)
            # modify the LSB only if there is still data to store
            if msg_index < msg_len:
                # hide the data into LSB of red pixel
                pixel[0] = int(r[:-1] + binary_msg[msg_index], 2)
                msg_index += 1
            if msg_index < msg_len:
                # hide the data into LSB of green pixel
                pixel[1] = int(g[:-1] + binary_msg[msg_index], 2)
                msg_index += 1
            if msg_index < msg_len:
                # hide the data into LSB of blue pixel
                pixel[2] = int(b[:-1] + binary_msg[msg_index], 2)
                msg_index += 1
            # if data is encoded, break
            if msg_index >= msg_len:
                break
    
    filename = input('\nEnter the name of new encoded image (with extension): ')

    # hide the secret message into the selected image
    cv2.imwrite(filename, img)

def decodeMessage():
    # read the image that contains the hidden image
    img_name = input('\nEnter the steganographed image name (with extension): ')
    # read the image
    img = cv2.imread(img_name)
    
    # display the image
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    
    print('\nDecoding...')

    binary_msg = ''
    for values in img:
        for pixel in values:
            # convert RGB values to binary format
            r, g, b = messageToBinary(pixel)

            # extract data from the LSB of red pixel
            binary_msg += r[-1]
            # extract data from the LSB of green pixel
            binary_msg += g[-1]
            # extract data from the LSB of blue pixel
            binary_msg += b[-1]
    
    # split the binary message by 8-bits
    bytes_msg = [binary_msg[i: i+8] for i in range(0, len(binary_msg), 8)]
    
    # convert from bits to characters
    decoded_msg = ''
    for byte in bytes_msg:
        decoded_msg += chr(int(byte, 2))
        # check if we have reached the delimeter
        if decoded_msg[-6:] == '!@#$%&':
            break
    
    # remove the delimeter
    return decoded_msg[:-6]

if __name__ == "__main__":
    os.system('cls')
    option = int(input('=== Image Steganography ===\n 1. Encode the message\n 2. Decode the message\n Select an option: '))

    if option == 1:
        encodeMessage()
        
    elif option == 2:
        print('\nDecoded message:', decodeMessage())
    else:
        raise Exception('Please enter a valid option')
