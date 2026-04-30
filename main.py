import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain

# Load environment variables from .env file
load_dotenv()

# Intialize the Google Generative AI model
llm = ChatGoogleGenerativeAI(model=os.getenv("MODEL"), google_api_key=os.getenv("GOOGLE_API_KEY"))

# Connecting with neo4j
graph = Neo4jGraph(
    # url = os.getenv("LOCAL_NEO4J_URI"),
    # username = os.getenv("LOCAL_NEO4J_USERNAME"),
    # password= os.getenv("LOCAL_NEO4J_PASSWORD"),
    # database=os.getenv("LOCAL_NEO4J_DB")
    
    url = os.getenv("LOCAL_NEO4J_URI"),
    username = os.getenv("LOCAL_NEO4J_USERNAME"),
    password= os.getenv("LOCAL_NEO4J_PASSWORD"),
    database=os.getenv("LOCAL_NEO4J_DB")
)

chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)

    
def main_agent():
    try:
        print("The agent is running ...: Type 'exit/quit' to stop the agent.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exting the agent. Goodbye!")
                break
            
            response = chain.invoke({"query": user_input})
            print(f"AI agent: {response}")
            
    except Exception as e:
        print(f"An error occured: {e}")
    
if __name__ == "__main__":
    main_agent()
