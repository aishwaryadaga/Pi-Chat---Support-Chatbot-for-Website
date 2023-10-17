from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import dotenv
import constants
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA, ConversationChain
import pinecone
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import openai
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings

load_dotenv()
config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']


bot_name = "Pi"

session_messages = []
responses = ['How can I assist you?']
requests = []
buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)


system_msg_template = SystemMessagePromptTemplate.from_template(template="""You are Pi, a chatbot for Pi Datacenters. Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

llm = ChatOpenAI(
        temperature=0, 
        model='gpt-3.5-turbo'
    )

conversation = ConversationChain(memory=buffer_memory, prompt=prompt_template, llm=llm, verbose=True)
# embeddings = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = OpenAIEmbeddings()

pinecone.init(
    # api_key="e194fde6-59d7-445e-aa6d-71622ffdb296", --> api key has been loaded from .env file
    environment= constants.PINECONE_ENVIRONMENT
    )


# def find_match(input):
#     input_em = embeddings.encode(input).tolist()
#     result = constants.PINECONE_INDEX.query(input_em, top_k=2, includeMetadata=True)
#     return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

#This function will help us in fetching the top relevent documents from our vector store - Pinecone Index
def get_similar_docs(query,k=2):
    index = Pinecone.from_existing_index(constants.PINECONE_INDEX, embeddings)
    similar_docs = index.similarity_search(query, k=k)
    return similar_docs



def query_refiner(conversation, query):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(responses)-1):
        conversation_string += "Human: "+requests[i] + "\n"
        conversation_string += "Bot: "+ responses[i+1] + "\n"
    return conversation_string


def get_response(msg):
    conversation_string = get_conversation_string()
    refined_query = query_refiner(conversation_string, msg)
    context = get_similar_docs(refined_query, k=2)
    response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{msg}")
    requests.append(msg)
    responses.append(response)

    return response



if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(bot_name+": " + resp)

 