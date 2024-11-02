from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Document
from .document_handler import extract_text_from_pdf
from .qa_engine import answer_question
import os

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Extract text from the uploaded PDF
    text = extract_text_from_pdf(file_location)
    os.remove(file_location)

    # Save document text and metadata to database
    db_doc = Document(name=file.filename, content=text)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    return {"document_id": db_doc.id, "content": text[:500]}  # Return the first 500 characters

@app.post("/answer")
async def answer(document_id: int, question: str, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Generate answer
    answer = answer_question(question, document.content)
    return {"answer": answer}
