# TODO: Articol de Presa cu Human Review si Time Travel

**Timp estimat: 25 minute**

## Arhitectura

```
[agent_write_article] → [subgraph: editor_final] → [human_review]
                                                          ↑
                                                     omul aproba
                                                     sau rescrie
                                                          ↓
                                              TIME TRAVEL: revino la
                                              subgraph cu text modificat
```

---

## TODO 1 — `state.py`
Adauga campurile necesare in `GraphState`:
- `article` — articolul generat (string)
- `approved` — boolean care indica daca omul a aprobat articolul

---

## TODO 2 — `nodes.py` — nodul `agent_write_article`
Inlocuieste `generate_text` cu un nod care apeleaza Groq pentru a genera un articol de presa scurt.

```python
from groq import Groq
from ex_3_time_travel.state import GraphState

client = Groq()

def agent_write_article(state: GraphState):
    print("\n[Node] Agent Write Article (Groq)...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Esti un jurnalist. Scrie un articol de presa scurt (3-5 propozitii) despre un eveniment fictiv. Returneaza doar articolul, fara titlu sau explicatii.",
            },
            {
                "role": "user",
                "content": "Scrie un articol de presa.",
            },
        ],
    )

    state["article"] = response.choices[0].message.content
    print("\n[Agent] Articol generat:\n", state["article"])
    return state
```

---

## TODO 3 — `subgraph.py` — nodul `editor_final`
Subgraful are un nod `editor_final` care:
- Primeste `state["article"]`
- Adauga un header de presa deasupra articolului:
  ```
  === ARTICOL DE PRESA ===
  <articolul>
  ========================
  ```
- Returneaza state-ul actualizat

---

## TODO 4 — `nodes.py` — nodul `human_review`
Nodul afiseaza articolul formatat si asteapta decizia omului:
- Daca raspunsul este `"edit"`, citeste articolul nou pastat (multi-line, terminat cu `###`)
- Seteaza `state["approved"] = True` in ambele cazuri

```python
def human_review(state: GraphState):
    print("\n[Review] Articol curent:\n", state["article"])
    decizie = input("\nAproba sau editeaza? (yes/edit): ")

    if decizie.lower() == "edit":
        print("Lipeste articolul nou, apoi scrie '###' pe o linie separata si apasa Enter:")
        lines = []
        while True:
            line = input()
            if line.strip() == "###":
                break
            lines.append(line)
        state["article"] = "\n".join(lines)

    state["approved"] = True
    return state
```

---

## TODO 5 — `main.py`
Conecteaza nodurile si adauga **Time Travel**:

```
agent_write_article → subgraph → human_review
```

Compileaza cu `MemorySaver` si `interrupt_before=["human_review"]`:

```python
app = build_graph()
config = {"configurable": {"thread_id": "thread-1"}}

# RUN 1: genereaza articolul, pauza inainte de review
app.invoke({"article": "", "approved": False}, config=config)

# RUN 1 (continued): resume pentru human review
app.invoke(None, config=config)

# TIME TRAVEL: gaseste checkpoint-ul inainte de subgraph
history = list(app.get_state_history(config))
target = next(s for s in history if s.next == ("subgraph",))

# Modifica articolul la acel checkpoint
updated_config = app.update_state(target.config, {"article": "Articol modificat prin time travel."})

# Replay de la checkpoint modificat — pauza inainte de review
app.invoke(None, config=updated_config)

# Resume final cu human review
result = app.invoke(None, config=config)

print("\nArticol final dupa time travel + human review:")
print(result["article"])
print("Aprobat:", result["approved"])
```

---

## Testare

- [ ] Ruleaza si alege `yes` — verifica ca articolul generat de Groq apare formatat in output final
- [ ] Ruleaza din nou si alege `edit` — verifica ca articolul editat de om (multi-line) este folosit in output final
- [ ] Verifica time travel — articolul modificat la checkpoint trece din nou prin `editor_final` inainte de review

---

## Rulare
```bash
python -m ex_3_time_travel.main
```
