# PyAlto
A small python application to transform an ALTO file into a set of textual data

To use it you just need to add the name of the file at the end of parse_alto.py, inside parse_alto_file.

PyAlto will generate several files that can be useful for different text mining applications:
* A dataset of text blocks and illustrations with their associated coordinates and metadata.
* A dataset of text lines with their associated coordinates and metadata.
* A dataset of words with their associated coordinates, OCR quality rate, style format and metadata.
* A dataset of word ngrams (that can be used for instance for reprinting detection).
