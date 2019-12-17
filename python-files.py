# Open file with open. Mode can be 'r' (read), 'w' (write) or 'a' (append):
f = open("resources/portland-oregon-crime-data.csv", "r")

# Attributes and functions
print("File info. Mode: {}. Name: {}. Closed? {}".format(f.mode, f.name, f.closed))

# Close file
f.close()

# Open file using with. Automatically closes file after block:
with open('/tmp/file.txt', 'w') as f:
    f.name
    print(f.read())

# Print file contents, line by line:
for line in f:
    print(f)

# Read the whole file as a string:
filecontents = f.read()

# Get lines of file as a list:
lst_lines = f.readlines()
print("Lines in file: {}".format(len(lst_lines)))

# Print next n characters:
f.read(10)

# Write into a file (must be open in mode w):
f.write("OK")
