from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import streamlit as st


urls = [
    'https://www.youtube.com/watch?v=WRFbpissttY'
]

for url in urls:
    video_id = extract.video_id(url)
    print(video_id)



video_id = "WRFbpissttY"
transcript = YouTubeTranscriptApi.get_transcript(video_id)
print(transcript)
transcript = " ".join([item["text"] for item in transcript])

print(transcript)

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
#from openai import openAI

#########################################
OPENAI_API_KEY = ""
#########################################

max_context_length = 4097
transcript = transcript[:max_context_length]

template = f"""
You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, you're tasked with designing 5 distinct questions. Each of these questions will be accompanied by 3 possible answers: one correct answer and two incorrect ones. 

For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

Your output should be shaped as follows:

1. An outer list that contains 5 inner lists.
2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
- The generated question.
- The correct answer.
- The first incorrect answer.
- The second incorrect answer.

Your output should mirror this structure:
[
    ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
    ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
    ...
]

It is crucial that you adhere to this format as it's optimized for further Python processing.

"""

context_limit = 4097
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)
chain = LLMChain(
    llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY),
    prompt=chat_prompt,
)
quiz_data = chain.run(transcript)

print(quiz_data)
