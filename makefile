SOURCE	= Huffman.py
PY		= python3

all:
	$(PY) $(SOURCE)

clean:
	rm -f output.txt