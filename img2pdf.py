# -*- coding: utf-8 -*-

'''
feature : convert multi images to a pdf  
date    : 20230210
'''

# import
from PIL import Image
import os
import PyPDF2
import shutil

# combine the images in a given folder to a pdf file
def combine_imgs_pdf(folder, pdfFile):
    print('start converting')
    files = os.listdir(folder)
    png_files = []
    sources = []

    for file in files:
    	# png jpg jpeg are supported
        if 'png' in file or 'jpeg' in file or 'jpg' in file:
            png_files.append(folder + file)

    # sort the images by creation time
    png_files.sort(key=lambda x: os.path.getmtime(x))   

    for file in png_files:
        print(folder+file)
        png_file = Image.open(file)
        if png_file.mode == "RGBA":
            png_file = png_file.convert("RGB")
        sources.append(png_file)

    # output pdf
    png_file.save(pdfFile, "pdf", 
    	save_all=True, append_images=sources)
    print('conversion is done: '+pdfFile)

# remove the first slide of a pdf
def remove_first_slice(pdfFile_name):
    # open pdf
    pdf_file = open(pdfFile_name, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # create a new pdf and write the remaining slides
    pdf_writer = PyPDF2.PdfWriter()
    for page_num in range(1, len(pdf_reader.pages)):
        # print(page_num)
        pdf_writer.add_page(pdf_reader.pages[page_num])

    # write pdf
    result_pdf = open(pdfFile_name, 'wb')
    pdf_writer.write(result_pdf)

    # close pdf
    pdf_file.close()

if __name__ == "__main__":

    # multi filefolder
    # path_in = path + "\in\\"
    path_in = " "
    path_out = " "
    file_names = os.listdir(path_in)
    
    for file_name in file_names:
        print(file_name)
        folder = path_in + file_name + "\\"
        pdfFile = path_out +  file_name + ".pdf"
        combine_imgs_pdf(folder, pdfFile)   # combine images to pdf file
        remove_first_slice(pdfFile)         # remove the first slice
        shutil.rmtree(folder)               # delete input filefolder


