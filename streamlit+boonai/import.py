import boonsdk
import glob

app = boonsdk.app_from_keyfile("apikey.json")

files = []
paths = glob.glob('unsplash-small/*.jpg')

for p in paths:
    files.append(boonsdk.FileUpload(p))

# We import 100 files at a time
while files:
    app.assets.batch_upload_files(files[:100], modules=['gcp-label-detection', 'azure-object-detection'])
    files = files[100:]

