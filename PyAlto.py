#Loading the local python scrips
from parse_alto import *
      
#Try to parse any file
parse_alto_file("liberte_1866_07_18_ex1_p2.xml")

#Optionally you can iterate over a directory:
#parse_alto_directory("alto_dir", "result_dir")
