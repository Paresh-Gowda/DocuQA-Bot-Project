import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
function Summary({ uploaded }) {
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  useEffect(() => {
    if (!uploaded) {
      setSummary("");
      setMessage("");
      return;
    }
    const generateSummary = async () => {
      setLoading(true);
      setMessage("");
      setSummary("");
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/api/summary`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            file_id: uploaded,
          }),
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
    generateSummary();
  }, [uploaded]);
  return (
    <section className="summary-section">
      <h2>📝 Summary</h2>
      <div className="summary-card">
        {loading && <p>Generating summary...</p>}
        {message && <p>{message}</p>}
        {summary && (
          <div className="markdown-content">
            <ReactMarkdown>{summary}</ReactMarkdown>
          </div>
        )}
        {!uploaded && !summary && (
          <p>Your document summary will appear here after you upload a PDF.</p>
        )}
      </div>
    </section>
  );
}
export default Summary;
