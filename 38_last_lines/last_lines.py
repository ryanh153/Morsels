def last_lines(filepath):
    block_size = 8192  # work in blocks of this many bytes
    block_number = -1
    end_reached = False

    with open(filepath, 'rb') as f:
        f.seek(0, 2)  # offset = 0, starting from end of file
        block_end_byte = f.tell()  # get where we are (end of last block currently)

        while not end_reached:
            if (block_end_byte - block_size) > 0:
                #  More than one block left in file so parse one block at a time
                f.seek(block_number*block_size, 2)  # Go to the appropriate block
                block_end_byte = f.tell()  # remember this position for next loop
                lines = f.readlines(block_size)[1:]  # read that block, ignoring first line since it may be partial
                yield from (l.decode('utf-8') for l in reversed(lines))
                block_number -= 1
            else:
                # File is smaller than a block, or less than one block left
                f.seek(0, 0)  # go to start
                lines = f.readlines(block_end_byte+1)  # read until end or the start of the last block processed
                yield from (l.decode('utf-8') for l in reversed(lines))
                end_reached = True
