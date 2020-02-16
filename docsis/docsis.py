from ctypes import *;
from ctypes.util import find_library

libdocsis_path = None
libdocsis = None
char_pointer = POINTER(c_ubyte)
char_pointer_pointer = POINTER(POINTER(c_ubyte))
libc = CDLL(find_library('c'))

def set_libdocsis_path(path):
	global libdocsis_path
	libdocsis_path = path

def load_libdocsis():
	global libdocsis, libdocsis_path
	if libdocsis_path is None:
		libdocsis_path = './libdocsis.so'
	libdocsis = cdll.LoadLibrary(libdocsis_path)

def encode_content(content, key, encode_docsis=True, hash= 0):
	#hash = 2 means eu
	#hash = 1 means na
	global libdocsis, libc
	if libdocsis is None:
		raise Exception('You have to load libdocsis first!')
	p = char_pointer()
	p1 = char_pointer_pointer(p)
	output_size = libdocsis.encode_file(content, len(content),p1, key,len(key),1 if encode_docsis else 0,hash) 
	if output_size == 0: raise Exception('Unable to encode file')
	ret = ''.join(chr(p1.contents[i]) for i in range(output_size))
	libc.free(p)
	return ret


if __name__ == '__main__':
	load_libdocsis()
	ifile = file('docsis.txt', 'rb')
	content = ifile.read()
	ret = encode_content(content, 'a key', encode_docsis=True, hash= 1)
	out = open('docsis.bin', 'wb')
	out.write(ret)
	out.close()



