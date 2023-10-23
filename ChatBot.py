import json
import os
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pinecone setup
pinecone.init(
    api_key='c3a21119-9913-4afe-8025-16406093325b',
    environment='gcp-starter'
)

# Pinecone index name
index_name = 'chatbot-production'

# Delete existing index if it exists
if index_name in pinecone.list_indexes():
    pinecone.delete_index(index_name)

# Create a new index
pinecone.create_index(index_name, 1536, metric='cosine')
index = pinecone.Index(index_name)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")  # Fetch the API key from environment variable

# Use relative paths for data loading
current_directory = Path(__file__).parent
json_file_path = current_directory / 'youtubeTranscription.json'

# Load the transcript from the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

class Document:
    def __init__(self, content, metadata):
        self.page_content = content
        self.metadata = metadata

# Transform data to make it compatible with LangChain
# Including all available metadata from the JSON
documents = [Document(entry["text"], {"sequence": index, "speaker": entry["speaker"]}) for index, entry in enumerate(data)]

# Create embeddings with OpenAI and store in Pinecone
embeddings = OpenAIEmbeddings()
index = Pinecone.from_documents(documents, embeddings, index_name=index_name)

def get_answer_to_question(question):
    # Search for relevant segments from the transcript
    results = index.similarity_search(question, k=5)  # Retrieve the 5 most relevant segments

    # Aggregate segments to provide context to GPT-3.5
    context = "\n".join([f"Sequence {doc.metadata['sequence']} - {doc.metadata['speaker']}: {doc.page_content}" for doc in results])

    # Generate the response with GPT-3.5
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "The following is a transcript segment from a YouTube interview. Please answer strictly based on the provided transcript:"},
            {"role": "user", "content": context},
            {"role": "user", "content": f"Question: {question}\nAnswer:"}
        ]
    )

    return response.choices[0].message['content'].strip()

# Loop to allow the user to ask questions
while True:
    question = input("Please enter your question (or 'exit' to stop): ")
    if question.lower() == 'exit':
        break
    print(get_answer_to_question(question))
