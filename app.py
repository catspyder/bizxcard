
import streamlit as st
import numpy as np
import easyocr as ocr
# from PIL import Image
# from io import StringI/O
import json
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
import pickle


class Card:
    card={}
    data=[]
    dynamic=[]
    www=''
    com=''
    def initial(self):
        for i in range(len(self.text)):
            self.data.append(self.text[i][1])
            self.dynamic.append(self.text[i][1])
   
    def int_checker(self,field):
        nums=0
        zeroes=0
        for i in range(len(field)):
            
            if field[i] in['0','1','2','3','4','5','6','7','8','9']:
                
                nums+=1
            if field[i] == '0':
                zeroes+=1
#         print(nums,zeroes)
        return nums,zeroes 

        
    def phone_finder(self):
        ph=None
        for field in self.dynamic:
            
            ret=self.int_checker(field)
            if ret[0]==10 and ret[1]!=10:
                if ph is not None and len(ph)>field:
                    ph=field
                elif ph is None:
                    ph=field
        if ph is not None:
            self.card['phno']=ph
        
    def email_finder(self):
        for field in self.dynamic:
            pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if re.match(pat,field):
                self.card['email']=field
                pass #(field)
                break           
    def weblink(self):
        w=0
        c=0
        www=None
        com=None
        for item in self.dynamic:
            if w==1 and c==1:
                break
            elif re.search("^www",item) or re.search("^WWW",item) and w==0:

                www=item
                w+=1
            elif re.search("com$",item) and c==0:
                com=item
                c+=1
            

        if www is not None:
            
            pass #(www)
            if com is not None:
                pass #(com)
                if len(www)==3 and com[0]!='.':
                    www=www+'.'
                    website= www + com
                    self.card['website'] = website


    def pin_finder(self):
        for item in self.dynamic:
            if len(item)==6:
                num,zero=self.int_checker(item)
                if num==6 and zero!=6:
                    self.card['pincode']=item
        if self.card['pincode'] is not None:
            pass #(self.card['pincode'])

   
     
    


    def clean(self):
        keys=self.card.keys()
        for key in keys:
            value=self.card[key]
            if value in self.dynamic:
                self.dynamic.remove(value)

    def partial_string_match(self,pattern):
        matches = []

        if isinstance(pattern, str):
            pattern = re.compile(pattern, re.IGNORECASE)

        for string in self.dynamic:
            if pattern.findall(string):
                matches.append(string)
        
        return matches



    def company_name(self):
        company=None
        email=self.card['email']
        pattern = r'@([^.]*)\.'
        company= re.search(pattern,email)
        if company is not None:
            match = self.partial_string_match(company)
            company_name=match[-1]
            self.card['company_name'] = company_name
        
    def title_finder(self):    

        model = load_model('model.h5')

        with open('tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        # pre processinng the input
        max_length=17
        test_words = self.dynamic
        test_sequences = tokenizer.texts_to_sequences(test_words)
        test_padded_sequences = pad_sequences(test_sequences, maxlen=max_length)
        predictions = model.predict(test_padded_sequences)
        mx=0
        j=-1
        # program to find the max position
        for i in range(len(t)):
        if predictions[i]>mx:
            j=i
            mx=predictions[i]

        self.card['title']=self.dynamic[j]


    
    def __init__(self,img):
        reader=ocr.Reader(['en'])
        self.text=reader.readtext  (img,ycenter_ths=1)
        self.initial()
        self.phone_finder()
        self.email_finder()
        self.weblink()
        self.pin_finder()
        self.clean()
        self.company_name()
        self.title_finder()



img_file_buffer=st.file_uploader('upload business card')

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    card= Card(bytes_data)
    st.write(card.dynamic)
    st.write(card.card)
