import { useState } from "react";
import PdfUpload from "../components/PdfUpload";
import Summary from "../components/Summary";
import ChatBox from "../components/ChatBox";
import DocumentHistory from "../components/DocumentHistory";
function Home() {
  const [uploaded, setUploaded] = useState(null);
  const [refreshDocuments, setRefreshDocuments] = useState(0);
  const handleNewDocument = () => {
    setUploaded(null);
  };
  return (
    <main className="home">
      <section className="hero">
        <h1>Chat with your documents</h1>
        <p>
          Upload a PDF and use AI to summarize it and answer your questions.
        </p>
      </section>
      <PdfUpload
        onUploadSuccess={(fileId) => {
          setUploaded(fileId);
          setRefreshDocuments((value) => value + 1);
        }}
      />
      <DocumentHistory
        activeFileId={uploaded}
        onSelectDocument={(fileId) => setUploaded(fileId)}
        refreshTrigger={refreshDocuments}
      />
      {uploaded && (
        <div className="new-document-container">
          <button className="new-document-button" onClick={handleNewDocument}>
            + New Document
          </button>
        </div>
      )}
      <Summary uploaded={uploaded} />
      <ChatBox fileId={uploaded} />
    </main>
  );
}
export default Home;
