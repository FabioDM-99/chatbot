# YouTube Transcript-Based Chatbot with Pinecone, OpenAI, and LangChain

This project is a smart chatbot leveraging YouTube transcriptions to respond to user queries. It employs Pinecone for storing and retrieving text embeddings and OpenAI's GPT-3.5 for generating responses based on relevant transcript segments. The project also utilizes LangChain for handling language embeddings and related operations.

## Prerequisites

1. Python 3.6 or higher.
2. Pinecone account with an API key.
3. OpenAI account with an API key.
4. LangChain configured for handling embeddings.

## Installation

Clone this repository to your local machine using:

```bash
git clone REPO_URL
```

Navigate to the directory of the cloned project.

## Configuration

1. **Environment Variables:**  
   Create a `.env` file in the project's root and add your API keys as follows:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

   This project uses `python-dotenv` to load these environment variables. Never hard-code your API keys directly into your code.

2. **Dependencies:**  
   Install all required dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file should be created and include:

   ```plaintext
   openai
   pinecone-io
   python-dotenv
   langchain
   ```

## Usage

After setting up the environment variables and installing dependencies, you can run the script `main.py` (or whatever your main script is named):

```bash
python main.py
```

The program will start running in the terminal. You can ask questions related to the loaded YouTube transcription, and the chatbot will respond accordingly. Type 'exit' to stop the program.

## Features

- **Pinecone Integration:**  
  The chatbot creates embeddings for each text segment from the transcription and stores them in a Pinecone index. It then uses Pinecone to perform similarity searches and find the most relevant segments in response to a user's query.

- **OpenAI Integration:**  
  Employs GPT-3.5 to generate dynamic responses based on relevant transcript segments.

- **LangChain Utilization:**  
  Handles the creation and management of language embeddings, enhancing the chatbot's linguistic capabilities.

- **Looped Querying:**  
  The chatbot can receive and respond to a series of questions until the user decides to exit by typing 'exit'.

## Contributing

Contributions are welcome! To contribute, please fork the repository, create a new branch for each feature or fix, and submit a pull request after pushing your changes.
