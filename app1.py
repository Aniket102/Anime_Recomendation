# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
import pickle
import streamlit as st
user=0
loaded_model = pickle.load(open("recomendation_engine.pkl", 'rb'))
def main():
    st.title("Anime Recomendation")
    user = st.text_input("Enter the user id", 0)
    if st.button("Predict"):
     result=loaded_model(user)   
    st.sucess("The output is{}".format(result)) 

if __name__=="__main__":
 main()