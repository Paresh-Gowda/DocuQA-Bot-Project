import { useRef, useState } from "react";
function PdfUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);
  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    if (
      selectedFile.type !== "application/pdf" &&
      !selectedFile.name.toLowerCase().endsWith(".pdf")
    ) {
      setMessage("Please select a PDF file.");
      setFile(null);
      return;
    }
    setFile(selectedFile);
    setMessage("");
  };
  const handleFileChange = (event) => {
    handleFile(event.target.files[0]);
  };
  const handleDrop = (event) => {
    event.preventDefault();
    setDragging(false);
    const droppedFile = event.dataTransfer.files[0];
    handleFile(droppedFile);
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
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/api/upload`,
        {
          method: "POST",
          body: formData,
        }
      );
      const data = await response.json();
      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to upload PDF."
        );
      }
      setMessage(
        `PDF uploaded successfully! ${data.chunks} chunks created.`
      );
      onUploadSuccess(data.file_id);
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };
  const handleClear = () => {
    setFile(null);
    setMessage("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };
  return (
    <section className="upload-section">
      <h2>📄 Upload a PDF</h2>
      <div
        className={`upload-dropzone ${
          dragging ? "dragging" : ""
        }`}
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="upload-icon">📄</div>
        <p>
          Drag & drop your PDF here
        </p>
        <span>or click to browse</span>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          hidden
        />
      </div>
      {file && (
        <div className="selected-file">
          <div>
            <strong>📄 {file.name}</strong>
            <p>
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
          </div>
          <button
            type="button"
            className="clear-file-button"
            onClick={handleClear}
            disabled={loading}
          >
            ✕
          </button>
        </div>
      )}
      <button
        className="upload-button"
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? "⏳ Processing..." : "⬆️ Upload PDF"}
      </button>
      {message && (
        <p className="upload-message">
          {message}
        </p>
      )}
    </section>
  );
}
export default PdfUpload;