#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pdftoimage.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/8/20 12:28   gxrao      1.0         None
'''

from wand.image import Image

filename = "d:/aa.pdf"

with(Image(filename=filename, resolution=120)) as source:
    images = source.sequence
    pages = len(images)
    for i in range(pages):
        n = i + 1
        newfilename = filename[:-4] + str(n) + '.jpeg'
        Image(images[i]).save(filename=newfilename)