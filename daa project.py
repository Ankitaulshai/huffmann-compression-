
import heapq
import os
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox

# Huffman Node Class
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Functions for Huffman Encoding
def calculate_frequency(text):
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq

def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_codes(root, prefix="", code_dict={}):
    if root:
        if root.char is not None:
            code_dict[root.char] = prefix
        generate_codes(root.left, prefix + "0", code_dict)
        generate_codes(root.right, prefix + "1", code_dict)
    return code_dict

def encode_text(text, code_dict):
    return ''.join(code_dict[char] for char in text)

def decode_text(encoded_text, root):
    decoded_text = ""
    node = root
    for bit in encoded_text:
        node = node.left if bit == "0" else node.right
        if node.char is not None:
            decoded_text += node.char
            node = root
    return decoded_text

# File Handling
def compress_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    with open(file_path, "r") as f:
        text = f.read()

    freq_dict = calculate_frequency(text)
    root = build_huffman_tree(freq_dict)
    code_dict = generate_codes(root)
    encoded_text = encode_text(text, code_dict)

    save_path = file_path + ".bin"
    with open(save_path, "wb") as f:
        # Save frequency dictionary and encoded text
        pickle.dump((freq_dict, encoded_text), f)

    messagebox.showinfo("Success", f"File compressed and saved as: {save_path}")

def decompress_file():
    file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
    if not file_path:
        return

    with open(file_path, "rb") as f:
        freq_dict, encoded_text = pickle.load(f)

    root = build_huffman_tree(freq_dict)
    decoded_text = decode_text(encoded_text, root)

    save_path = file_path.replace(".bin", "_decompressed.txt")
    with open(save_path, "w") as f:
        f.write(decoded_text)

    messagebox.showinfo("Success", f"File decompressed and saved as: {save_path}")

# GUI Setup
root = tk.Tk()
root.title("Huffman Compression Tool")
root.geometry("400x300")

tk.Label(root, text="Huffman Encoding Compression", font=("Arial", 14)).pack(pady=10)

compress_button = tk.Button(root, text="Compress File", command=compress_file)
compress_button.pack(pady=10)

decompress_button = tk.Button(root, text="Decompress File", command=decompress_file)
decompress_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

root.mainloop()
