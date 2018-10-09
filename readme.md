
modified one of the image-export examples found in PyMuPDF
so one could specify DPI...

FEATURES

- Command-line friendly (argparse)
- PDF to PNG or JPG
- Rotate 90°, 180° or 270°
- Specicify desired DPI
- Example Windows command (*.cmd) drag-drop use-cases.

EXAMPLE command-line help

```
>$ python3 pdf2png.py --help
```
outputs the following

```text
usage: pdf2png.py [-h] [--alpha] [--dpi DPI] [--rot ROT] [--fmt FMT]
                  [--quality QUALITY]
                  [file [file ...]]

This is a customized example script whose prior was provided by the PyMuPDF
project. This allows one to specify: - DPI: (default=72) - ROTATION: Only
allows 90, 180 or 270.

positional arguments:
  file

optional arguments:
  -h, --help            show this help message and exit
  --alpha, -a           use aplha channel (assumes `--fmt png`).
  --dpi DPI, -d DPI     DPI resolution for rendering images. [DEFAULT:
                        (72,72)].
  --rot ROT, -r ROT     Rotation Angle(s); EG: (MUST BE) 90, 180, 270
  --fmt FMT, -f FMT     default=png; accepts: png | jpg
  --quality QUALITY, -q QUALITY
                        default=63; integers 1-100 (percent)
```

with example (drag-drop) Windows command-script use-cases.


EXTERNAL DEPENDENCIES

https://github.com/rk700/PyMuPDF  
license: GPLv3

https://python-pillow.org/  
license: MIT


license: inherits PyMuPDF's GPLv3
