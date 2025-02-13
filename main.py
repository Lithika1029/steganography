import numpy as np
import cv2

def encode_image(image_path, message, output_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or format not supported.")
    
    binary_message = ''.join(format(ord(i), '08b') for i in message) + '11111110'  # 8-bit EOF marker
    data_index = 0
    message_length = len(binary_message)
    
    for row in image:
        for pixel in row:
            for channel in range(3):  # Modify R, G, B
                if data_index < message_length:
                    # Clear the LSB and ensure the result is non-negative
                    pixel[channel] = (pixel[channel] & 0xFE) | int(binary_message[data_index])
                    data_index += 1
                else:
                    break
            else:
                continue
            break
        else:
            continue
        break
    
    cv2.imwrite(output_path, image)
    print(f"Message encoded and saved to {output_path}")

def decode_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or format not supported.")
    
    binary_message = ""
    for row in image:
        for pixel in row:
            for channel in range(3):
                binary_message += str(pixel[channel] & 1)
    
    binary_chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ""
    for char in binary_chars:
        if char == '11111110':  # 8-bit EOF marker
            break
        message += chr(int(char, 2))
    
    return message

if __name__ == "__main__":
    choice = input("Do you want to encode (e) or decode (d) a message? ").strip().lower()
    if choice == 'e':
        img_path = input("Enter the image path: ").strip('"')  # Remove quotes
        msg = input("Enter the message: ")
        output_img = input("Enter output image path: ").strip('"')  # Remove quotes
        encode_image(img_path, msg, output_img)
    elif choice == 'd':
        img_path = input("Enter the encoded image path: ").strip('"')  # Remove quotes
        print("Decoded message:", decode_image(img_path))
    else:
        print("Invalid choice!")