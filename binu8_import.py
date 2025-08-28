# -*- coding:utf-8 -*-

import struct
import os
import io
from pathlib import Path


def byte2int(byte: bytes) -> int:
	long, = struct.unpack("<L", byte)
	return long


def dumpstr(src: io.BufferedReader) -> str:
	length, = struct.unpack("<I", src.read(4))  # pascal string
	bstr = src.read(length)
	assert bstr[-1] == 0  # pascal string should be null-terminated
	# return str and remove trailing null bytes
	return bstr.decode("utf-8").rstrip("\x00")


def dumptxt(src: io.BufferedReader, offset: int, count: int) -> list[str]:
	src.seek(offset, os.SEEK_SET)
	str_list = []
	for _ in range(count):
		# str_list.append(dumpstr(src).replace("\n", "\\n").replace("\r", "\\r"))
		str_list.append(dumpstr(src))
	return str_list


def main(src_folder: Path):
	# make new dest folder
	dest_folder = src_folder.parent / "Output" / (src_folder.name)
	dest_folder.mkdir(parents=True, exist_ok=True)

	f_lst = [file_path for file_path in src_folder.rglob("*.binu8") if file_path.name != "__global.binu8"]

	for fn in f_lst:
		src = fn.open("rb")
		txt = fn.with_suffix(".txt").open("r", encoding="utf-8")
		filesize = fn.stat().st_size
		# src.seek(4)
		# entry_count = byte2int(src.read(4))
		# str_offset = (entry_count << 1) * 4 + 8
		header = src.read(9)
		VER_MAGIC = b"VER"
		# does it start with version (no length prefix)
		if header[:3] == VER_MAGIC:
			src.seek(9, os.SEEK_SET)
			unk_count = byte2int(src.read(4))
			src.seek(unk_count * 4, os.SEEK_CUR)
		# does it start with version (length prefixed)
		elif header[0] == 9 and header[4:7] == VER_MAGIC:
			src.seek(13, os.SEEK_SET)
			unk_count = byte2int(src.read(4))
			src.seek(unk_count * 4, os.SEEK_CUR)
		# if it doesnt start with version
		else:
			src.seek(0, os.SEEK_SET)

		init_code_count = byte2int(src.read(4))
		src.seek(init_code_count * 8, os.SEEK_CUR)
		code_count = byte2int(src.read(4))
		src.seek(code_count * 8, os.SEEK_CUR)
		str_count = byte2int(src.read(4))

		str_offset = src.tell()
		src.seek(0)
		data = src.read(str_offset)
		dst = (dest_folder / fn.stem).with_suffix(".binu8").open("wb")
		dst.write(data)
		dst.write(struct.pack("<LB", 1, 0))

		rows = txt.readlines()
		for i, row in enumerate(rows):
			if row[0] != "●":
				continue
			if i + 1 < len(rows):
				row = rows[i + 1].rstrip("\r\n").replace("\\n", "\n").replace("\\r", "\r") + "\x00"
				str_bytes = bytes(row, "utf-8")
				dst.write(struct.pack("<L", len(str_bytes)))
				dst.write(struct.pack(f"{len(str_bytes)}s", str_bytes))

		src.seek(str_offset)
		_ = dumptxt(src, src.tell(), str_count)

		data = src.read(filesize - src.tell())
		dst.write(data)
		src.close()
		dst.close()
		txt.close()

	print(f"Import completed successfully with {len(f_lst)} files processed.")


if __name__ == "__main__":
	import sys

	if len(sys.argv) != 2:
		print("Usage: python binu8_import.py <pac_unpack folder>")
		sys.exit(1)

	src_folder = Path(sys.argv[1])

	if not src_folder.exists():
		print(f"Error: Folder '{src_folder}' not found!")
		sys.exit(1)

	try:
		main(src_folder)
	except Exception as e:
		print(f"Error during dump: {e}")
		import traceback

		traceback.print_exc()
		sys.exit(1)
