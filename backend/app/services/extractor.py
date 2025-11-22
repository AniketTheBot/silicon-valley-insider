from langchain_groq import ChatGroq
from app.core.config import settings
from app.models.schemas import GraphData
from langchain_core.prompts import ChatPromptTemplate


llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",  # Powerful model for logic
    temperature=0
)

structured_llm = llm.with_structured_output(GraphData)


def extract_graph_from_text(text: str):
    system_prompt = """
    You are an expert Knowledge Graph Engineer. 
    Your goal is to extract structured data and enforce strict entity resolution.

    CRITICAL RULES FOR DEDUPLICATION:
    1. **Normalize Names (Companies/People)**:
       - "Microsoft Corp", "MSFT" -> "Microsoft"
       - "Sam Altman", "Samuel Altman" -> "Sam Altman"
       - "Nvidia Corp" -> "Nvidia"
    
    2. **Standardize Product Names (The "Blackwell" Rule)**:
       - ALWAYS use the format: [Brand/Series] [Model]
       - "B200 Blackwell" -> "Blackwell B200"
       - "Blackwell B200 GPU" -> "Blackwell B200"
       - "Gemini 2.0" -> "Gemini 2"
       - "Llama 4 model" -> "Llama 4"
    
    3. **Standardize Relationships (Verbs)**:
       - "Fired", "Dismissed", "Removed", "Ousted" -> "FIRED"
       - "Hired", "Appointed", "Recruited", "Joined" -> "HIRED"
       - "Sued", "Filed Lawsuit" -> "SUED"
       - "Invested", "Bought stake" -> "INVESTED_IN"
       - "Launched", "Released", "Unveiled" -> "LAUNCHED"
       - "Partnered" -> "PARTNERED_WITH"

    Return JSON with 'nodes' and 'edges'.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input_text}"),
    ])

    chain = prompt | structured_llm

    try:
        # Run the AI
        response = chain.invoke({"input_text": text})
        return response
    except Exception as e:
        print(f"AI Extraction Error: {e}")
        return None
