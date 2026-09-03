import PdfUpload from "../components/PdfUpload";
import Summary from "../components/Summary";
import ChatBox from "../components/ChatBox";
function Home() {
  return (
    <main className="home">
      <section className="hero">
        <h1>Chat with your documents</h1>
        <p>
          Upload a PDF and use AI to summarize it and answer your questions.
        </p>
      </section>
      <PdfUpload />
      <Summary />
      <ChatBox />
    </main>
  );
}
export default Home;
