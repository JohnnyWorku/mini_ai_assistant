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
    url = os.getenv("LOCAL_NEO4J_URI"),
    username = os.getenv("LOCAL_NEO4J_USERNAME"),
    password= os.getenv("LOCAL_NEO4J_PASSWORD"),
    database=os.getenv("LOCAL_NEO4J_DB")
    
    # url = os.getenv("REMOTE_NEO4J_URI"),
    # username = os.getenv("REMOTE_NEO4J_USERNAME"),
    # password= os.getenv("REMOTE_NEO4J_PASSWORD"),
    # database=os.getenv("REMOTE_NEO4J_DB")
)


def get_schema():
    return graph.schema


def generate_cypher(question, schema):
    prompt = f"""
    You are a Neo4j expert.
    
    shcema:
    {schema}
    
    Convert the question into Cypher query.
    Only return the query.
    No markdown(```).
    No any other elaboration just the cypher only.
    
    Question:
    {question}
    """
    
    response = llm.invoke(prompt)
    content = response.content
    
    if isinstance(content, list):
        content = content[0].get("text", "")
        
    return content


def validate_cypher(cypher: str):
    forbidden = ["DELETE", "CREATE", "MERGE", "DROP"]
    
    for word in forbidden:
        if word in cypher.upper():
            raise ValueError("Dangerous query detected.")
        
    return cypher


def run_query(cypher):
    return graph.query(cypher)


def format_results(results):
    if not results:
        return "No such data found."
    
    formatted = []

    for row in results:
        formatted.append(", ".join(str(value) for value in row.values()))
        
    return "\n".join(formatted)


def generate_humanized_answer(question, context):
    prompt = f"""
    Answer the question using the data below.
    
    Question:
    {question}
    
    Data:
    {context}
    
    Answer:
    """
    
    response = llm.invoke(prompt)
    return response.content
    
    
def ask_the_graph(question):
    try:
        schema = get_schema()
        
        cypher = generate_cypher(question, schema)
        print("\nGenerated cypher:\n", cypher)
        
        cypher = validate_cypher(cypher)
        
        results = run_query(cypher)
        print("\nRaw results:\n", results)
        
        context = format_results(results)
        
        final_answer = generate_humanized_answer(question, context)
        
        return final_answer
    
    except Exception as e:
        return f"""
            Error: The statement you entered is either not changeable to cypher or it has some flaw. Check it.
            If you want see the original error: {str(e)}
        """
    

# chain = GraphCypherQAChain.from_llm(
#     llm=llm,
#     graph=graph,
#     verbose=True,
#     allow_dangerous_requests=True
# )


# def main_agent():
#     try:
#         print("The agent is running ...: Type 'exit/quit' to stop the agent.")
#         while True:
#             user_input = input("You: ")
#             if user_input.lower() in ["exit", "quit"]:
#                 print("Exting the agent. Goodbye!")
#                 break
            
#             response = chain.invoke({"query": user_input})
#             print(f"AI agent: {response}")
            
#     except Exception as e:
#         print(f"An error occured: {e}")
    
# if __name__ == "__main__":
#     main_agent()
