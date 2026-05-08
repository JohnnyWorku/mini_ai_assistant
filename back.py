import os
from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_neo4j import Neo4jGraph
from langchain_core.output_parsers import PydanticOutputParser


from query_validator import CypherQuery


# Load environment variables from .env file
load_dotenv()


llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
    api_key=os.getenv("GROQ_API_KEY")
)


# Connecting with neo4j
graph = Neo4jGraph(
    url = os.getenv("LOCAL_NEO4J_URI"),
    username = os.getenv("LOCAL_NEO4J_USERNAME"),
    password= os.getenv("LOCAL_NEO4J_PASSWORD"),
    database=os.getenv("LOCAL_NEO4J_DB")
)

parser = PydanticOutputParser(
    pydantic_object=CypherQuery
)


def get_schema():
    return graph.schema


def generate_cypher(question, schema):
    prompt = f"""
    You are a Neo4j expert.
    
    shcema:
    {schema}
    
    Convert the user question into a valid Cypher query.
    
    Rules:
    - Use ONLY schema elements provided
    - Return ONLY JSON
    - No markdown
    - No explanation
    - No dangerous operations
    
    {parser.get_format_instructions()}
    
    
    User Question:
    {question}
    """
    
    response = llm.invoke(prompt)
    parsed_content = parser.parse(response.content)
        
    return parsed_content.cypher


# To validate its syntax correctness
def validate_with_neo4j(cypher: str):
    try:
        graph.query(f"EXPLAIN {cypher}")
        
    except Exception as e:
        raise ValueError(f"Neo4j syntax validation failed: {str(e)}")


def run_query(cypher):
    return graph.query(cypher)


def format_results(results):
    if not results:
        return "No such data found."
    
    formatted = []

    for row in results:
        formatted.append(", ".join(f"{key}: {value}" for key, value in row.items()))
        
    return "\n".join(formatted)


def generate_humanized_answer(question, context):
    prompt = f"""
    Answer the user's question using ONLY the provided data.
    
    Question:
    {question}
    
    Data:
    {context}
    
    Answer:
    """
    
    response = llm.invoke(prompt)
    return response.content.strip()
    
    
def ask_the_graph(question):
    try:
        schema = get_schema()
        
        cypher = generate_cypher(question, schema)
        
        print("\nGenerated cypher:\n", cypher)
        
        validate_with_neo4j(cypher)
        
        results = run_query(cypher)
        
        print("\nRaw results:\n", results)
        
        context = format_results(results)
        
        print("\nContext:\n", context)
        
        final_answer = generate_humanized_answer(question, context)
        
        return final_answer
    
    except Exception as e:
        return f"""
            Error: The generated Cypher query was invalid or unsafe.

            Details:
                {str(e)}
        """

