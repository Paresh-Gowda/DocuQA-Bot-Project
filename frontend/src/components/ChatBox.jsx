import { useState } from "react";
import ReactMarkdown from "react-markdown";
function ChatBox({ fileId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const handleAsk = async () => {
    if (!fileId) {
      setMessage("Please upload a PDF first.");
      return;
    }
    if (!question.trim()) {
      setMessage("Please enter a question.");
      return;
    }
    setLoading(true);
    setMessage("");
    setAnswer("");
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/question`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
          file_id: fileId,
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to get an answer.");
      }
      setAnswer(data.answer);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <section className="chat-section">
      <h2>💬 Ask about your document</h2>
      <div className="chat-box">
        <input
          type="text"
          placeholder={
            fileId
              ? "Ask a question about your document..."
              : "Upload a PDF first..."
          }
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              handleAsk();
            }
          }}
          disabled={!fileId || loading}
        />
        <button onClick={handleAsk} disabled={!fileId || loading}>
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
      {message && <p className="chat-message">{message}</p>}
      {answer && (
        <div className="answer-card">
          <h3>🤖 Answer</h3>
          <div className="markdown-content">
            <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
        </div>
      )}
    </section>
  );
}
export default ChatBox;
