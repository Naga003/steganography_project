# Image Steganography with Python

This project demonstrates a simple method for hiding and retrieving secret messages within images using steganography techniques. The code is written in Python and utilizes the OpenCV library for image processing.

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- OpenCV (`cv2`)
- `os` module (part of the standard Python library)

## Installation

You can install OpenCV using pip if you don't have it already:

```bash
pip install opencv-python

Usage
Encryption
Ensure your image (e.g., r.PNG) is in the same directory as the script.

Run the encryption script:

python
import cv2
import os

# Read the image
img = cv2.imread("r.PNG")

# Prompt the user for a secret message and passcode
msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Ensure the message length fits within the image dimensions
if len(msg) > img.shape[0] * img.shape[1] * 3:
    print("Message is too long to be hidden in the image.")
    exit(1)

# Dictionaries for mapping characters to integers (and vice versa)
d = {chr(i): i for i in range(256)}
c = {i: chr(i) for i in range(256)}

# Initialize variables for the pixel manipulation
m = 0
n = 0
z = 0

# Encrypt the secret message into the image
for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    z = (z + 1) % 3
    if z == 0:
        m += 1
        if m == img.shape[1]:
            m = 0
            n += 1
            if n == img.shape[0]:
                break

# Save the encrypted image
cv2.imwrite("encryptedImage.png", img)

# Open the encrypted image (works on Windows)
os.system("start encryptedImage.png")

# Save the password and message length in a separate file for decryption
metadata_file_path = "metadata.txt"
with open(metadata_file_path, "w") as f:
    f.write(password.strip() + "\n")
    f.write(str(len(msg)))

# Let the user know the encryption is done
print(f"Image encrypted and saved as 'encryptedImage.png'.")
print(f"Metadata saved in '{metadata_file_path}'.")
Decryption
Ensure the encrypted image (encryptedImage.png) and metadata file (metadata.txt) are in the same directory as the script.

Run the decryption script:

python
import cv2
import os

# Check if the metadata file exists
metadata_file_path = "metadata.txt"
if not os.path.exists(metadata_file_path):
    print(f"Metadata file '{metadata_file_path}' not found.")
    exit(1)

# Read the encrypted image
encrypted_img = cv2.imread("encryptedImage.png")

# Prompt the user for the decryption passcode
decrypt_password = input("Enter the decryption passcode: ")

# Read the original passcode and message length from the metadata file
with open(metadata_file_path, "r") as f:
    original_password = f.readline().strip()
    msg_length = int(f.readline().strip())

# Verify the entered passcode
if decrypt_password.strip() == original_password:
    # Dictionaries for mapping integers to characters
    c = {i: chr(i) for i in range(256)}

    # Initialize variables for pixel reading
    m = 0
    n = 0
    z = 0

    # Decrypt the message from the image
    decrypted_msg = ""
    while len(decrypted_msg) < msg_length:
        pixel_value = encrypted_img[n, m, z]
        if 0 <= pixel_value < 256:
            decrypted_msg += c[pixel_value]
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m == encrypted_img.shape[1]:
                m = 0
                n += 1
                if n == encrypted_img.shape[0]:
                    break

    # Print the decrypted message
    print("Decrypted message:", decrypted_msg)
else:
    print("Incorrect passcode. Decryption failed.")

# Let the user know the decryption process is completed
print("Decryption process completed.")
