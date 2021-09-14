# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pickle
import streamlit as st
import pandas as pd
import numpy as np
sim = pickle.load(open(r"user_sim_df", 'rb'))
user_sim_df=pd.DataFrame(sim)
alist=pickle.load(open(r"anime", 'rb'))
anime=pd.DataFrame(alist)
pv= pickle.load(open(r"pivot", 'rb'))
pivot=pd.DataFrame(pv)
def get_similar_user(user_id):
    if user_id not in pivot.index:
        return None, None
    else:
        sim_users = user_sim_df.sort_values(by=user_id, ascending=False).index[1:]
        sim_score = user_sim_df.sort_values(by=user_id, ascending=False).loc[:, user_id].tolist()[1:]
        return sim_users, sim_score
def get_recommendation(user_id, n_anime=10):
    users, scores = get_similar_user(user_id)
    
    # there is no information for this user
    if users is None or scores is None:
        return None
    # only take 10 nearest users
    user_arr = np.array([x for x in users[:10]])
    sim_arr = np.array([x for x in scores[:10]])
    predicted_rating = np.array([])   
    for anime_name in pivot.columns:
        filtering = pivot[anime_name].loc[user_arr] != 0.0  
        temp = np.dot(pivot[anime_name].loc[user_arr[filtering]], sim_arr[filtering]) / np.sum(sim_arr[filtering])
        predicted_rating = np.append(predicted_rating, temp) 
    # don't recommend something that user has already rated
    temp = pd.DataFrame({'predicted':predicted_rating, 'name':pivot.columns})
    filtering = (pivot.loc[user_id] == 0.0)
    temp = temp.loc[filtering.values].sort_values(by='predicted', ascending=False)
    # recommend n_anime anime
    return temp
def main():
 st.title("Anime Recomendation")
 user = st.text_input("Enter the user id", 0)
 if st.button("Predict"):
   result_df=get_recommendation(user)
   result_list=result_df["name"].tolist()
   for i in result_list: 
    st.sucess("The output is{}".format(i)) 
if __name__=="__main__":
 main()