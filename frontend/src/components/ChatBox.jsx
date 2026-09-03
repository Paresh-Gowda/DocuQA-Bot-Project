function ChatBox() {
  return (
    <section className="chat-section">
      <h2>💬 Ask about your document</h2>
      <div className="chat-box">
        <input
          type="text"
          placeholder="Ask a question about your document..."
        />
        <button>Send</button>
      </div>
    </section>
  );
}
export default ChatBox;
