# -*- coding:utf-8 -*-

import struct
import os
import pathlib

path = pathlib.Path('./')

def walk(adr):
	mylist=[]
	for root,dirs,files in os.walk(adr):
		for name in files:
			if name[-4:] != '.bin':
				continue
			if name == '__global.bin':
				continue
			adrlist=os.path.join(root, name)
			mylist.append(adrlist)
	return mylist

def byte2int(byte):
	long_tuple=struct.unpack('<L',byte)
	long = long_tuple[0]
	return long

def dumpstr(src):
	bstr = b''
	c = src.read(1)
	while c != b'\x00':
		bstr += c
		c = src.read(1)
	return bstr.decode('utf-8')
	
def dumptxt(src, offset, count):
	src.seek(offset)
	str_list = []
	for i in range(0, count):
		str_list.append(dumpstr(src))
	return str_list

def main():
	f_lst = walk('Script.pac_unpack')

	for fn in f_lst:
		src = open(fn, 'rb') # origin bin file
		print('Open',fn)
		
		dstname = fn[:-4] + '.txt'
		txt = open(dstname, 'r', encoding='utf-8') # exported txt file
		print('Open',dstname)
		
		filesize=os.path.getsize(fn)
		src.seek(4+17) # header 17bytes + 4bytes
		entry_count = byte2int(src.read(4))
		#print(entry_count)
		str_offset = (entry_count << 1) * 4 + 8 + 17 # where strings begin
		src.seek(0)
		data=src.read(str_offset + 5)
		dst = open(path.joinpath(fn[:-4]+'.bin'),'wb') # new bin file
		dst.write(data)
		for rows in txt:
			if rows[0] != '●':
				continue
			row = txt.readline().rstrip('\r\n').replace('\\n', '\n').replace('\\r', '\r')
			str = bytes(row, 'utf-8')
			#dst.write(struct.pack('L', len(str)+1)) # write string len + \x00
			#dst.write(struct.pack("B", str)) # write string as bytes
			dst.write(str)
			dst.write(struct.pack('B',0)) # write \x00

		src.seek(str_offset)
		str_count = byte2int(src.read(4))
		dumptxt(src, src.tell()+1, str_count-1)
		data=src.read(filesize-src.tell())
		dst.write(data)
		src.close()
		dst.close()
		txt.close()

main()