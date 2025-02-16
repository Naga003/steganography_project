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
    original_password = f.readline().strip()  # Read without leading/trailing spaces
    msg_length = int(f.readline().strip())  # Read the message length

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
        if 0 <= pixel_value < 256:  # Ensure pixel value is within ASCII range
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
