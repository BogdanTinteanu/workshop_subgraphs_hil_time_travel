from groq import Groq
from langgraph.graph import StateGraph
from .state import SharedState
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_lead(state: SharedState):
    print("\n[Subgraph Qualify] Analyzing lead...")
    
    system_prompt = (
        "Esti un agent expert in calificare vanzari pentru solutii de Cybersecurity. "
        "Analizeaza datele si raspunde strict in acest format:\n"
        "CALIFICARE: [HOT/WARM/COLD]\n"
        "MOTIV: [Explicatie scurta]\n\n"
        "Criterii: Buget > 50k = HOT, Industrie Tech/Finante = WARM/HOT."
    )
    
    user_content = (
        f"Lead: {state['lead_name']}\nCompanie: {state['company']}\n"
        f"Industrie: {state['industry']}\nBuget: {state['budget']}"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    )

    content = response.choices[0].message.content
    print("[Qualify] Raspuns Groq:", content)

    # Parsing logic
    qualification = "WARM"
    reason = content
    for line in content.splitlines():
        if line.upper().startswith("CALIFICARE:"):
            val = line.split(":", 1)[1].strip().upper()
            if "HOT" in val: qualification = "HOT"
            elif "COLD" in val: qualification = "COLD"
        elif line.upper().startswith("MOTIV:"):
            reason = line.split(":", 1)[1].strip()

    return {"qualification": qualification, "qualification_reason": reason}

def build_qualify_subgraph():
    builder = StateGraph(SharedState)
    builder.add_node("analyze_lead", analyze_lead)
    builder.set_entry_point("analyze_lead")
    builder.set_finish_point("analyze_lead")
    return builder.compile()
