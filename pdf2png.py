#! python
'''
This demo extracts all images of a PDF as PNG files that are referenced
by pages.
Runtime is determined by number of pages and volume of stored images.
Usage:
------
extract_img1.py input.pdf
Changes:
--------
(1)
Do not use pix.colorspace when checking for CMYK images, because it may be None
if the image is a stencil mask. Instead, we now check pix.n - pix.alpha < 4
to confirm that an image is not CMYK.
IAW: the repr() of a stencil mask pixmap looks like
"Pixmap(None, fitz.IRect(0, 0, width, height), 1)", and we have
width * height == len(pix.samples).
(2)
Pages may reference the same image multiple times. To avoid to also extracting
duplicate images, we maintain a list of xref numbers.

-----------------------------------------------------------------------------------

tfwio simply added the ArgumentParser and some PILlow usage so as to allow an arbitrary
DPI setting on exported PNG files in addition to a rotation setting.

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

- DPI: (default=96)
- ROTATION: Only allows 90, 180 or 270.
''')
  
  parser.add_argument('--dpi', action='store', dest='dpi', help='DPI resolution for rendering images. [DEFAULT: (72,72)].')
  parser.add_argument('--rot', action='store', dest='rot', help='Rotation Angle(s); EG: (MUST BE) 90, 180, 270')
  parser.add_argument('file', nargs='*')
  
  app_args = parser.parse_args()


def img_transform(fname):
  from PIL import Image
  im = Image.open(fname)
  
  if (app_args.rot != None) and (app_args.rot != 0):
    rot = int(app_args.rot)
    if rot == 270: im = im.transpose(PIL.Image.ROTATE_270)
    if rot == 180: im = im.transpose(PIL.Image.ROTATE_180)
    if rot == 90:  im = im.transpose(PIL.Image.ROTATE_90)

  if (app_args.dpi != None) and (app_args.dpi != 0):
    im_dpi = int(app_args.dpi)
    im.save(fname, dpi=(im_dpi, im_dpi))

  else:
    im.save(fname)


def img_dpi(fname):
  from PIL import Image
  im = Image.open(fname)
  
  dpi = 72 if app_args.dpi == None else int(app_args.dpi)
  im.save(fname, dpi=(dpi,dpi))

def recoverpix(doc, item):

  x = item[0]  # xref of PDF image
  s = item[1]  # xref of its /SMask

  pix1 = fitz.Pixmap(doc, x)
  if s == 0:                    # has no /SMask
    return pix1               # no special handling
  pix2 = fitz.Pixmap(doc, s)    # create pixmap of /SMask entry
  # check that we are safe
  if not (pix1.irect == pix2.irect and \
      pix1.alpha == pix2.alpha == 0 and \
      pix2.n == 1):
    print("pix1", pix1, "pix2", pix2)
    raise ValueError("unexpected situation")
  pix = fitz.Pixmap(pix1)       # copy of pix1, alpha channel added
  pix.setAlpha(pix2.samples)    # treat pix2.samples as alpha value
  pix1 = pix2 = None            # free temp pixmaps
  return pix

def main_function_old(pInputFile):

  # assert len(sys.argv) == 2, 'Usage: %s <input file>' % sys.argv[0]

  t0 = time.clock()
  doc = fitz.open(pInputFile)           # the PDF
  imgcount = 0                           # counts extracted images
  xreflist = []                          # records images already extracted
  lenXREF = doc._getXrefLength()         # only used for information

  # display some file info
  print("file: %s, pages: %s, objects: %s" % (pInputFile, len(doc), lenXREF-1))

  for i in range(len(doc)):
    imglist = doc.getPageImageList(i)
    for img in imglist:
      if img[0] in xreflist:         # this image has been processed
        continue
      xreflist.append(img[0])        # take note of the xref
      pix = recoverpix(doc, img[:2])  # make pixmap from image
      if pix.n - pix.alpha < 4:      # can be saved as PNG
        pass
      else:                          # must convert CMYK first
        pix0 = fitz.Pixmap(fitz.csRGB, pix)
        pix = pix0

      fname = "p%i-%s.png" % (i, img[7])

      pix.writePNG(fname)
      img_transform(fname)

      imgcount += 1

      print('- got image: {}'.format(i))

      pix = None                     # free Pixmap resources

  t1 = time.clock()
  print("run time", round(t1-t0, 2))
  print("extracted images", imgcount)


def dpi_ratio(dpi_new, dpi_old=72):
  """
  This returns a multiplier that can be used in our Matrix
  so as to render an image at a specific DPI.
  """
  return dpi_new / dpi_old

def main_function(pInputFile):

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
    main_function(arg)

