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
import numpy as np

app_args = None

def get_options():
  
  global app_args

  from argparse import ArgumentParser

  parser = ArgumentParser(description='''This is a customized example script whose prior was provided by the PyMuPDF project.

This allows one to specify:

- DPI: (default=72)
- ROTATION: Only allows 90, 180 or 270.
''')
  
  parser.add_argument('--alpha', '-a', action='store_true',   help='use aplha channel (assumes `--fmt png`).')
  parser.add_argument('--dpi', action='store', default='72',  help='DPI resolution for rendering images. [DEFAULT: (72,72)].')
  parser.add_argument('--rot', action='store', default='0',   help='Rotation Angle(s); EG: (MUST BE) 90, 180, 270')
  parser.add_argument('--fmt', action='store', default='png', help='default=png; accepts: png | jpg')
  parser.add_argument('--quality', '-q', action='store', default='63', help='default=63; integers 1-100 (percent)')
  parser.add_argument('file', nargs='*')
  
  app_args = parser.parse_args()

  app_args.dpi = float(app_args.dpi)
  app_args.rot = float(app_args.rot)
  app_args.quality = int(app_args.quality)

#
def main(pInputFile):
  global app_args
  from PIL import Image

  t0 = time.clock()
  doc = fitz.open(pInputFile)           # the PDF
  imgcount = 0                          # counts extracted images
  lenXREF = doc._getXrefLength()        # only used for information
  
  # display some file info
  print("file: %s, pages: %s, objects: %s\n" % (pInputFile, len(doc), lenXREF-1))
  
  dpi   = app_args.dpi
  ratio = dpi / 72.0
  mtx   = fitz.Matrix(1, 1).preScale(ratio, ratio).preRotate(app_args.rot)
  
  if (app_args.fmt.lower() == 'png') or (app_args.alpha == True):
    fmt = 'png'
  else:
    fmt = 'jpg'

  print("uses alpha channel" if app_args.alpha else "uses NO alpha channel")
  
  for i in range(len(doc)):

    page = doc.loadPage(i)
    pix = page.getPixmap(alpha=app_args.alpha, matrix=mtx)
    
    if pix.n - pix.alpha < 4:      # can be saved as PNG
      pass
    else:                          # must convert CMYK first
      pix0 = fitz.Pixmap(fitz.csRGB, pix) # uses a default DPI of 72
      pix = pix0

    fname = "page-%i.%s" % (i+1, fmt)

    if app_args.alpha:
      im = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
    else:
      im = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    if fmt == 'png':
      im.save(fname, "png", dpi=(dpi, dpi))
    else:
      im.save(fname, "jpeg", dpi=(dpi, dpi), optimize=True, quality=app_args.quality)

    print('- got image: {}'.format(i+1))
    pix = None                     # free Pixmap resources

  t1 = time.clock()
  print("run time", round(t1-t0, 2))
  print("extracted images", len(doc))

get_options()

if app_args.file != None:
  for arg in app_args.file:
    main(arg)

