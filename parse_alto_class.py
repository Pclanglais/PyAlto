

#A function to identify the original dir in R Studio
def identify_dir(collection, id_work, id_year, id_month, id_day):
  id_date = id_year + "_" + id_month + "_" + id_day
  work_location = "collection/" + collection + "/" + id_work
  date_location = id_work + "_" + id_year + "/" + id_work + "_" + id_year + "_" + id_month + "/" + id_work + "_" + id_date
  dirname = "/data/user/l/pclanglais/" + work_location + "/" + date_location
  return(dirname)

# A class to store all the elements regarding the location of a doc.
class DocIndex(object):

    def __init__(self, collection, work, year, month, day, page):
        self.collection = collection
        self.work = work
        self.year = year
        self.month = month
        self.day = day
        self.page = page.split("_")
        self.directory = identify_dir(collection, work, year, month, day)
  
#doc_id = DocIndex(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])


# A class to store all the elements regarding a text block
class TextBlock(object):

    def __init__(self, id_text, id_line_word, line_text, content_text, coordinate_text, wc_text, size_text, font_text, font_style, begin_text, id_line, coordinate_line, height_block, width_block, hpos_block, vpos_block, style_block, shape_block, type_block, id_block, id_composed_block):
        self.id_text = id_text
        self.id_line_word = id_line_word
        self.line_text = line_text
        self.content_text = content_text
        self.coordinate_text = coordinate_text
        self.wc_text = wc_text
        self.size_text = size_text
        self.font_text = font_text
        self.font_style = font_style
        self.begin_text = begin_text
        self.id_line = id_line
        self.coordinate_line = coordinate_line
        self.height_block = height_block
        self.width_block = width_block
        self.hpos_block = hpos_block
        self.vpos_block = vpos_block
        self.style_block = style_block
        self.shape_block = shape_block
        self.type_block = type_block
        self.id_block = id_block
        self.id_composed_block = id_composed_block


# A class to store all the elements regarding a text block
class DataAlto(object):

    def __init__(self, style, block_metadata, line_metadata, ocr_text, ngram):
        self.style = style
        self.block_metadata = block_metadata
        self.line_metadata = line_metadata
        self.ocr_text = ocr_text
        self.ngram = ngram

