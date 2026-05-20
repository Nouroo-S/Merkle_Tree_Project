import hashlib
import os

class MerkleNode: 
    def __init__(self, file_path, left=None, right=None, hash=None):
        self.left = left
        self.right = right
        if hash:
            self.hash = hash
        else:
            with open(file_path, 'r') as file:
                file_content = file.read()
            self.hash = hashlib.sha1(file_content.encode()).hexdigest()

# Write a list of words to corresponding list of files
def write_to_files(word_list, file_list):
    if (len(word_list) < len(file_list)):
        for i in range(len(word_list) , len(file_list) - len(word_list) , 1):
            word_list.append(word_list[0]+ " ")
    
    for i, file_Path in enumerate(file_list):
        with open(file_Path, 'w') as f:
            f.write(word_list[i])
    return file_list

# Create a MerkleTree object with full hashes
def build_tree(file_paths):
    nodes = [MerkleNode(file_path) for file_path in file_paths]

    while len(nodes) > 1:
        temp_nodes = []

        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else None
            if right is None:  # Handle odd number of nodes
                # Hash the last node with itself
                node_value = left.hash + left.hash
            else:
                node_value = left.hash + (right.hash if right else '')
            new_node = MerkleNode(None, left, right, hash=hashlib.sha1(node_value.encode()).hexdigest())
            temp_nodes.append(new_node)

        nodes = temp_nodes

    return nodes[0]

# Print out a MerkleTree object starting with the first node
def print_tree(node, indent=''):
    if node is None:
        return

    # Check if the node is a leaf node (has no children)
    if node.left is None and node.right is None:
        print(indent + '-- Leaf Hash: ' + node.hash)
    else:
        print(indent + '|')
        print(indent + '-- Hash: ' + node.hash)
        # Use recursion to print tree starting from the first node
        print_tree(node.left, indent + '   |')
        print_tree(node.right, indent + '   |')

# Create a MerkleTree object with 1-bit hashes
def build_tree_one_bit(file_paths):
    nodes = [MerkleNode(file_path) for file_path in file_paths]

    while len(nodes) > 1:
        temp_nodes = []

        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else None
            if right is None:
                node_value = left.hash[:1] + left.hash[:1]
            else:
                node_value = left.hash[:1] + (right.hash[:1] if right else '')
            new_node = MerkleNode(None, left, right, hash=hashlib.sha1(node_value.encode()).hexdigest()[:1])
            temp_nodes.append(new_node)

        nodes = temp_nodes

    return nodes[0]

# Print out a MerkleTree object with 1-bit hashes, starting with the first node
def print_tree_one_bit(node, indent=''):
    if node is None:
        return

    if node.left is None and node.right is None:
        print(indent + '-- Leaf Hash: ' + node.hash[:1])
    else:
        print(indent + '|')
        print(indent + '-- Hash: ' + node.hash[:1])
        print_tree_one_bit(node.left, indent + '   |')
        print_tree_one_bit(node.right, indent + '   |')

# Create a MerkleTree object with 4-bit hashes
def build_tree_four_bit(file_paths):
    nodes = [MerkleNode(file_path) for file_path in file_paths]

    while len(nodes) > 1:
        temp_nodes = []

        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else None
            if right is None:
                node_value = left.hash[:4] + left.hash[:4]
            else:
                node_value = left.hash[:4] + (right.hash[:4] if right else '')
            new_node = MerkleNode(None, left, right, hash=hashlib.sha1(node_value.encode()).hexdigest()[:4])
            temp_nodes.append(new_node)

        nodes = temp_nodes

    return nodes[0]

# Print out a MerkleTree object with 4-bit hashes, starting with the first node
def print_tree_four_bit(node, indent=''):
    if node is None:
        return

    if node.left is None and node.right is None:
        print(indent + '-- Leaf Hash: ' + node.hash[:4])
    else:
        print(indent + '|')
        print(indent + '-- Hash: ' + node.hash[:4])
        print_tree_four_bit(node.left, indent + '   |')
        print_tree_four_bit(node.right, indent + '   |')

# Compare two different MerkleTree objects print("COLLISION?")
def compare_merkle_trees(tree1, tree2):
    def compare_nodes(node1, node2):
        if node1 is None and node2 is None:
            print("No Change")
        elif node1 is None or node2 is None:
            print("DIFFERENCE")
        elif node1.hash == node2.hash:
            print("No Change")
        else:
            print("DIFFERENCE")

    def compare_tree_nodes(tree1, tree2):
        if tree1 is None and tree2 is None:
            return
        elif tree1 is None or tree2 is None:
            print("DIFFERENCE")
            return
        # Use recursion to reuse code and start with the first node
        compare_nodes(tree1, tree2)
        compare_tree_nodes(tree1.left, tree2.left)
        compare_tree_nodes(tree1.right, tree2.right)

    print("Comparing Merkle Trees:")
    compare_tree_nodes(tree1, tree2)

# Locate any hash collisions within the hash puzzle
def find_collisions_in_merkle_tree(merkle_root, bits):
    def traverse(node, hashes, collisions):
        if node is None:
            return
        
        # Extract the relevant portion of the hash based on bits
        relevant_hash = node.hash[:bits]

      # Check for collision
        if relevant_hash in hashes:
            collisions.append((hashes[relevant_hash], node))
        else:
            hashes[relevant_hash] = node
        
        # Recursively check left and right children
        traverse(node.left, hashes, collisions)
        traverse(node.right, hashes, collisions)

    hashes = {}  # Dictionary to keep track of hashes
    collisions = []  # List to store found collisions

    traverse(merkle_root, hashes, collisions)

    return collisions

# Create a set list of phrases for text files, phrases
phrases = ["Hello world", "Coding is fun"
        , "A.I is awesome", "Python is easy"
        , "I miss c++", "Let's hash something"
        , "Life is beautiful", "Sleep is very nice"
        , "So much coding" , "Praise be the grace period"
        , "Experiencing technical difficulties" , "Anything"
        , "Thirteen is an annoying prime" , "Collisions are interesting"
        , "Happy Birthday To Hash Collisions" , "A very merry unbirthday to alll"]

# Create a set list of text file names, file_paths
# Create a set list of text file names, file_paths
# Create a set list of text file names, file_paths

desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")

file_paths = [
    os.path.join(desktop, f"data{i}.txt")
    for i in ["1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G"]
]

# Populate the text files in file_paths with the words in phrases
file_paths = write_to_files(phrases,file_paths)

# QUESTION ONE
# Build and print a Four-Node MerkleTree object
print("Four-Node Merkle Tree:")
merkle_tree_4 = build_tree(file_paths[0:4])
print_tree(merkle_tree_4)

# Build and print a Six-Node MerkleTree object
print("\nSix-Node Merkle Tree:")
merkle_tree_6 = build_tree(file_paths[0:6])
print_tree(merkle_tree_6)

# Alter the contents of data1.txt
with open(file_paths[0] , 'r') as file:
    contents = file.read()
word = "Hello world today"
with open(file_paths[0] , 'w') as file:
    file.write(word)

# QUESTION TWO
# Build and print a Four-Node MerkleTree object, one node changed
print("Changed Four-Node Merkle Tree:")
merkle_tree_node1changed = build_tree(file_paths[0:4])
print_tree(merkle_tree_node1changed)

# Compare the two Four-Node MerkleTree objects
print("Comparison Result:")
compare_merkle_trees(merkle_tree_4, merkle_tree_node1changed)

# QUESTION THREE AND FOUR
# Generate four-bit hashes to find a collision

for i in range(0, len(phrases), 1 ):
    phrases[i] = phrases[0] + i*" "

file_paths = write_to_files(phrases,file_paths)

print("1-bit tree:")
merkle_tree_8 = build_tree_one_bit(file_paths[:8])
merkle_tree_16 = build_tree_four_bit(file_paths)
print_tree_one_bit(merkle_tree_8)
print("4-bit tree:")
print_tree_four_bit(merkle_tree_16)

# QUESTION FOUR

    # Testing both 1-bit tree and 4-bit tree for our collisions
collisions_1_bit = find_collisions_in_merkle_tree(merkle_tree_8, 1)
collisions_4_bits = find_collisions_in_merkle_tree(merkle_tree_16, 4)

# Check and print results for 1-bit collisions
if collisions_1_bit:
    print("1-bit Collisions Found:")
    for node1, node2 in collisions_1_bit:
        print(f"Collision found between nodes with hashes: {node1.hash[:1]} and {node2.hash[:1]}")
else:
    print("No 1-bit collisions found.")

# Check and print results for 4-bit collisions
if collisions_4_bits:
    print("\n4-bit Collisions Found:")
    for node1, node2 in collisions_4_bits:
        print(f"Collision found between nodes with hashes: {node1.hash[:4]} and {node2.hash[:4]}")
else:
    print("No 4-bit collisions found.")

# For the sake of time and not burning out the CPU for anyone's computer,
# we are going to not do the second portion of question four since that
# would necessitate at minimum 1024 attempts before the odds of finding a
# suitable hash with 20 prefix zeroes rose above 50%. And worst case is
# over a million combinations.
