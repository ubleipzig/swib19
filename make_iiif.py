#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import base64
import json
import cv2
import glob
import hashlib
import copy
import subprocess
import sys

def buildManifest(manifest,folder,config):
    uri = config['baseurl']+"/manifests/"+id+".json"
    manifest['@id'] = uri
    manifest['label'] = folder.split('/')[1].replace('_',' ')
    manifest['attribution'] = config['attribution']
    manifest['description'] = config['description']
    manifest['sequences'][0]['@id'] = uri+"/sequence/1"
    manifest['metadata'].append( { 'label' : 'Author' , 'value' : config['creator'] } )
    return manifest

def addCanvasToManifest(manifest,canvas,config,image,ic):
    uri = manifest['@id']
    # set IDs
    canvas['@id'] = uri+"/canvas/%d" % ic
    canvas['images'][0]['@id'] = uri+"/image/%d" % ic
    canvas['images'][0]['resource']['@id'] = uri+"/resource/%d" % ic
    # linke IDs
    canvas['images'][0]['on'] = canvas['@id']
    # set image dimensions
    output = subprocess.check_output(["./get_image_dim.sh", image[:-5]])
    width, height = [int(v) for v in output.strip().split('x')]
    canvas['width'] = width
    canvas['images'][0]['resource']['width'] = width
    canvas['height'] = height
    canvas['images'][0]['resource']['height'] = height
    # set license
    canvas['images'][0]['license'] = config['license']
    # set labels
    label = image.split('/')[1].replace('_',' ')
    canvas['label'] = label
    canvas['images'][0]['resource']['label'] = label
    # set service
    try:
        canvas['images'][0]['resource']['service']['@id'] = config['baseurl']+"/"+image
    except UnicodeDecodeError:
        canvas['images'][0]['resource']['service']['@id'] = config['baseurl']+"/"+image.decode('utf-8')
    # append canvas to manifest
    manifest['sequences'][0]['canvases'].append(canvas)
    return manifest

with open('config.json', 'r') as f:
    config = json.load(f)

with open('manifest_template.json', 'r') as f:
    manifest_template = json.load(f)

with open('canvas_template.json', 'r') as f:
    canvas_template = json.load(f)

folders = [f for f in glob.glob("imageapi/*")]
for folder in folders:
    manifest = copy.deepcopy(manifest_template)
    id = hashlib.md5(folder.encode()).hexdigest()
    manifest = buildManifest(manifest, folder, config)
    images = [image for image in glob.glob(folder+"/*.ptif")]
    ic = 1
    for image in images:
        canvas = copy.deepcopy(canvas_template)
        manifest = addCanvasToManifest(manifest,canvas,config,image,ic)
        ic = ic +1
    filename = "presentationapi/manifests/"+id+".json"
    print("writing: "+filename)
    with open(filename, 'w') as outfile:
        json.dump(manifest, outfile, sort_keys=True, indent=4, separators=(',', ': '))
