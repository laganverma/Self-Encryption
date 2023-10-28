import hashlib
import time

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

def main():
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    num_of_blocks_to_add = 20

    for i in range(0, num_of_blocks_to_add):
        new_block_data = "Hey! I'm block #" + str(i)
        new_block = create_new_block(previous_block, new_block_data)
        blockchain.append(new_block)
        previous_block = new_block
        print("Block #{} has been added to the blockchain!".format(new_block.index))
        print("Hash: {}\n".format(new_block.hash))

if __name__ == '__main__':
    main()
