# extract_pred_metadata.py
from utils.location import find_bbox_centroid, find_quadrant
import streamlit as st

def extract_prediction_data(raw_results, image_input):
    data = []
    for r in raw_results:
        centroid = find_bbox_centroid(r['xyxy'][0], r['xyxy'][1], r['xyxy'][2], r['xyxy'][3])
        location = find_quadrant(image_input, centroid[0], centroid[1])
        data.append({
            'class_id': r['class'],
            'class_name': r['class_name'],
            'confidence_score': r['conf'],
            'location': location
        })
    return data

