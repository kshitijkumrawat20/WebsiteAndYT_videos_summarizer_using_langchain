import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import validators

st.set_page_config(
    page_title="Website and YT summarizer",
    page_icon="🦜"
)
st.title("Website and YT videos Summarizer using Langchain 🦜🔗")

with st.sidebar:
    groq_api_key = st.text_input("Groq API key", value ="",type="password")
    
url = st.text_input("URL",label_visibility="collapsed")

llm = ChatGroq(model="gemma2-9b-it", groq_api_key= groq_api_key)

template = """
Provide the summary of the following content in 200 words:
content: {text}
"""

prompt = PromptTemplate(
    input_variables=['text'],
    template=template,
)
if st.button("Summarize"):
    if not groq_api_key.strip() or not url.strip():
        st.error("Please provide the key and url")
    elif not validators.url(url):
        st.error("Please provide the URL.")
    else: 
        try:
            with st.spinner("Wait..."):
            
            # load the webiste or yt url
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(url=[url], ssl_verify= True, headers= {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
            docs= loader.load()
            
            # chain for summarization 
            chain = load_summarize_chain(llm, chain_type="stuff", prompt= prompt)
            output_summary = chain.run(docs)
            st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception;{e}")