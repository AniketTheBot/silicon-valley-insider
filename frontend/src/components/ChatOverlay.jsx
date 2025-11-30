import { useState, useRef, useEffect } from "react"; // <--- Added useRef, useEffect
import axios from "axios";

export default function ChatOverlay({ onFocusNode }) {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "system",
      text: "System Online. Connected to Knowledge Graph. Ask me anything.",
    },
  ]);
  const [loading, setLoading] = useState(false);

  // 1. Create a reference for the bottom of the chat
  const messagesEndRef = useRef(null);

  // 2. Scroll to bottom whenever 'messages' change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAsk = async () => {
    if (!query.trim()) return;

    const newMessages = [...messages, { role: "user", text: query }];
    setMessages(newMessages);
    setLoading(true);
    setQuery("");

    try {
      const historyPayload = messages.slice(-5).map((msg) => ({
        role: msg.role === "user" ? "human" : "ai", // LangChain prefers 'human'/'ai'
        text: msg.text,
      }));
      const res = await axios.post("http://72.61.232.29:8000/chat", {
        question: query,
        history: historyPayload,
      });

      setMessages((prev) => [
        ...prev,
        { role: "system", text: res.data.answer },
      ]);

      // Camera Focus Logic
      let entitiesRaw = res.data.entity;
      if (entitiesRaw) {
        let targetNode = entitiesRaw
          .replace(/[\[\]'"]/g, "")
          .split(",")[0]
          .trim();

        console.log("🎯 Chatbot identified target:", targetNode);

        if (targetNode && targetNode !== "None" && onFocusNode) {
          onFocusNode({ id: targetNode, timestamp: Date.now() });
        }
      }
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "system", text: "Error connecting to Neural Core." },
      ]);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col w-full h-full bg-gray-900/90 backdrop-blur-md border-2 border-cyan-500 rounded-2xl shadow-2xl overflow-hidden">
      <div className="p-4 border-b border-white/10 bg-black/40">
        <h2 className="text-cyan-400 font-mono font-bold">INSIDER_AI</h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 rounded ${
              msg.role === "system" ? "text-white" : "text-cyan-300 text-right"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {/* 3. Invisible element at the bottom to scroll to */}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 bg-black/40">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          placeholder="Ask about the graph..."
          className="w-full bg-gray-800 text-white p-3 rounded border border-gray-600 focus:border-cyan-400 outline-none"
        />
      </div>
    </div>
  );
}
