from AoC import AoC
from itertools import zip_longest
from tqdm import tqdm
import numpy as np

class Solver(AoC):
    example_data = """2333133121414131402"""


    def parse(self):
        self.tqdm_total = 0
        raw = self.read_input_txt()[0].strip()
        self.debug(raw)
        self.files = np.array([int(b) for b in raw[0::2]], dtype=np.uint32)
        self.free_space = np.array([int(b) for b in raw[1::2]], dtype=np.uint32)

    def part1(self):
        """
        """
        hdd = np.zeros(self.files.sum(), dtype=np.uint32)
        self.debug(f'HDD Size: {hdd.size}')
        pbar = tqdm(total=self.files.sum(), ncols=100)
        file_id = 0
        insert_file_id = len(self.files)-1
        free_space_id = 0
        block_counter = 0
        insert_file_counter = 0
        insert = False
        for i in range(len(hdd)):
            #self.debug(hdd)
            while True:
                if not insert:
                    if block_counter < self.files[file_id]:
                        hdd[i] = file_id
                        block_counter += 1
                        break
                    else:
                        block_counter = 0
                        file_id += 1
                        insert = True
                else:
                    if block_counter < self.free_space[free_space_id]:
                        if insert_file_counter < self.files[insert_file_id]:
                            hdd[i] = insert_file_id
                            block_counter += 1
                            insert_file_counter += 1
                            break
                        else:
                            insert_file_counter = 0
                            insert_file_id -= 1
                            hdd[i] = insert_file_id
                            block_counter += 1
                            insert_file_counter += 1
                            break
                    else:
                        block_counter = 0
                        free_space_id += 1
                        insert = False
            pbar.update(1)

        # compute checksum
        pbar.close()
        chk = 0
        for (i, n) in enumerate(hdd):
            chk += i*int(n)
        self.debug(hdd)
        return chk

    def part2(self):
        """
        """
        # Now we need to track absolute position of each file and free space
        files = []
        free_space = []
        hdd_pos = 0
        file_id = 0
        for (fi, fr) in zip_longest(self.files, self.free_space):
            if fi:
                files.append((hdd_pos, fi, file_id))
                hdd_pos += fi
                file_id += 1
            if fr:
                free_space.append((hdd_pos, fr))
                hdd_pos += fr
        self.debug(files)
        self.debug(free_space)
        pbar = tqdm(total=len(files), ncols=100)
        
        for (f_pos, f_size, f_id) in files.copy()[::-1]:
            for i in range(len(files)-1):
                new_pos = files[i][0] + files[i][1]
                if new_pos >= f_pos:
                    break
                if f_size <= files[i+1][0] - new_pos:
                    # if current file fits between files at i and i+1
                    files.remove((f_pos, f_size, f_id))
                    files.insert(i+1, (new_pos, f_size, f_id))
                    break
            pbar.update(1)
        pbar.close()
        # compute checksum
        chk = 0
        for (f_pos, f_size, f_id) in files:
            for i in range(f_size):
                chk += (f_pos + i) * int(f_id)
        self.debug(f'final files: {files}')
        return chk
