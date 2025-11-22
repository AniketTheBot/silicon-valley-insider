from app.core.database import neo4j_conn
from langchain_groq import ChatGroq
from app.core.config import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize LLM
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0
)

def contextualize_question(question: str, history: list):
    """
    Uses the LLM to rewrite the question based on history.
    Example: "Who fired him?" -> "Who fired Sam Altman?"
    """
    if not history:
        return question

    # Format history into a string
    history_str = "\n".join([f"{msg['role']}: {msg['text']}" for msg in history])

    system_prompt = """
    Given a chat history and the latest user question which might reference context in the chat history, 
    formulate a standalone question which can be understood without the chat history. 
    DO NOT answer the question, just reformulate it if needed and otherwise return it as is.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Chat History:\n{history}\n\nLatest Question: {question}"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    print("⏳ Contextualizing question...")
    new_question = chain.invoke({"history": history_str, "question": question})
    print(f"🔄 Rephrased: '{question}' -> '{new_question}'")
    return new_question

def get_graph_context(entity_names: list):
    # ... (Keep existing logic) ...
    session = neo4j_conn.get_session()
    query = """
    MATCH (n)-[r]-(m)
    WHERE n.id IN $names
    RETURN n.id, type(r) as relationship, r.sentiment as sentiment, m.id as target
    LIMIT 50
    """
    results = session.run(query, names=entity_names)
    context_lines = []
    for record in results:
        line = f"{record['n.id']} is connected to {record['target']} via {record['relationship']} ({record['sentiment']})"
        context_lines.append(line)
    session.close()
    return "\n".join(context_lines)

def get_general_context():
    # ... (Keep existing logic) ...
    session = neo4j_conn.get_session()
    query = """
    MATCH (n)-[r]->(m)
    RETURN n.id, type(r) as relationship, r.sentiment as sentiment, m.id as target
    LIMIT 20
    """
    results = session.run(query)
    context_lines = []
    for record in results:
        line = f"{record['n.id']} {record['relationship']} {record['target']} (Sentiment: {record['sentiment']})"
        context_lines.append(line)
    session.close()
    return "\n".join(context_lines)

def answer_question(question: str, history: list = []): # <--- Accepts history
    
    # 1. CONTEXTUALIZE (The Magic Step)
    # Replaces "him/it/they" with actual names
    refined_question = contextualize_question(question, history)

    # 2. EXTRACT ENTITIES (Using the REFINED question)
    extraction_prompt = ChatPromptTemplate.from_messages([
        ("system", """
         You are a precise Entity Extractor API. 
         Your ONLY job is to extract entity names from the user's question.
         RULES:
         1. Return ONLY a comma-separated list of names (e.g. "Microsoft, Sam Altman").
         2. If no specific Company, Person, or Product is named, return exactly the word "None".
         3. DO NOT output any explanation. JUST the names.
         """),
        ("human", "{question}"),
    ])
    
    entity_chain = extraction_prompt | llm
    response = entity_chain.invoke({"question": refined_question}).content.strip()
    
    # Clean up response
    if ":" in response: response = response.split(":")[-1].strip()
    response = response.replace("**", "").replace('"', '').replace("'", "")
    
    print(f"🕵️ AI Extracted: '{response}'")

    # 3. GRAPH LOOKUP
    if response.lower() == "none" or response == "":
        print("🌍 General Question detected.")
        context = get_general_context()
        entity_list = ["Global Context"]
        if not context: context = "The graph is currently empty."
    else:
        entity_list = [e.strip() for e in response.split(",")]
        print(f"🔍 Looking up entities: {entity_list}")
        context = get_graph_context(entity_list)
        if not context:
            return {
                "entity": str(entity_list),
                "context": "No data",
                "answer": f"I couldn't find records for {response} in the database."
            }

    # 4. GENERATE ANSWER
    rag_prompt = ChatPromptTemplate.from_template(
        """
        You are a Data Analyst. Answer strictly based on the database context.
        
        Context:
        {context}
        
        User Question: {question}
        
        Answer (Max 3 sentences):
        """
    )
    
    answer_chain = rag_prompt | llm
    final_response = answer_chain.invoke({"context": context, "question": refined_question})
    
    return {
        "entity": str(entity_list),
        "context": context,
        "answer": final_response.content
    }