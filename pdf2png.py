#! python
'''

This was once one of the demo or example py-script(s) to extract images
from a PDF page --converted to an example converting each page to png.

- added command-line argument inputs for DPI and ROTATION.
- using PILlow to (re-)write images with DPI setting stored to the image.
- ONLY rotation expects 90, 180 and 270
  so that the image's BOX is either portrait or landscape.

'''
from __future__ import print_function
import fitz
import PIL
import sys
import time

app_args = None

def get_options():
  
  global app_args

  from argparse import ArgumentParser

  parser = ArgumentParser(description='''This is a customized example script whose prior was provided by the PyMuPDF project.

This allows one to specify:

- DPI: (default=72)
- ROTATION: Only allows 90, 180 or 270.
''')
  
  parser.add_argument('--dpi', action='store', dest='dpi', help='DPI resolution for rendering images. [DEFAULT: (72,72)].')
  parser.add_argument('--rot', action='store', dest='rot', help='Rotation Angle(s); EG: (MUST BE) 90, 180, 270')
  parser.add_argument('file', nargs='*')
  
  app_args = parser.parse_args()

#
def dpi_ratio(dpi_new, dpi_old=72):
  """
  This returns a multiplier that can be used in our Matrix
  so as to render an image at a specific DPI.
  """
  return dpi_new / dpi_old

#
def main(pInputFile):

  # assert len(sys.argv) == 2, 'Usage: %s <input file>' % sys.argv[0]

  t0 = time.clock()
  doc = fitz.open(pInputFile)           # the PDF
  imgcount = 0                          # counts extracted images
  lenXREF = doc._getXrefLength()        # only used for information
  
  # display some file info
  print("file: %s, pages: %s, objects: %s\n" % (pInputFile, len(doc), lenXREF-1))
  
  ratio = 1.0 if app_args.dpi == None else dpi_ratio(float(app_args.dpi))
  rotation = 0 if app_args.rot == None else float(app_args.rot)
  mtx = fitz.Matrix(1, 1).preScale(ratio, ratio).preRotate(rotation)

  for i in range(len(doc)):

    page = doc.loadPage(i)
    pix = page.getPixmap(alpha=False, matrix=mtx)
    if pix.n - pix.alpha < 4:      # can be saved as PNG
      pass
    else:                          # must convert CMYK first
      pix0 = fitz.Pixmap(fitz.csRGB, pix) # uses a default DPI of 72
      pix = pix0

    fname = "page-%i.png" % (i+1)


    pix.writePNG(fname)
    img_dpi(fname)

    imgcount += 1

    print('- got image: {}'.format(i+1))

    pix = None                     # free Pixmap resources

  t1 = time.clock()
  print("run time", round(t1-t0, 2))
  print("extracted images", imgcount)

get_options()

if app_args.file != None:
  for arg in app_args.file:
    main(arg)
