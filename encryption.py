import cv2
import os

# Read the image
img = cv2.imread("r.PNG")  # Replace with the correct image path

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
cv2.imwrite("encryptedImage.png", img)  # Use .png to avoid compression artifacts

# Open the encrypted image (works on Windows)
os.system("start encryptedImage.png")  # Use 'start' for Windows

# Save the password and message length in a separate file for decryption
metadata_file_path = "metadata.txt"
with open(metadata_file_path, "w") as f:
    f.write(password.strip() + "\n")  # Save without leading/trailing spaces
    f.write(str(len(msg)))  # Save the message length

# Let the user know the encryption is done
print(f"Image encrypted and saved as 'encryptedImage.png'.")
print(f"Metadata saved in '{metadata_file_path}'.")
