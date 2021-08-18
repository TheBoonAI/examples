
from boonsdk.util import denormalize_bbox
from boonsdk.func import FunctionResponse

def process(asset):

    # First grab the height and width of the asset itself, we'll need these
    # calculate the area later on.
    width = asset.get_attr("media.width")
    height = asset.get_attr("media.height")
    
    if not width or not height:
        return None

    # There could be multiple faces, so we'll stash the area of our biggest
    # face into the big_face variable.
    big_face = 0
    
    # Not iterate detected faces, calculate the area and keep track of the largest one.
    attr = "analysis.boonai-face-detection.predictions"
    faces = asset.get_attr(attr)
    if faces:
        for face in faces:
            bbox = denormalize_bbox(width, height, face['bbox'])
            area = abs(bbox[0]-bbox[2]) * abs(bbox[1]-bbox[3])
            if area > big_face:
                big_face = area
   
        if big_face:
            # Take our big face and set the value of the face_bbox_area custom fieid.
            rsp = FunctionResponse()
            rsp.set_custom_field("face_bbox_area", big_face)
            return rsp
    
    # It's ok to return None to indicate no modifications to asset.
    return None