import { useState } from "react";
import PdfUpload from "../components/PdfUpload";
import Summary from "../components/Summary";
import ChatBox from "../components/ChatBox";
function Home() {
  const [uploaded, setUploaded] = useState(false);
  return (
    <main className="home">
      <section className="hero">
        <h1>Chat with your documents</h1>
        <p>
          Upload a PDF and use AI to summarize it and answer your questions.
        </p>
      </section>
      <PdfUpload onUploadSuccess={() => setUploaded(true)} />
      <Summary uploaded={uploaded} />
      <ChatBox />
    </main>
  );
}
export default Home;
