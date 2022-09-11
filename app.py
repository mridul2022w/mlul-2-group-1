import streamlit as st
from streamlit_card import card
from utils import *
from PIL import Image


st.set_page_config(layout="wide", initial_sidebar_state="expanded")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


if 'submit' not in st.session_state:
    st.session_state.submit = 0

df = pd.read_csv('featuressub.csv')
df['imageurl'] = np.where(df['sex'] == 'm','https://cdn-icons-png.flaticon.com/512/4128/4128176.png','https://cdn1.iconfinder.com/data/icons/user-pictures/100/female1-512.png')


def my_callback():
    global df
    st.session_state.submit = 1
    st.session_state.formdata = {'id':df['id'].max() + 1,
                                'age':widage,
                                'status':st.session_state.optionstatus,
                                'orientation':st.session_state.optionorientation,
                                'location':st.session_state.optionlocation,
                                'sex':st.session_state.optionsex,
                                'smokes':st.session_state.optionsmokes,
                                'body_type':st.session_state.optionbody_type,
                                'drugs':st.session_state.optiondrugs,
                                'drinks':st.session_state.optiondrinks}
    st.session_state.userid = df['id'].max() + 1

def like_button(id):
    with st.spinner('Refining your matches...'): 
        out = get_recommended_user(df1,id)
        if len(out) != 0:
            print(out)
            df2 = df1[df1['id'].isin(out)]

    
with st.container():
    
    col1, col2 = st.columns([0.3,0.7],gap="large")
    
    with col1:
        st.header("TeAMO")
        st.write("")
        
        st.write("Dating is a stage of romantic relationships in humans whereby two people meet socially with the aim of each assessing the other's suitability as a prospective partner in an intimate relationship.It is a form of courtship, consisting of social activities done by the couple, either alone or with others.")
        st.write("")
        st.write("")
        
    with col2:
        image = Image.open('dating1.png')
        st.image(image)
    
    
    
        
with st.container():
        
    st.header("Basic Information*")
    
    with st.form(key="my-form1"):
        col1, col2,col3= st.columns([0.3,0.3,0.3],gap="large")
        with col1:
            lst = ['status','smokes']
            for j in lst:
                widget = 'option' + str(j)
                widget = st.selectbox(j.capitalize(),df[j].unique().tolist(),key=widget)
            widage = st.slider('How old are you?', 18, 100, 25)

        
        with col2:
            
            lst = ['orientation','location','drugs','pets']
            for j in lst:
                widget = 'option' + str(j)
                widget = st.selectbox(j.capitalize(),df[j].unique().tolist(),key=widget)
        
        with col3:
            lst = ['sex','body_type','drinks','diet']
            for j in lst:
                widget = 'option' + str(j)
                widget = st.selectbox(j.capitalize(),df[j].unique().tolist(),key=widget)
        submitted1 = st.form_submit_button("Submit",on_click=my_callback)

st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

if st.session_state['submit'] == 1:
    print("check again")
    with st.container():

        col1, col2,col3= st.columns([0.3,0.3,0.3],gap="large")
        
        with col1:
            st.header("Your Preference")
            start_age, end_age = st.select_slider('Select a range of age',options=range(18,101),value=(22,28))
            sex = st.radio("Sex",('Male', 'Female','Both'))
            options = st.multiselect('Orientation',['straight', 'bisexual', 'gay'])
        
        with col2:
            if sex=='Male':
                sex1 = 'm'
            elif sex=="Female":
                sex1 = 'f'
            else:
                sex1 = 'b'
            if sex1 != 'b':
                df1 = df[df['sex']==sex1]
            else:
                df1 = df.copy()
            if len(options) > 0:
                df1 = df1[df1['orientation'].isin(options)]
            df1 = df1[(df1['age']>=start_age) & (df1['age']<=end_age)]
            df1 = df1.append(st.session_state.formdata, ignore_index=True)
            
            with st.spinner('Finding the perfect match for you...'):
                out = get_recommended_user(df1,st.session_state.userid)
                df2 = df1[df1['id'].isin(out)]
                if df2.shape[0]:
                    for i in range(0,df2.shape[0],2):
                        card(title='User #'+str(df2['id'].iloc[i])+","+str(df2['age'].iloc[i]), text=df2['location'].iloc[i],key="firstcardview"+str(i),image=df2['imageurl'].iloc[i])
                        with st.expander("See Details"):
                             st.write("Smokes: ",df2['smokes'].iloc[i])
                             st.write("Drinks: ",df2['drinks'].iloc[i])
                             st.write("Body type: ",df2['body_type'].iloc[i])
                             st.write("Drugs: ",df2['drugs'].iloc[i])
                             st.write("Orientation: ",df2['orientation'].iloc[i])
                             st.write("Status: ",df2['status'].iloc[i])
                             st.write("Pets: ",df2['pets'].iloc[i])
                             st.write("Diet: ",df2['diet'].iloc[i])
                             st.button("Like",key="firstcardbutton"+str(i),on_click=like_button,args=[df2['id'].iloc[i]])
        with col3:
            if df2.shape[0]:
                for i in range(1,df2.shape[0],2):
                    card(title='User #'+str(df2['id'].iloc[i])+","+str(df2['age'].iloc[i]), text=df2['location'].iloc[i],key="secondcardview"+str(i),image=df2['imageurl'].iloc[i])
                    with st.expander("See Details"):
                         st.write("Smokes: ",df2['smokes'].iloc[i])
                         st.write("Drinks: ",df2['drinks'].iloc[i])
                         st.write("Body type: ",df2['body_type'].iloc[i])
                         st.write("Drugs: ",df2['drugs'].iloc[i])
                         st.write("Orientation: ",df2['orientation'].iloc[i])
                         st.write("Status: ",df2['status'].iloc[i])
                         st.write("Pets: ",df2['pets'].iloc[i])
                         st.write("Diet: ",df2['diet'].iloc[i])
                         st.button("Like",key="secondcardbutton"+str(i),on_click=like_button,args=[df2['id'].iloc[i]])
        