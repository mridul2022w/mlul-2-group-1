import pandas as pd
import numpy as np
import time
import requests
from sklearn.metrics.pairwise import cosine_similarity
from heapq import nlargest


def get_recommended_user(subsetdata,user):
    dummydat2= subsetdata[["id", "age", "status", "sex", "drinks", "smokes", "drugs", "body_type", "orientation"]]  #CHOOSING ONLY THESE COLUMNS FOR ENCODING
    nominal_features = pd.get_dummies(data = dummydat2,columns= ["status", "sex", "drinks", "smokes", "drugs", "body_type", "orientation"], drop_first=True)   # ENCODE
    # lengthdf = len(nominal_features)-1
    # print(lengthdf)
    # new_user = nominal_features._get_value(lengthdf, 0, takeable = True)
    # print(new_user)
    out = findmatches(user,nominal_features)
    
    return out

def findmatches(curr,nominal_features):  # FUNCTION TO RETURN LIST OF RECO IDS CORRESPONDING TO CURR ID
    Dict = {}
     
#   curr = int(liked_list[1])
    curterm = nominal_features[nominal_features["id"]==curr]  #PICKOUT THE WHOLE ROW CORESP TO CURR ID
    curterm.drop(labels="id", axis=1)   #remove id COLUMN before cosine similarty
    nominal_features1 = nominal_features
    for t in nominal_features1.id:   #ITERATE FOR ALL PROFILES(IDS)
        if t!=curr: 
            iterm = nominal_features1[nominal_features1["id"]==int(t)]  #ROW OF EACH ID
            iterm.drop(labels="id", axis=1)
            Dict[int(t)] = cosine_similarity(curterm,iterm )    #STORE THE KEY-ID AND VALUE-SIMILARITY PAIR IN DICT DICTIONARY
        
        
    best_matches = nlargest(6, Dict, key = Dict.get)       #PICK OUT TOP 3 MATCHES OF CURR AND STORE IN BEST_MATCHES
    return best_matches