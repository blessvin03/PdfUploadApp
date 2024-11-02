import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [file, setFile] = useState(null);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [documentId, setDocumentId] = useState(null);

    const handleFileUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        const response = await axios.post("http://localhost:8000/upload", formData);
        setDocumentId(response.data.document_id);
        console.log("Uploaded and indexed document:", response.data);
    };

    const handleQuestion = async () => {
        if (!documentId) {
            alert("Please upload a document first.");
            return;
        }

        const response = await axios.post("http://localhost:8000/answer", {
            document_id: documentId,
            question: question
        });

        setAnswer(response.data.answer);
    };

    return (
        <div>
            <h2>PDF Q&A System</h2>
            <input type="file" onChange={e => setFile(e.target.files[0])} />
            <button onClick={handleFileUpload}>Upload PDF</button>

            <input
                type="text"
                placeholder="Ask a question..."
                value={question}
                onChange={e => setQuestion(e.target.value)}
            />
            <button onClick={handleQuestion}>Get Answer</button>

            {answer && <div><strong>Answer:</strong> {answer}</div>}
        </div>
    );
}

export default App;
