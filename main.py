from agents import study_pipeline, doubt_solver
from database import get_notes

# Optional: keep for future use

try:
    from fastapi import FastAPI
except:
    FastAPI = None

if FastAPI:
    app = FastAPI()

    @app.get("/")
    def home():
        return {"message": "Multi-Agent Study AI Running 🚀"}


@app.get("/")
def home():
    return {"message": "Multi-Agent Study AI Running 🚀"}


@app.get("/study")
def study(topic: str):
    try:
        result = study_pipeline(topic)

        print("DEBUG RESULT:", result)

        if not result or "notes" not in result:
            return {"error": "Invalid pipeline response"}

        return result

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}

@app.get("/doubt")
def doubt(topic: str, question: str):
    notes = get_notes(topic)

    if not notes:
        return {"error": "Generate study material first!"}

    answer = doubt_solver(notes, question)
    return {"answer": answer}