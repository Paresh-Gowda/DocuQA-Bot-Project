function PdfUpload() {
  return (
    <section className="upload-card">
      <div className="upload-icon">📄</div>
      <h2>Upload your PDF</h2>
      <p>Drag & drop your document here or browse your files.</p>
      <input type="file" accept=".pdf,application/pdf" />
      <button>Summarize PDF</button>
    </section>
  );
}
export default PdfUpload;
