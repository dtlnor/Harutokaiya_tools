import struct
import os
import io
from pathlib import Path


def byte2int(byte: bytes) -> int:
	long, = struct.unpack("<L", byte)
	return long


def int2byte(num: int) -> bytes:
	return struct.pack("L", num)


def FormatString(string: str, count: int) -> str:
	res = f"○{count:08d}○\n{string}\n●{count:08d}●\n{string}\n\n"

	return res


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
		str_list.append(dumpstr(src).replace("\n", "\\n").replace("\r", "\\r"))
	return str_list


def main(src_folder: Path):
	f_lst = [file_path for file_path in src_folder.rglob("*.binu8") if file_path.name != "__global.binu8"]
	for fn in f_lst:
		src = fn.open("rb")
		dstname = fn.with_suffix(".txt")
		dst = dstname.open("w", encoding="utf-8")

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

		str_list = dumptxt(src, src.tell(), str_count)
		assert str_list[0] == ""  # first string is always empty
		str_list = str_list[1:]

		for i, string in enumerate(str_list):
			dst.write(FormatString(string, i))

		src.close()
		dst.close()


if __name__ == "__main__":
	import sys

	src_folder = Path(sys.argv[1])
	main(src_folder)
