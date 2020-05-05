#Loading the local python scrips
from parse_alto_class import *
from parse_alto_main import *
from lxml import etree
import zipfile

#A function to get the styles
def extract_style(style_alto, alto_file, namespace):

  #We initialize the columns of the tsv file

  list_style = []
  list_style_id = []
  list_style_size = []
  list_style_font = []
  list_style_fontstyle = []

  #We iterate on every <TextStyle> xml object and extract the id, font size and font family from the attribute.
  for text_style in style_alto.findall(namespace + "TextStyle"):
    style_id = text_style.get("ID")
    style_size = text_style.get("FONTSIZE")
    style_font = text_style.get("FONTFAMILY")
    if text_style.get("FONTSTYLE") is not None:
      style_fontstyle = text_style.get("FONTSTYLE")
    else:
      style_fontstyle = "_"
    list_style.append("\t".join([alto_file, style_id, style_size, style_font, style_fontstyle]))
    list_style_id.append(style_id)
    list_style_size.append(style_size)
    list_style_font.append(style_font)
    list_style_fontstyle.append(style_fontstyle)

  #The list becomes a linebreak separated file and is written to a style file.

  return([list_style, list_style_id, list_style_size, list_style_font, list_style_fontstyle])


def extract_alto(alto_file, spacy_data):
  
  alto_content = open(alto_file, "rb").read()
  
  #A recurrent error in xml files from the BNF: the encoding is declared as encoding="ISO-8859-1" where it is really unicode
  
  alto_content = alto_content.decode().replace('encoding="ISO-8859-1"', 'encoding="UTF-8"').encode()
  
  
  if 1==1:
    
    xml_alto = etree.fromstring(alto_content)
  
    namespace = xml_alto.tag
    if '}' in namespace:
      namespace = namespace.split('}')[0] + "}"
    else:
      namespace = ""
      
    #Extract description
    description = xml_alto.find(namespace + "Description")
    
    #Extract styles
    style = xml_alto.find(namespace + "Styles")
  
    style = extract_style(style, alto_file, namespace)
  
    spacy_data.style.extend(style[0])
  
    #Extract pages
    page = xml_alto.find(namespace + "Layout").find(namespace + "Page")
  
    #Extract Header. Will be None type if there is none.
    header = page.find(namespace + "TopMargin")
  
    #Extract main text.
    main = page.find(namespace + "PrintSpace")
  
    main_objects = block_to_object(main, namespace, style)
    spacy_data = everything_to_alto(main_objects, alto_file, spacy_data)
  
  else:
    print("0")
  
  return(spacy_data)
