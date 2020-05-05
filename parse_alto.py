#Loading the local python scrips
from parse_alto_class import *
from parse_alto_extract import *
import os


#A function to write the textual data files into the directory of each issue of a newspaper
def write_alto_data(final_file_name, end_file, alto_data, zip_file = False):
  final_file_name = final_file_name + "_" + end_file + ".tsv"
  with open(final_file_name, "w") as f:
    f.write(alto_data)
  if zip_file:
    zipfile.ZipFile(final_file_name.replace(".tsv", ".zip"), 'w', zipfile.ZIP_DEFLATED).write(final_file_name)
    os.remove(final_file_name)

#A function to generate all the data files compiling ALTO and Spacy outputs.
def parse_alto_file(file_name, zip_file = False):
  
  alto_data = DataAlto(style = ["\t".join(["work", "date", "issue", "page", "id_style", "size", "font"])], 
          block_metadata = ["\t".join(["work", "date", "issue", "page", "composed_block", "block", "type", "height", "width", "hpos", "vpos", "shape", "id_style_meta", "text"])],
          line_metadata = ["\t".join(["work", "date", "issue", "page", "composed_block", "block", "id_line", "coordinate_line", "line_text"])],
          ocr_text = ["\t".join(["work", "date", "issue", "page", "length_text", "composed_block", "block", "type", "id_line", "id_word", "original_word", "coordinate_word", "ocr", "size_text", "font_text", "font_style"])],
          ngram = ["\t".join(["work", "date", "issue", "page", "composed_block", "block", "ngram"])])
      
  #We parse the alto using extract_alto
  alto_data = extract_alto(file_name, alto_data)

  #Removing the end file in .xml
  final_file_name = file_name[:-4]
      
  write_alto_data(final_file_name, "style", "\n".join(alto_data.style), zip_file)
  write_alto_data(final_file_name, "block_metadata", "\n".join(alto_data.block_metadata), zip_file)
  write_alto_data(final_file_name, "line_metadata", "\n".join(alto_data.line_metadata), zip_file)
  write_alto_data(final_file_name, "ocr_text", "\n".join(alto_data.ocr_text), zip_file)
  write_alto_data(final_file_name, "ngram", "\n".join(alto_data.ngram), zip_file)
      

parse_alto_file("liberte_1866_07_18_ex1_p2.xml")