import streamlit as st
import numpy as np
import easyocr as ocr


class Card:
    
    def __init__(self,img):
        self.text=ocr.Reader(img)

    


img=np.asarray(st.file_uploader('upload business card',type=['png', 'jpg'] ))
card= Card(img)
st.write(card.text)