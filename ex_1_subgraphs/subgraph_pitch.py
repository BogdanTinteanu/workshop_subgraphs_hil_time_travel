from groq import Groq
from langgraph.graph import StateGraph
from .state import SharedState
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def draft_pitch(state: SharedState):
    print("\n[Subgraph Pitch] Generating pitch...")
    
    # Adaptam tonul in functie de calificare
    tone = "entuziast si direct" if state["qualification"] == "HOT" else "formal si consultativ"
    
    system_prompt = (
        f"Esti un expert in vanzari B2B. Scrie un email de pitch {tone}. "
        "Fii extrem de concis (max 50 cuvinte). Adreseaza-te specific industriei."
    )
    
    user_content = (
        f"Lead: {state['lead_name']} la {state['company']} ({state['industry']}). "
        f"Calificat ca {state['qualification']} deoarece: {state['qualification_reason']}."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )

    return {"pitch": response.choices[0].message.content}

def build_pitch_subgraph():
    builder = StateGraph(SharedState)
    builder.add_node("draft_pitch", draft_pitch)
    builder.set_entry_point("draft_pitch")
    builder.set_finish_point("draft_pitch")
    return builder.compile()
