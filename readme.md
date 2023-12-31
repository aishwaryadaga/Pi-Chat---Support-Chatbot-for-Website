# Chatbot using LangChain, OpenAI and Pinecone

Welcome to Pi Chat! This chatbot is designed to generate responses for Pi Datacenters' website using large language models and provide a seamless user experience. It is built with a Flask backend and a frontend created using HTML, CSS, and JavaScript.

## Project Overview

This project aims to demonstrate the capabilities of LangChain and OpenAI to create an intelligent chatbot that can engage in meaningful conversations with users. The architecture consists of the following components:

- **Backend (Flask):** The backend of the chatbot is built using Flask, a Python web framework. It handles user requests, communicates with the LangChain's chat models, and manages the integration with OpenAI's API.

- **Frontend (HTML, CSS, JS):** The frontend is developed using HTML for structuring, CSS for styling, and JavaScript for interactive features. It allows users to interact with the chatbot and view the responses in a user-friendly interface.

- **LangChain Models:** LangChain chat models are utilized to process user input, understand context, and generate coherent responses. They play a key role in providing relevant and context-aware replies to user queries.

- **OpenAI Integration:** The project leverages OpenAI's large language models to enhance the quality and diversity of responses generated by the chatbot. This integration enhances the user experience and makes the conversations more engaging.

- **Pinecone Integration:** The data scraped from the website is stored in the vector database and relevant documents are pulled from here to answer questions.

## Getting Started

1. **Installation:**

   - Clone this repository to your local machine.
   - Install the required Python packages using `pip install -r requirements.txt`.

2. **Configuration:**

   - Obtain API keys and credentials for LangChain and OpenAI.
   - Configure the API endpoints and authentication details in the Flask app.
   - Create .env and .env.example files to store API Keys securely.

3. **Running the App:**
   - Start the Flask server using `python app.py`.
   - Access the chatbot interface by opening the provided URL in your web browser.

## Usage

- Users can visit the chatbot interface via the web browser.
- Input messages and queries in the provided input field.
- The chatbot will process the input, use LangChain models for context analysis, and generate responses using OpenAI's language models.
- Responses will be displayed in the chat interface in real-time.

## Contributions and Feedback

Contributions, suggestions, and feedback are welcome! If you find any issues, have ideas for improvements, or want to contribute new features, feel free to submit pull requests or open issues on the GitHub repository.

## License

---
