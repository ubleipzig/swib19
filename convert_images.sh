#!/bin/bash

find imageapi -type f | while read i
do
  if [ ${i: -5} != ".ptif" ]; then
    echo "converting $i to $i.ptif"
    # convert "$i" -define tiff:tile-geometry=256x256 -compress jpeg -quality 96 "ptif:$i.ptif"
    vips im_vips2tiff $i $i.ptif:deflate,tile:256x256,pyramid
   else
    echo "skipping $i"
  fi
done

