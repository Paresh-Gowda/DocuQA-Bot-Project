import { useState } from "react";
function Summary({ uploaded }) {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const generateSummary = async () => {
    setLoading(true);
    setMessage("");
    try {
      const response = await fetch("http://127.0.0.1:8000/api/summary", {
        method: "POST",
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to generate summary.");
      }
      setSummary(data.summary);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };
  if (uploaded && !summary && !loading) {
    generateSummary();
  }
  return (
    <section className="summary-section">
      <h2>📝 Summary</h2>
      <div className="summary-card">
        {loading && <p>Generating summary...</p>}
        {message && <p>{message}</p>}
        {summary && <p>{summary}</p>}
        {!uploaded && !summary && (
          <p>Your document summary will appear here after you upload a PDF.</p>
        )}
      </div>
    </section>
  );
}
export default Summary;
