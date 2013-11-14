#!/usr/bin/env python
#############################################################
# ubi_reader/ubifs
# (c) 2013 Jason Pruitt (jrspruitt@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#############################################################
import lzo
import struct
import zlib
from ubifs.defines import *

# For happy printing
ino_types = ['file', 'dir','lnk','blk','chr','fifo','sock']
node_types = ['ino','data','dent','xent','trun','pad','sb','mst','ref','idx','cs','orph']
key_types = ['ino','data','dent','xent']


def parse_key(key):
    """Parse node key

    Arguments:
    Str:key    -- Hex string literal of node key.

    Returns:
    Int:key_type   -- Type of key, data, ino, dent, etc.
    Int:ino_num    -- Inode number.
    Int:khash      -- Key hash.
    """
    lkey, hkey = struct.unpack('<II',key[0:UBIFS_SK_LEN])
    ino_num = lkey & UBIFS_S_KEY_HASH_MASK
    key_type = hkey >> UBIFS_S_KEY_BLOCK_BITS
    khash = hkey

    #if key_type < UBIFS_KEY_TYPES_CNT:
    return {'type':key_type, 'ino_num':ino_num, 'khash': khash}


def decompress(ctype, unc_len, data):
    """Decompress data.

    Arguments:
    Int:ctype    -- Compression type LZO, ZLIB (*currently unused*).
    Int:unc_len  -- Uncompressed data lenth.
    Str:data     -- Data to be uncompessed.

    Returns:
    Uncompressed Data.
    """
    if ctype == UBIFS_COMPR_LZO:
        return lzo.decompress(''.join(('\xf0', struct.pack('>I', unc_len), data)))
    elif ctype == UBIFS_COMPR_ZLIB:
        return zlib(decompress(data))
    else:
        return data

