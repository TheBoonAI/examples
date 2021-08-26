'''
This Streamlit script displays the results of one search
'''

import json
import numpy as np
from PIL import Image
import cv2
import streamlit as st
from boonsdk import app_from_env

import boonsdk

app = boonsdk.app_from_keyfile("apikey.json")

query = st.text_area("Copy Query from Visualizer", '{"size": 20}')
query = json.loads(query)

search = app.assets.search(query)
count = len(search.assets)

images = []
labels = []
for asset in search:
    thumbnail = asset.get_files()[-1]
    img = np.array(Image.open(app.assets.download_file(thumbnail)))
    img = cv2.resize(img, None, fx=.5, fy=.5)
    images.append(img)
    labels.append(asset.id)

st.image(images, caption=labels)

