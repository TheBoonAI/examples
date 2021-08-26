'''
This Streamlit script displays one random image from the server you log into
'''

import random
import streamlit as st
from boonsdk import app_from_env

import boonsdk

app = boonsdk.app_from_keyfile("apikey.json")

query = {"size": 10000}
search = app.assets.search(query)
count = len(search.assets)
st.text(count)
asset = search.assets[random.randint(0, count)]

thumbnail = asset.get_files(category="web-proxy")[0]

st.image(app.assets.download_file(thumbnail))
st.sidebar.text("Hello World")

