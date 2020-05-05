import re
from parse_alto_class import *


def extract_none(elm):
  if elm is None:
    elm = "None"
  return(elm)


#A function to map each text block of a alto file into a python object containing the main metadata (loc, ocr, etc.)
def block_to_object(block_zone, namespace, list_style):
  
  list_blocks = []

  #####################
  #### TEXT BLOCKS ####
  #####################

  #We iterate over each text block. Additional iterations will focus on composite block and illustration block.
  for block in block_zone.findall(namespace + "TextBlock"):
      type_block = "text"
      style_block = block.get("STYLEREFS")
      #We initialize all the list containing the elements at a word level (content is the actual work, height, the height, wc the ocr word confidence and style the specific style of the word)
      #Each block therefore contain metadata and a list of aligned data.

      #Aligned data at line level.
      id_line = []                  #ID of the line
      line_text = []                #Textual content of a line
      coordinate_line = []          #Coordinates of the line (expressed as height / hpos / width / vpos)

      #Aligned data at text level.
      content_text = []             #Actual content of a token
      id_text = []                  #ID of a token
      id_line_word = []             #ID of the line
      coordinate_text = []          #Coordinates of a token in the original file
      wc_text = []                  #Confidence interval of the OCR
      begin_text = []
      size_text = []
      font_text = []
      font_style = []
      word_start = 0
      
      #Storing the "shape" of the block whenever it exists. Especially useful for drawings.
      shape_block = ""
      shape = block.find(namespace + "Shape")
      if (shape is not None):
        shape = block.find(namespace + "Shape")
        shape_block = shape.find(namespace + "Polygon").get("POINTS")

      #We iterate on every word of every line and retrieve the elements at word level.
      for line in block.findall(namespace + "TextLine"):

        #We get line data.
        line_id = line.get("ID")
        new_line_text = []
        id_line.append(line_id)
#        print(line_id)
#        print(";".join([line.get("HEIGHT"), line.get("HPOS"), line.get("WIDTH"), line.get("VPOS")]))
        coordinate_line.append(";".join([line.get("HEIGHT"), line.get("HPOS"), line.get("WIDTH"), line.get("VPOS")]))

        #We iterate over each word of every line.
        for word in line.findall(namespace + "String"):

          #First we check if the word is hyphenized (very frequent in newspaper writings as column space is limited)
          if word.get("SUBS_TYPE") is None:
            id_text.append(word.get("ID"))
            id_line_word.append(line_id)
            content = word.get("CONTENT")
            new_line_text.append(content)
            content_text.append(content)
            coordinate_text.append(";".join([extract_none(word.get("HEIGHT")), extract_none(word.get("HPOS")), extract_none(word.get("WIDTH")), extract_none(word.get("VPOS"))]))
            wc_text.append(word.get("WC"))
            
            #Retrieving the styles using the style list.
            style_word = word.get("STYLEREFS")
            if style_word is None:
              if style_block is not None:
                style_word = style_block.split(" ")[0]
                index_style = list_style[1].index(style_word)
                size_text.append(list_style[2][index_style])
                font_text.append(list_style[3][index_style])
                font_style.append(list_style[4][index_style])
              else:
                size_text.append("_")
                font_text.append("_")
                font_style.append("_")
            else:
              if " " in style_word:
                style_word = style_word.split(" ")[0]
              index_style = list_style[1].index(style_word)
              size_text.append(list_style[2][index_style])
              font_text.append(list_style[3][index_style])
              font_style.append(list_style[4][index_style])
            if word_start == 0:
              begin_text.append(0)
              word_start = word_start + len(content)
            else:
              begin_text.append(word_start + 1)
              word_start = word_start + 1 + len(content)
          else:
            if word.get("SUBS_TYPE") == "HypPart1":
              hyphen_length = len(word.get("CONTENT"))-1
              id_text.append(word.get("ID") + "/" + str(hyphen_length))
              id_line_word.append(line_id)
              content = word.get("SUBS_CONTENT")
              content_text.append(content)
              coordinate_text.append(";".join([word.get("HEIGHT"), word.get("HPOS"), word.get("WIDTH"), word.get("VPOS")]))
              wc_text.append(word.get("WC"))
              style_word = word.get("STYLEREFS")
              if style_word is None:
                if style_block is not None:
                  style_word = style_block.split(" ")[0]
                  index_style = list_style[1].index(style_word)
                  size_text.append(list_style[2][index_style])
                  font_text.append(list_style[3][index_style])
                  font_style.append(list_style[4][index_style])
                else:
                  size_text.append("_")
                  font_text.append("_")
                  font_style.append("_")
              else:
                index_style = list_style[1].index(style_word)
                size_text.append(list_style[2][index_style])
                font_text.append(list_style[3][index_style])
                font_style.append(list_style[4][index_style])
              if word_start == 0:
                begin_text.append(0)
                word_start = word_start + len(content)
              else:
                begin_text.append(word_start + 1)
                word_start = word_start + 1 + len(content)
            elif word.get("SUBS_TYPE") == "HypPart2":
              if not not id_line_word:
                id_line_word[-1] = id_line_word[-1] + "+" + line_id
              if not not id_text:
                id_text[-1] = id_text[-1] + "+" + word.get("ID")
              if not not coordinate_text:
                coordinate_text[-1] = coordinate_text[-1] + "+" + ";".join([word.get("HEIGHT"), word.get("HPOS"), word.get("WIDTH"), word.get("VPOS")])
            else:
              pass
          
        #We append the text content of a line.
        line_text.append(" ".join(new_line_text).replace('"', '').replace("\t", ""))
      
      #We transfer the lists of word elements and metadata regarding the block to a new_text_block object
      new_text_block = TextBlock(id_text = id_text,
        id_line_word = id_line_word,
        content_text = content_text,
        line_text = line_text,
        coordinate_text = coordinate_text,
        wc_text = wc_text,
        size_text = size_text,
        font_text = font_text,
        font_style = font_style,
        begin_text = begin_text,
        id_line = id_line,
        coordinate_line = coordinate_line,
        height_block = block.get("HEIGHT"),
        width_block = block.get("WIDTH"),
        hpos_block = block.get("HPOS"),
        vpos_block = block.get("VPOS"),
        style_block = style_block,
        shape_block = shape_block,
        type_block = type_block,
        id_block = block.get("ID"),
        id_composed_block = "_")
      
      list_blocks.append(new_text_block)
  
  #######################
  #### ILLUSTRATIONS ####
  #######################

  #We iterate over Illustration block.
  for block in block_zone.findall(namespace + "Illustration"):
    type_block = "illustration"
    shape_block = ""
    shape = block.find(namespace + "Shape")
    if (shape is not None):
      shape_block = shape.find(namespace + "Polygon").get("POINTS")
    new_text_block = TextBlock(id_text = "",
            id_line_word = "",
            line_text = "",
            content_text = "",
            coordinate_text = "",
            wc_text = "",
            size_text = "",
            font_text = "",
            font_style = "",
            begin_text = "",
            id_line = "",
            coordinate_line = "",
            height_block = block.get("HEIGHT"),
            width_block = block.get("WIDTH"),
            hpos_block = block.get("HPOS"),
            vpos_block = block.get("VPOS"),
            style_block = block.get("STYLEREFS"),
            shape_block = shape_block,
            type_block = type_block,
            id_block = block.get("ID"),
            id_composed_block = "_")

    list_blocks.append(new_text_block)
  
  ########################
  #### COMPOSED BLOCK ####
  ########################

  #We iterate over composed block (usually advertisings.)  
  for composed_block in block_zone.findall(".//" + namespace + "ComposedBlock"):
      for block in composed_block.findall(namespace + "TextBlock"):

          type_block = "composed_text"
          style_block = block.get("STYLEREFS")
          #We initialize all the list containing the elements at a word level (content is the actual work, height, the height, wc the ocr word confidence and style the specific style of the word)
          id_line = []
          coordinate_line = []
          id_line_word = []
          line_text = []
          id_text = []
          content_text = []
          coordinate_text = []
          wc_text = []
          size_text = []
          font_text = []
          font_style = []
          begin_text = []
          word_start = 0
      
          #We iterate on every word of every line and retrieve the elements at word level.
          for line in block.findall(namespace + "TextLine"):

            #We get line data.
            line_id = line.get("ID")
            id_line.append(line_id)
            new_line_text = []
            coordinate_line.append(";".join([line.get("HEIGHT"), line.get("HPOS"), line.get("WIDTH"), line.get("VPOS")]))

            for word in line.findall(namespace + "String"):
              if word.get("SUBS_CONTENT") is None:
                id_text.append(word.get("ID"))
                id_line_word.append(line_id)
                content = word.get("CONTENT")
                content_text.append(content)
                new_line_text.append(content)
                coordinate_text.append(";".join([extract_none(word.get("HEIGHT")), extract_none(word.get("HPOS")), extract_none(word.get("WIDTH")), extract_none(word.get("VPOS"))]))
                wc_text.append(word.get("WC"))
                style_word = word.get("STYLEREFS")
                if style_word is None:
                  if style_block is not None:
                    style_word = style_block.split(" ")[0]
                    index_style = list_style[1].index(style_word)
                    size_text.append(list_style[2][index_style])
                    font_text.append(list_style[3][index_style])
                    font_style.append(list_style[4][index_style])
                  else:
                    size_text.append("_")
                    font_text.append("_")
                    font_style.append("_")
                else:
                  if " " in style_word:
                    style_word = style_word.split(" ")[0]
                  index_style = list_style[1].index(style_word)
                  size_text.append(list_style[2][index_style])
                  font_text.append(list_style[3][index_style])
                  font_style.append(list_style[4][index_style])
                if word_start == 0:
                  begin_text.append(0)
                  word_start = word_start + len(content)
                else:
                  begin_text.append(word_start + 1)
                  word_start = word_start + 1 + len(content)
              else:
                if word.get("SUBS_CONTENT") == "HypPart1":
                  hyphen_length = len(word.get("CONTENT"))+1
                  id_text.append(word.get("ID") + "/" + str(hyphen_length))
                  id_line_word.append(line_id)
                  content = word.get("SUBS_CONTENT")
                  content_text.append(content)
                  coordinate_text.append(";".join([word.get("HEIGHT"), word.get("HPOS"), word.get("WIDTH"), word.get("VPOS")]))
                  wc_text.append(word.get("WC"))
                  style_word = word.get("STYLEREFS")
                  if style_word is None:
                    if style_block is not None:
                      style_word = style_block.split(" ")[0]
                      index_style = list_style[1].index(style_word)
                      size_text.append(list_style[2][index_style])
                      font_text.append(list_style[3][index_style])
                      font_style.append(list_style[4][index_style])
                    else:
                      size_text.append("_")
                      font_text.append("_")
                      font_style.append("_")
                  else:
                    index_style = list_style[1].index(style_word)
                    size_text.append(list_style[2][index_style])
                    font_text.append(list_style[3][index_style])
                    font_style.append(list_style[4][index_style])
                  if word_start == 0:
                    begin_text.append(0)
                    word_start = word_start + len(content)
                  else:
                    begin_text.append(word_start + 1)
                    word_start = word_start + 1 + len(content)
                elif word.get("SUBS_TYPE") == "HypPart2":
                  try:
                    id_line_word[-1] = id_line_word[-1] + "+" + line_id
                  except IndexError: #In some very rare case there is a line index error.
                    id_line_word = ["0+" + line_id]
                  try:
                    id_text[-1] = id_text[-1] + "+" + word.get("ID")
                  except IndexError:
                    id_text = ["0+" + word.get("ID")]
                  try:
                    coordinate_text[-1] = coordinate_text[-1] + "+" + ";".join([word.get("HEIGHT"), word.get("HPOS"), word.get("WIDTH"), word.get("VPOS")])
                  except IndexError:
                    coordinate_text = ["0+" + ";".join([word.get("HEIGHT"), word.get("HPOS"), word.get("WIDTH"), word.get("VPOS")])]
                else:
                  pass
              
              #We append the text content of a line.
            line_text.append(" ".join(new_line_text).replace('"', '').replace("\t", ""))
          
          #We transfer the lists of word elements and metadata regarding the block to a new_text_block object
          new_text_block = TextBlock(id_text = id_text,
            id_line_word = id_line_word,
            line_text = line_text,
            content_text = content_text,
            coordinate_text = coordinate_text,
            wc_text = wc_text,
            size_text = size_text,
            font_text = font_text,
            font_style = font_style,
            begin_text = begin_text,
            id_line = id_line,
            coordinate_line = coordinate_line,
            height_block = block.get("HEIGHT"),
            width_block = block.get("WIDTH"),
            hpos_block = block.get("HPOS"),
            vpos_block = block.get("VPOS"),
            style_block = style_block,
            shape_block = "",
            type_block = type_block,
            id_block = block.get("ID"),
            id_composed_block = composed_block.get("ID"))
          
          list_blocks.append(new_text_block)

      ###############################
      #### COMPOSED ILLUSTRATION ####
      ###############################
    
      for block in composed_block.findall(namespace + "Illustration"):
            type_block = "composed_illustration"
            
            new_text_block = TextBlock(id_text = "",
                id_line_word = "",
                content_text = "",
                coordinate_text = "",
                wc_text = "",
                size_text = "",
                font_text = "",
                font_style = "",
                begin_text = "",
                line_text = "",
                id_line = "",
                coordinate_line = "",
                height_block = block.get("HEIGHT"),
                width_block = block.get("WIDTH"),
                hpos_block = block.get("HPOS"),
                vpos_block = block.get("VPOS"),
                style_block = block.get("STYLEREFS"),
                shape_block = "",
                type_block = type_block,
                id_block = block.get("ID"),
                id_composed_block = composed_block.get("ID"))
    
            list_blocks.append(new_text_block)
      #Alternative: sometimes the illustration appears under graphical element
      for block in composed_block.findall(namespace + "GraphicalElement"):
            type_block = "composed_illustration"
            
            new_text_block = TextBlock(id_text = "",
                id_line_word = "",
                content_text = "",
                coordinate_text = "",
                wc_text = "",
                size_text = "",
                font_text = "",
                font_style = "",
                begin_text = "",
                line_text = "",
                id_line = "",
                coordinate_line = "",
                height_block = block.get("HEIGHT"),
                width_block = block.get("WIDTH"),
                hpos_block = block.get("HPOS"),
                vpos_block = block.get("VPOS"),
                style_block = composed_block.get("STYLEREFS"),
                shape_block = "",
                type_block = type_block,
                id_block = block.get("ID"),
                id_composed_block = composed_block.get("ID"))
    
            list_blocks.append(new_text_block)
      
  return(list_blocks)

def block_to_alto(list_blocks, alto_file, alto_data):
  block_metadata = []
  block_text = []
  ocr_data = []
  n_block = 0
  for block in list_blocks:
    n_block = n_block + 1
    block_metadata.append("\t".join([alto_file, str(block.id_composed_block), str(block.id_block), str(block.type_block), str(block.height_block), str(block.width_block), str(block.hpos_block), str(block.vpos_block), str(block.shape_block), str(block.style_block)]))
    for begin_text, height_text, wc_text in zip(block.begin_text, block.height_text, block.wc_text):
      ocr_data.append("\t".join([alto_file, str(block.id_composed_block), str(block.id_block), str(block.type_block), str(begin_text), str(height_text), str(wc_text)]))
    for token in block.content_text:
      if token == '"':
        token_text = '/"/'
      elif '"' in token:
        token_text = re.sub('"', '', token)
      else:
        token_text = token
      if token != "":
        block_text.append("\t".join([alto_file, str(block.id_composed_block), str(block.id_block), str(block.type_block), token_text]))
  alto_data.block_metadata.extend(block_metadata)
  alto_data.ocr_data.extend(ocr_data)
  alto_data.ocr_text.extend(block_text)
  return(alto_data)

def extract_ngram(ngram, ngram_size, sample_rate):
    #Dealing with the ngram.
    ngram_list = []
    ngram_index = 0
    
    #Some cleaning (as ocr recognition limitation makes punctuation troublesome)
    ngram_block = re.sub("[\.,\?\!]", "", " ".join(block.content_text)).lower()
    ngram_block = re.sub("['\(\)\[\]\<\>/;:\^-]", " ", ngram_block)
    ngram_block = ngram_block.replace('"', ' ').replace("\\", " ")
    ngram_block = re.sub(" +", " ", ngram_block).split(" ")
    
    #We iterate through every word that match the sample rate and takes a slice of words corresponding to ngram_size.
    for content_text in ngram_block:
      if (((ngram_index % sample_rate) == 0) & ((ngram_index + ngram_size) <= len(ngram_block))):
        ngram_list.append("\t".join([file_name, str(block.id_composed_block), str(block.id_block), " ".join(ngram_block[ngram_index:ngram_index+4])]))
      ngram_index = ngram_index + 1
    
    ngram.extend(ngram_list)

def everything_to_alto(list_blocks, alto_file, alto_data):
  #We initiate all the list to me transformed into tables or processed data.
  block_metadata = []
  block_text = []
  ocr_data = []
  line_metadata = []
  complete_text = []
  ngram = []
  n_block = 0
  length_text = 0

  #We iterate every ocr block in list_blocks and append them to create block_metadata.
  for block in list_blocks:
    n_block = n_block + 1
    content_text_block = " ".join(block.content_text)
    content_text_block = re.sub('"', '', content_text_block)
    
    block_metadata.append("\t".join([alto_file, str(block.id_composed_block), str(block.id_block), str(block.type_block), str(block.height_block), str(block.width_block), str(block.hpos_block), str(block.vpos_block), str(block.shape_block), str(block.style_block), content_text_block]))
        #Within each block we extract all the metadata of the words using zip to iterate on every list.
    for id_text, id_line_word, begin_text, coordinate_text, wc_text, size_text, font_text, font_style, content_text in zip(block.id_text, block.id_line_word, block.begin_text, block.coordinate_text, block.wc_text, block.size_text, block.font_text, block.font_style, block.content_text):
      ocr_data.append("\t".join([alto_file, str(length_text), str(block.id_composed_block), str(block.id_block), str(block.type_block), str(id_line_word), str(id_text), re.sub('"|“', '', str(content_text)), str(coordinate_text), str(wc_text), str(size_text), str(font_text), str(font_style)]))
      length_text = length_text + len(content_text) + 1
    
    #Dealing with the ngram. Might be better with a function.
    ngram_list = []
    ngram_index = 0
    ngram_block = re.sub("[\.,\?\!]", "", " ".join(block.content_text)).lower()
    ngram_block = re.sub("['\(\)\[\]\<\>/;:\^\-•«»—\{\}\~■®\*#°%♦_]", " ", ngram_block)
    ngram_block = ngram_block.replace('"', ' ').replace("\\", " ")
    ngram_block = re.sub(" +", " ", ngram_block).split(" ")
    for content_text in ngram_block:
      if (((ngram_index % 5) == 0) & ((ngram_index+4) <= len(ngram_block))):
        ngram_list.append("\t".join([alto_file, str(block.id_composed_block), str(block.id_block), " ".join(ngram_block[ngram_index:ngram_index+4])]))
      ngram_index = ngram_index + 1
    
    ngram.extend(ngram_list)
    
    for id_line, line_text, coordinate_line in zip (block.id_line, block.line_text, block.coordinate_line):
      line_metadata.append("\t".join([alto_file, str(block.id_composed_block), str(block.id_block), str(id_line), str(coordinate_line), str(line_text)]))
    #We merge all the text to be sent to parse_alto_extract. Having all the text in one batch save up a lot of time!

  alto_data.block_metadata.extend(block_metadata)
  alto_data.ocr_text.extend(ocr_data)
  alto_data.line_metadata.extend(line_metadata)
  alto_data.ngram.extend(ngram)
  return(alto_data)

