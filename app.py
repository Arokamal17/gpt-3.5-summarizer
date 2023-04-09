import streamlit as st
import openai
import os
import requests
import json
# from dotenv import load_dotenv

# load_dotenv()
# openai.api_type = "azure"
# openai.api_base = "https://chat-gpt-a1.openai.azure.com/"
# openai.api_version = "2022-12-01"
api_key = "c09f91126e51468d88f57cb83a63ee36"



def generate_summarizer(max_tokens,temperature,top_p,frequency_penalty,prompt,):
    
    url = "https://chat-gpt-a1.openai.azure.com/openai/deployments/DanielChatGPT/chat/completions?api-version=2023-03-15-preview"
        
    headers = {'Content-Type': 'application/json', 
               'api-key':api_key,
               'max_tokens':str(max_tokens),
               'temperature':str(temperature),
               'top_p':str(top_p),
               'frequency_penalty':str(frequency_penalty)
               }
    data = {'messages': [{"role": "system", "content": "You are a helpful assistant for text summarization."}, 
                         {"role": "user", "content": f"Summarize this: {prompt}"} ]}
    body = str.encode(json.dumps(data))
    # res = openai.ChatCompletion.create(
    #     engine="DanielChatGPT",
    #     max_tokens=max_tokens,
    #     temperature=temperature,
    #     top_p=top_p,
    #     frequency_penalty=frequency_penalty,
    #     messages=[
    #         {"role": "system","content": "You are a helpful assistant for text summarization."},
    #         {"role": "user","content": f"Summarize this: {prompt}"},
    #     ]
    # )
    # return res["choices"][0]["message"]["content"]
    r = requests.post(url=url,data=body, headers=headers)
    response = r.content
    response = json.loads(response.decode())
    response = response["choices"][0]["message"]["content"]
    return response


#Set the application title
st.title("GPT-3.5 Text Summarizer")

#Provide the input area for text to be summarized
input_text = st.text_area("Enter the text you want to summarize:", height=200)

#Initiate three columns for section to be side-by-side
col1, col2, col3 = st.columns(3)

#Slider to control the model hyperparameter
with col1:
    token = st.slider("Token", min_value=0.0,
                      max_value=4096.0, value=50.0, step=1.0)
    temp = st.slider("Temperature", min_value=0.0,
                     max_value=1.0, value=0.0, step=0.01)
    top_p = st.slider("top_p", min_value=0.0,
                      max_value=1.0, value=0.5, step=0.01)
    f_pen = st.slider("Frequency Penalty", min_value=-1.0,
                      max_value=1.0, value=0.0, step=0.01)


#Showing the current parameter used for the model
with col3:
    with st.expander("Current Parameter"):
        st.write("Current Token :", token)
        st.write("Current Temperature :", temp)
        st.write("Current Top_p :", top_p)
        st.write("Current Frequency Penalty :", f_pen)

#Creating button for execute the text summarization
if st.button("Summarize"):
    st.write(generate_summarizer(token, temp, top_p, f_pen, input_text))
