# Defines shared state across graph

from typing import TypedDict

class SharedState(TypedDict):
# Date Lead
    lead_name: str
    company: str
    industry: str
    budget: str
    # Rezultate Calificare
    qualification: str # HOT, WARM, COLD
    qualification_reason: str
    # Rezultat Final
    pitch: str
