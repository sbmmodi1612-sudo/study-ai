import anthropic
from config import CLAUDE_API_KEY
from database import save_notes, get_notes

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

def llm(prompt):
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


# 🔍 Research Agent
def research_agent(topic):
    prompt = f"""
    Explain the topic in detail:
    {topic}
    
    Include examples and concepts.
    """
    return llm(prompt)


# 📝 Notes Agent
def notes_agent(data):
    prompt = f"""
    Convert into structured notes:

    {data}

    Format:
    - Headings
    - Bullet points
    - Key points
    """
    return llm(prompt)


# ❓ Quiz Agent
def quiz_agent(notes):
    import json

    for attempt in range(3):  # 🔁 retry 3 times
        prompt = f"""
        Create EXACTLY 5 MCQ questions.

        STRICT RULES:
        - Return ONLY valid JSON
        - No explanation
        - No markdown
        - Must be a list of 5 items

        Format:
        [
          {{
            "question": "text",
            "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
            "answer": "A"
          }}
        ]

        Notes:
        {notes[:2000]}
        """

        response = llm(prompt).strip()
        response = response.replace("```json", "").replace("```", "").strip()

        try:
            data = json.loads(response)

            # ✅ VALIDATION
            if isinstance(data, list) and len(data) == 5:
                return data

        except:
            continue  # retry

    # ❌ FALLBACK (always return something)
    return [
        {
            "question": "Quiz could not be generated. Try again.",
            "options": ["A. Retry", "B. Retry", "C. Retry", "D. Retry"],
            "answer": "A"
        }
    ]

# 🤖 Doubt Solver
def doubt_solver(notes, question):
    prompt = f"""
    Answer using notes:

    Notes:
    {notes}

    Question:
    {question}
    """
    return llm(prompt)


# 🔄 PIPELINE
def study_pipeline(topic):
    # Check memory
    saved_notes = get_notes(topic)

    if saved_notes:
        notes = saved_notes
    else:
        research = research_agent(topic)
        notes = notes_agent(research)
        save_notes(topic, notes)

    quiz = quiz_agent(notes)

    return {
        "notes": notes,
        "quiz": quiz
    }