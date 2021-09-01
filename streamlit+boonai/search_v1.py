'''
This Streamlit script displays the results of one search
'''

import streamlit as st
import boonsdk
import numpy as np
from PIL import Image


app = boonsdk.app_from_keyfile("apikey.json")

query = {"query":{"bool":{"must":[{"simple_query_string":{"query":"dog"}}]}}}

search = app.assets.search(query)
count = len(search.assets)

images = []

for asset in search:
    thumbnail = asset.get_files()[0]
    img = np.array(Image.open(app.assets.download_file(thumbnail)))
    images.append(img)

st.image(images, width=200)

