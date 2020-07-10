import io
import os


def last_lines(filepath, *, block_size=io.DEFAULT_BUFFER_SIZE):
    block_number = -1
    with open(filepath, 'rb') as f:
        block_end_byte = f.seek(0, os.SEEK_END)  # offset = 0, starting from end of file
        while True:
            if (block_end_byte - block_size) > 0:  # More than one block left in file, parse next block
                block_end_byte = f.seek(block_number*block_size, os.SEEK_END)  # Go to the appropriate block
                lines = f.readlines(block_size)[1:]  # read that block, ignoring first line since it may be partial
                yield from (l.decode('utf-8') for l in reversed(lines))
                block_number -= 1
            else:  # File is smaller than a block, or less than one block left
                f.seek(0, os.SEEK_SET)  # go to start
                lines = f.readlines(block_end_byte+1)  # read until end or the start of the last block processed
                yield from (l.decode('utf-8') for l in reversed(lines))
                break
