from ctypes import *;
from ctypes.util import find_library
from threading import Lock

libdocsis_path = None
libdocsis = None
char_pointer = POINTER(c_ubyte)
char_pointer_pointer = POINTER(POINTER(c_ubyte))
libc = CDLL(find_library('c'))
lib_lock = Lock()

def set_libdocsis_path(path):
	lib_lock.acquire()
	global libdocsis_path
	libdocsis_path = path
	lib_lock.release()

def load_libdocsis():
	lib_lock.acquire()
	global libdocsis, libdocsis_path
	if libdocsis is not None:
		return
	if libdocsis_path is None:
		libdocsis_path = './libdocsis.so'
	libdocsis = cdll.LoadLibrary(libdocsis_path)
	libdocsis.initialize()
	lib_lock.release()

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
	
	if len(ret) == 0: raise Exception('Unable to encode file')
	return ret


if __name__ == '__main__':
	load_libdocsis()
	ifile = open('docsis.txt', 'rb')
	content = ifile.read()
	print(content)
	ret = encode_content(content, 'a key', encode_docsis=True, hash= 0)
	out = open('docsis.bin', 'wb')
	#print(ret)
	out.write(ret.encode('utf8'))
	out.close()



