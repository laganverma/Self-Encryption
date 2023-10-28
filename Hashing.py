import hashlib
import time
import json
import tkinter as tk
from tkinter import messagebox

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def create_genesis_block():
    return Block(0, "0", time.time(), "BLOCKCHAIN IS CREATED", calculate_hash(0, "0", time.time(), "BLOCKCHAIN IS CREATED"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + previous_hash + str(timestamp) + data
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def save_blockchain(blockchain):
    with open('blockchain.json', 'w') as file:
        json.dump([vars(block) for block in blockchain], file)

def load_blockchain():
    try:
        with open('blockchain.json', 'r') as file:
            data = json.load(file)
            return [Block(block['index'], block['previous_hash'], block['timestamp'], block['data'], block['hash']) for block in data]
    except FileNotFoundError:
        return []

def validate_blockchain(blockchain):
    for i in range(1, len(blockchain)):
        if blockchain[i].previous_hash != blockchain[i-1].hash:
            return False
    return True

def add_block():
    new_block_data = entry.get()
    if not new_block_data:
        messagebox.showerror("Error", "Please enter block data")
        return

    new_block = create_new_block(blockchain[-1], new_block_data)
    blockchain.append(new_block)
    save_blockchain(blockchain)

    entry.delete(0, tk.END)
    label.config(text="Block #{} added to the blockchain".format(new_block.index))

def show_blockchain():
    chain = "\n".join("Block #{}: {}".format(block.index, block.data) for block in blockchain)
    messagebox.showinfo("Blockchain", chain)

def main():
    blockchain = load_blockchain()

    root = tk.Tk()
    root.title("Blockchain GUI")

    label = tk.Label(root, text="Enter block data:")
    label.pack()

    entry = tk.Entry(root, width=30)
    entry.pack()

    add_button = tk.Button(root, text="Add Block", command=add_block)
    add_button.pack()

    show_button = tk.Button(root, text="Show Blockchain", command=show_blockchain)
    show_button.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
