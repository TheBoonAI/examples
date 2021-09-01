'''
This Streamlit script displays the results of one search
'''

import json
import numpy as np
from PIL import Image
import streamlit as st
from boonsdk import app_from_env

import boonsdk


def make_thumb(img):
    s = max(img.shape[0:2])
    f = np.zeros((s, s, 3), np.uint8)
    ax, ay = (s - img.shape[1])//2, (s - img.shape[0])//2
    f[ay:img.shape[0] + ay, ax:ax + img.shape[1]] = img
    return f


app = boonsdk.app_from_keyfile("apikey.json")

text_query = st.text_input("Search", ' ')
query = {"query":{"bool":{"must":[{"simple_query_string":{"query":text_query}}]}}}

search = app.assets.search(query)
count = len(search.assets)

images = []
labels = []

for asset in search:
    thumbnail = asset.get_files()[0]
    img = np.array(Image.open(app.assets.download_file(thumbnail)))
    img = make_thumb(img)
    images.append(img)
    labels.append(asset.get_attr('source.filename'))

st.image(images, caption=labels, width=200)

