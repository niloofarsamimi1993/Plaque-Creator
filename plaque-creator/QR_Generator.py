
''' This Code generates  QRcodes using fixed strings then creates plagues using generated QRcodes and Labels'''
#created January 07,2020
#Author: Niloofar
#this library has methods can be used for creating QRcodes and save them as SVG files
import pyqrcode
#this library has methods can be used for editing SVG files
import svgutils
import svgutils.transform as sg
#this libary has methods can be used for deleting useless files
import os
#this library has methods for working with different fonts
import reportlab
#the following ten lines allow PDFwriter using new fonts
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
import fitz
#adding B_Traffic font to resigtered fonts
pdfmetrics.registerFont(TTFont("B_Traffic", "B_Traffic.ttf"))




#calculating number of zeros
def zero_counter(i):
    zero_count=""
    if i>=0 and i<10:
        #for 0-9: plaques and links numbering format: 00001 ,00002,....
        zero_count="0000"
    elif i>=10 and i<100:
        #for 00-99: plaques and links numbering format: 00010 ,00011,....
        zero_count="000"
    elif i>=100 and i<1000:
        #for 100-999: plaques and links numbering format: 00100 ,00101,....
        zero_count="00"
    elif i>=1000 and i<9999:
        #for 1000-9999: plaques and links numbering format: 01000 ,01001,....
        zero_count="0"
    elif i>=10000 and i<20000:
        #for 10000-99999: plaques and links numbering format: 10000 ,10001,...
        zero_count=""
    return zero_count

#turning a English number to a farsi string
def num_convertr(input_number):
#turning a number to a string and then to a list
    number = list(str(input_number))
    for i in range(0,len(number)):
        if number[i]=="0":
             number[i]="۰"
        elif number[i]=="1":
             number[i]="۱"
        elif number[i]=="2":
             number[i]="۲"
        elif number[i]=="3":
             number[i]="۳"
        elif number[i]=="4":
             number[i]="۴"
        elif number[i]=="5":
             number[i]="۵"
        elif number[i]=="6":
             number[i]="۶"
        elif number[i]=="7":
             number[i]="۷"
        elif number[i]=="8":
             number[i]="۸"
        elif number[i]=="9":
             number[i]="۹"
    #initiating a variable for keeping the output string
    final_string = ""
    #the following three lines convert a list of chars to a string
    for i in number:
        final_string += i
    return final_string

#this function makes a string (in this case a URL) to generate a QRcode using a fixed string and a unique number
#i is unique number at the end of string
#link_string is a fixed string (in this case a URL)
def link_maker(i,link_string,zero_count):
        qrcode_link=link_string+zero_count+str(i)
        return  qrcode_link
#creating a QRcode using a created link (in this cade string created with link_maker)
def QRcode_maker(i,qrcode_link):
        #creating a QRcode
        url = pyqrcode.create(qrcode_link,version=5)
        #saving QRcode as a SVG file
        url.svg(str(i)+'.svg', scale=1.05 ,module_color="#fff" )

#making plaque label (setting position,size,cBolor and font)
def txt_maker(i,zero_count):
        txt1 = sg.TextElement(31,158,num_convertr(zero_count)+ num_convertr(i), size=60,color="#fff",font="B_Traffic")
        return txt1

#creating plagues using a string(first part of link),number of plaques and base plague file(SVG) name
def plaque_creator(number,link_for_QRcodes,plaque_file_name):
    for i in range (1013,number++1):
            zc=zero_counter(i)
            #making a link for current plaque number
            current_link=link_maker(i,link_for_QRcodes,zc)
            #making a QRcode from link created by link_maker
            QRcode_maker(i,current_link)
            #craeting a window  using given size
            fig = sg.SVGFigure("12cm", "7cm")
            #load QRcode svg files
            fig1 = sg.fromfile(str(i)+'.svg')
            #load raw plaque SVG file
            fig2 = sg.fromfile(plaque_file_name)
            # get the plot objects
            #plot1 is QRcode SVG file and plot2 is plaque SVG file
            plot1 = fig1.getroot()
            plot2 = fig2.getroot()
            #fixing plot object scale and position
            plot1.moveto(222,103, scale=1.7)
            plot2.moveto(0,0, scale=1)
            #making text labels
            current_txt=txt_maker(i,zc)
            #add plots and labels to figure
            fig.append(plot2)
            fig.append(plot1)
            fig.append(current_txt)
            # save generated SVG files(final plaque files)
            fig.save("Final_QR_Code_"+str(i)+".svg")
            #opening plaque SVG files
            drawing = svg2rlg("Final_QR_Code_"+str(i)+".svg")
            #converting Plaque SVG files to PDF files
            renderPDF.drawToFile(drawing,str(i)+".pdf")
            #convert pdf to JPG
            """pdffile = str(i)+".pdf"
            doc = fitz.open(pdffile)
            page = doc.loadPage(0) #number of page
            pix = page.getPixmap()
            output =str(i)+".jpg"
            pix.writePNG(output)"""
            #removing QRcode SVG files
            os.remove(str(i)+'.svg')
            #remove Plaque SVG file
            os.remove("Final_QR_Code_"+str(i)+".svg")


#plaque_creator(number,link_for_QRcodes,plaque_file_name)
plaque_creator(10000,"http://innovationgarden.ir/trees/","plaque.svg")
