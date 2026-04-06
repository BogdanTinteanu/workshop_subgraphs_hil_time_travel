# LangGraph: Subgraphs + Human-in-the-Loop + Time Travel

Trei exemple separate, rulabile, care demonstrează fiecare câte o funcționalitate de bază a LangGraph.
Fiecare exemplu se construiește pe cel anterior — citește-le în ordine dacă ești nou în LangGraph.

---

## Ce este LangGraph?

LangGraph este o bibliotecă pentru construirea fluxurilor AI ca **grafuri** — gândește-te la el ca la o diagramă de flux în care fiecare casetă este un pas pe care îl face AI-ul tău, iar săgețile conectează pașii în ordine.

Fiecare exemplu de aici folosește aceeași idee simplă: trece un text printr-o serie de pași, transformându-l pe parcurs.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Blocul de construcție comun

Fiecare exemplu trece o singură valoare prin graf — un text:

```python
class SharedState(TypedDict):
    text: str
```

Gândește-te la `SharedState` ca la un rucsac care este transmis de la pas la pas. Fiecare pas poate citi din el sau poate adăuga ceva în el.

---

## Exemplul 1 — Subgraphs (`ex_1_subgraphs`)

**Conceptul:** Un graf în interiorul unui graf.

Uneori un pas din fluxul tău este suficient de complex pentru a merita propriul mini-graf. În loc să înghesuiești totul într-un graf mare, îl separi într-un **subgraph** — un graf separat, de sine stătător, pe care graful principal îl apelează ca pe orice alt pas.

**Flow:**

```
draft → subgraph → final
```

| Pas | Ce se întâmplă |
|-----|----------------|
| `draft` | Creează textul inițial: `"The quick brown fox jumps over the lazy dog."` |
| `subgraph` | Transmite textul unui mini-graf care îl rafinează prin adăugarea `" (refined by subgraph)"` |
| `final` | Marchează textul final cu eticheta `[FINAL]` |

**De ce să folosești subgraphs?**
- Menține logica complexă izolată și reutilizabilă
- Graful principal nu trebuie să știe ce se întâmplă în interiorul subgraph-ului
- Poți înlocui subgraph-ul fără a atinge restul fluxului

```bash
python -m ex_1_subgraphs.main
```

**Output așteptat:**
```
=== RUN: SUBGRAPHS DEMO ===

[Node] Drafting initial text...

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...

[Node] Preparing final output...

Final Output:
[FINAL] The quick brown fox jumps over the lazy dog. (refined by subgraph)
```

---

## Exemplul 2 — Human-in-the-Loop (`ex_2_human_in_the_loop`)

**Conceptul:** Pauza AI-ului și solicitarea unui input de la o persoană reală.

Nu orice decizie AI trebuie să fie complet automatizată. Human-in-the-loop îți permite să **întrerupi** graful în mijlocul execuției, să arăți rezultatul curent unei persoane și să o lași să aprobe sau să îl corecteze înainte ca graful să continue.

Acest exemplu folosește `MemorySaver` (checkpointing) și `interrupt_before` pentru a opri automat execuția înainte de pasul de review, apoi a o relua într-un al doilea apel invoke.

**Flow:**

```
draft → subgraph → [pauză] → review
```

| Pas | Ce se întâmplă |
|-----|----------------|
| `draft` | Creează textul inițial |
| `subgraph` | Rafinează textul (același mini-graf ca în Exemplul 1) |
| `[pauză]` | Graful se oprește automat — starea este salvată într-un checkpoint |
| `review` | **Reia și te întreabă:** aprobă ca atare, sau introdu text nou |

**De ce să folosești human-in-the-loop?**
- Prinde greșelile înainte ca acestea să se propage mai departe în flux
- Permite oamenilor să rămână în control asupra deciziilor importante
- Util pentru moderarea conținutului, aprobări, sau oriunde acuratețea contează

```bash
python -m ex_2_human_in_the_loop.main
```

**Ce vei vedea:**
```
=== RUN 1: Draft text (pause before review) ===

[Node] Drafting initial text...

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...
[Paused before review node]

=== RUN 1 (continued): Resume for human review ===

[Node] Human Review
Current Output: The quick brown fox jumps over the lazy dog. (refined by subgraph)
Approve or edit? (yes/edit):
```

Tastează `yes` pentru a aproba, sau `edit` pentru a înlocui textul cu ceva propriu.

---

## Exemplul 3 — Time Travel (`ex_3_time_travel`)

**Conceptul:** Salvează fiecare pas, apoi întoarce-te în timp și rulează din nou de la orice punct.

LangGraph poate salva un **checkpoint** (o captură a stării) după fiecare pas. Asta înseamnă că poți privi înapoi la istoricul complet al unei rulări, alege orice moment anterior, schimba ceva și relua graful de acolo — ca un buton de undo pentru fluxul tău AI.

**Flow:**

```
draft → subgraph → review   (oprit automat aici)
```

Demo-ul are patru faze:

| Faza | Ce se întâmplă |
|------|----------------|
| **Run 1** | Rulează graful normal, se oprește automat înainte de `review` |
| **Run 1 (continued)** | Reia de la pauză și finalizează human review |
| **Run 2** | Revine la checkpoint-ul de dinaintea `subgraph`, suprascrie textul, apoi reia — se oprește din nou înainte de `review` |
| **Run 2 (continued)** | Reia de la pauză și finalizează human review cu starea din time travel |

**De ce să folosești time travel?**
- Depanează o rulare eșuată reluând-o cu o corecție
- Testează scenarii „ce-ar fi dacă" prin ramificarea dintr-o stare anterioară
- Recuperează dintr-un output AI prost fără a reporni de la zero

```bash
python -m ex_3_time_travel.main
```

**Output așteptat:**
```
=== RUN 1: Initial run (pauses before review) ===

[Node] Drafting initial text...

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...
[Paused before review node]

=== RUN 1 (continued): Resume for human review ===

[Node] Human Review
Current Output: The quick brown fox jumps over the lazy dog. (refined by subgraph)
Approve or edit? (yes/edit):

=== RUN 2: TIME TRAVEL (Start from subgraph) ===

[Node] Refining text via subgraph...
[Subgraph] Adding text from subgraph...
[Paused before review node]

=== RUN 2 (continued): Resume for human review ===

[Node] Human Review
Current Output: Overridden before subgraph. (refined by subgraph)
Approve or edit? (yes/edit):

Final output after time travel + human review:
Overridden before subgraph. (refined by subgraph)
```

Observă că în Run 2, `draft` este **sărit** — graful a sărit direct la `subgraph` folosind checkpoint-ul salvat, cu textul suprascris injectat în acel punct. Ambele rulări finalizează pasul complet de human review înainte de a se încheia.

---

## Cum se leagă exemplele între ele

```
Exemplul 1 (Subgraphs)
  └── Exemplul 2 (Human-in-the-Loop) — adaugă checkpointing și un pas de human review
        └── Exemplul 3 (Time Travel) — adaugă inspecția istoricului stării și reluarea
```

Fiecare exemplu adaugă o nouă capabilitate pe deasupra aceleiași structuri de bază a grafului.

---

## Structura proiectului

```
ex_1_subgraphs/
  state.py       — definește SharedState (rucsacul comun)
  subgraph.py    — mini-graful care rafinează textul
  nodes.py       — pașii individuali (draft_text, run_subgraph, final_output)
  main.py        — construiește și rulează graful complet

ex_2_human_in_the_loop/
  state.py
  subgraph.py
  nodes.py       — similar cu ex_1, dar pasul human_review înlocuiește final_output
  main.py

ex_3_time_travel/
  state.py
  subgraph.py
  nodes.py
  main.py        — rulează de două ori: rulare normală, apoi fork prin time travel dintr-un checkpoint anterior
```

---

## Glosar de termeni

| Termen (EN) | Explicație |
|-------------|------------|
| **Graph** | Graf — structura principală din LangGraph; o rețea de pași (noduri) conectați prin săgeți (muchii) care definesc ordinea execuției |
| **Node** | Nod — un pas individual din graf; o funcție Python care primește starea, face ceva cu ea și o returnează modificată |
| **Edge** | Muchie — conexiunea dintre două noduri; spune grafului „după pasul A, mergi la pasul B" |
| **State** | Stare — datele care circulă prin graf de la un nod la altul (în exemplele noastre, un dicționar cu câmpul `text`) |
| **Subgraph** | Subgraf — un graf complet de sine stătător, apelat ca un singur pas din interiorul unui graf mai mare |
| **Human-in-the-Loop** | Intervenție umană în buclă — mecanism prin care graful se oprește în mijlocul execuției și așteaptă ca un om să aprobe sau să corecteze rezultatul înainte de a continua |
| **Time Travel** | Călătorie în timp — capacitatea de a inspecta istoricul stărilor unei rulări și de a relua graful de la orice punct anterior |
| **Checkpoint** | Punct de salvare — o captură a stării complete a grafului, salvată automat după fiecare pas; stă la baza atât a human-in-the-loop, cât și a time travel |
| **MemorySaver** | Modul de salvare în memorie — implementare simplă de checkpointing care păstrează toate stările în memoria RAM (util pentru dezvoltare și testare) |
| **interrupt_before** | Întrerupe înainte — opțiune de compilare a grafului care îi spune să se oprească automat *înainte* de a executa un anumit nod |
| **invoke** | Invocare — apelul principal pentru a porni sau a relua execuția unui graf (`graph.invoke(...)`) |
| **fork** | Bifurcare — crearea unei noi ramuri de execuție plecând dintr-un checkpoint anterior, fără a modifica rularea originală |
| **Draft** | Ciornă — primul pas dintr-un flux, care generează versiunea inițială a unui text sau rezultat |
| **Review** | Revizuire — pasul în care un om (sau un alt sistem) verifică și aprobă sau modifică rezultatul curent |
| **Flow** | Flux — ordinea în care nodurile unui graf sunt executate |
| **Output** | Ieșire / Rezultat — datele produse la finalul execuției grafului sau al unui nod |
| **Input** | Intrare — datele furnizate grafului la pornire |
| **Setup** | Configurare — pașii de pregătire a mediului de lucru (instalarea dependențelor, etc.) |
| **TypedDict** | Dicționar tipizat — tip Python din modulul `typing` care permite definirea unui dicționar cu chei și tipuri de valori fixe; folosit pentru a defini structura stării |
| **thread_id** | ID de fir — identificator unic al unei conversații sau sesiuni; permite checkpointing-ului să separe stările mai multor rulări paralele |
