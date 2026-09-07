import { useState } from "react";
function PdfUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage("");
  };
  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a PDF first.");
      return;
    }
    setLoading(true);
    setMessage("");
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }
      setMessage(`PDF uploaded successfully! ${data.chunks} chunks created.`);
      onUploadSuccess();
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <section className="upload-card">
      <div className="upload-icon">📄</div>
      <h2>Upload your PDF</h2>
      <p>Drag & drop your document here or browse your files.</p>
      <input
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Summarize PDF"}
      </button>
      {message && <p className="upload-message">{message}</p>}
    </section>
  );
}
export default PdfUpload;