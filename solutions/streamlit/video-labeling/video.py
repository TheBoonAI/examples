
import streamlit as st

import boonsdk

import os
import cv2
import base64
import glob


@st.cache
def get_frames(video_name, n):
    cap = cv2.VideoCapture(video_name)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = int(frame_count / n)

    frames = []
    vals = []
    pos = 0
    for frame in range(0, n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        frames.append(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        vals.append(pos)
        pos += step

    return frames, vals


app = boonsdk.app_from_keyfile("apikey.json")

videos = glob.glob('videos/*.mp4')
video_name = st.sidebar.selectbox('Video', videos)
cap = cv2.VideoCapture(video_name)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

dataset_name = st.sidebar.text_input('Dataset', value='knn')

dataset = app.datasets.find_one_dataset(name=dataset_name)

n_frames = st.sidebar.slider('n Frames', min_value=2, max_value=100, value=4)

label_value = st.sidebar.text_input('Label')

scope = boonsdk.entity.dataset.LabelScope.TRAIN
if st.sidebar.radio('Label Scope', ['Train', 'Test']) == 'Test':
    scope = boonsdk.entity.dataset.LabelScope.TEST

frames, vals = get_frames(video_name, n_frames)

ncols = 6
pos = 0
buttonid = 0
while(frames):
    cols = st.columns(ncols)
    for i, col in enumerate(cols):
        if frames:
            col.image(frames[0])
            if col.button('Go to this frame', key=str(buttonid)):
                pos = vals[0]
            buttonid += 1
            frames = frames[1:]
            vals = vals[1:]

pos = st.slider('frame', min_value=0, max_value=frame_count, value=pos)

cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
ret, frame = cap.read()
st.image(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), use_column_width='always')

if st.sidebar.button('Label this frame'):
    im_name = video_name + '.' + str(pos) + '.jpg'
    cv2.imwrite(im_name, frame)
    label = dataset.make_label(label_value, scope=scope)
    app.assets.batch_upload_files([boonsdk.FileUpload(im_name, label=label)])

