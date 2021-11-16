#!/usr/bin/python3

import io
import math

def p(i, start, end):
    ss = i/2
    mm = math.floor(ss / 60)
    ss = ss - (mm * 60)
    hh = math.floor(mm / 60)
    mm = mm - (hh * 60)
    fn = f'frame{i:05d}_{hh}h{mm:02d}m{ss:04.1f}s'
    print(f'tail -c +{start+1} vid.psf | head -c {end-start} > {fn}.raw && hexdump -C {fn}.raw > {fn}.hex')

with open("vid.psf","rb") as file:
    file.seek(0, io.SEEK_END)
    fend = file.tell()
    pavs = 0
    i = 0
    for pos in range(16, fend-4, 16):
        file.seek(pos, io.SEEK_SET)
        bytes = file.read(4)
        if bytes[0:4] == b'\x50\x41\x56\x53': # PAVS
            p(i, pavs, pos)
            pavs = pos
            i += 1
    p(i, pavs, fend)
