import streamlit as st
from pytube import YouTube
import openai
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi 

openai.api_key="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"

def get_transcript(video_url):
    video_id = extract.video_id(video_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = " ".join([item["text"] for item in transcript])
    max_context_length = 4097
    transcript = transcript[:max_context_length]
    return transcript



def get_thumbnail_url(video_url):
    yt = YouTube(video_url)
    thumbnail_url = yt.thumbnail_url
    return thumbnail_url

st.title(":red[Youtube] Video Analyzer")
st.markdown("""
    <style>
        .element-space {
            margin-bottom: 20px; /* Adjust the margin as needed */
        }
    </style>
""", unsafe_allow_html=True)
st.subheader("About Youtube video analzyer")

multiline_markdown="""
Youtube video is tool used to generate summery,questions,comment sentiments and trailer extraction
from a youtube video.It helps in better understanding of topics you want to learn 

"""
st.markdown(multiline_markdown)
url = st.text_input("Paste an Youtube URL here:")
thumbnail_url = get_thumbnail_url(url)
st.image(thumbnail_url, caption="Example Image", use_column_width=True)
transcript=get_transcript(url)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You summerize paragraph to help get important points from the paragrapgh which are easy to remember "},
        {"role": "user", "content": transcript}
    ]
)

x=response['choices'][0]['message']['content']


h="I love You"
st.header('Summary')
mult=f"""
    {x}
""" 
st.markdown(mult) 

