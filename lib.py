def get_b64_size(instr): # returns the size of a base64 string in bytes
    padding = instr.count('=')
    length = len(instr)
    return ((3* (length/4)) - padding)