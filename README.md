# python-docsis
a library to compile human readable docsis to binary

You need to have libdocsis built:
https://github.com/federicoemartinez/libdocsis

Usage:
- Get the shared library libdocsis.
```python
from docsis import docsis 

docsis.load_libdocsis()
content = DOCSIS_TEXT_CONTENT
ret = encode_content(content, KEY_TO_USE, encode_docsis=True, hash= 1) # hash can be 0,1,2 for no hash, eu,na
```
