import { useEffect, useState } from "react";
function DocumentHistory({ activeFileId, onSelectDocument, refreshTrigger }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const fetchDocuments = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/api/documents`,
      );
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to load documents.");
      }
      setDocuments(data);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);
  const handleDelete = async (fileId) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/api/documents/${fileId}`,
        {
          method: "DELETE",
        },
      );
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Failed to delete document.");
      }
      setDocuments((currentDocuments) =>
        currentDocuments.filter((document) => document.file_id !== fileId),
      );
      if (activeFileId === fileId) {
        onSelectDocument(null);
      }
    } catch (error) {
      setMessage(error.message);
    }
  };
  if (loading) {
    return (
      <section className="document-history">
        <h2>📚 Your Documents</h2>
        <p className="history-message">Loading documents...</p>
      </section>
    );
  }
  return (
    <section className="document-history">
      <h2>📚 Your Documents</h2>
      {message && <p className="history-message">{message}</p>}
      {documents.length === 0 ? (
        <p className="history-empty">No documents uploaded yet.</p>
      ) : (
        <div className="document-list">
          {documents.map((document) => (
            <div
              className={`document-card ${
                activeFileId === document.file_id ? "active-document" : ""
              }`}
              key={document.file_id}
            >
              <div className="document-info">
                <h3>📄 {document.filename}</h3>
                <p>
                  {document.pages} pages • {document.chunks} chunks
                </p>
                <small>
                  Uploaded: {new Date(document.uploaded_at).toLocaleString()}
                </small>
              </div>
              <div className="document-actions">
                <button
                  className="open-document-button"
                  onClick={() => onSelectDocument(document.file_id)}
                >
                  Open
                </button>
                <button
                  className="delete-document-button"
                  onClick={() => handleDelete(document.file_id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
export default DocumentHistory;
