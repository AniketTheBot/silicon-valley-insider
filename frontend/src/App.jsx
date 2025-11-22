import { useState } from "react";
import GraphView from "./components/GraphView";
import ChatOverlay from "./components/ChatOverlay";
import CursorGlow from "./components/CursorGlow";
import "./App.css";

function App() {
  const [focusNode, setFocusNode] = useState(null);

  return (
    <main className="relative w-full h-screen bg-black overflow-hidden selection:bg-cyan-500/30">
      
      {/* Layer 0: Graph (Bottom) */}
      <div className="graph-layer">
        <GraphView focusNode={focusNode} />
      </div>

      {/* Layer 1: Title */}
      <div className="ui-layer pointer-events-none select-none">
        <h1 className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-600 tracking-tighter drop-shadow-[0_0_15px_rgba(6,182,212,0.5)]">
          SILICON<br/>VALLEY
        </h1>
        <div className="h-1 w-24 bg-cyan-500 mt-2 mb-2 shadow-[0_0_10px_#06b6d4]"></div>
        <h2 className="text-xl text-cyan-100/70 tracking-[0.4em] font-mono font-light">
          INSIDER KNOWLEDGE GRAPH
        </h2>
      </div>

      {/* Layer 2: Chatbox */}
      <div className="chat-layer">
        <ChatOverlay onFocusNode={setFocusNode} />
      </div>

      {/* Layer 3: Cursor (MOVED TO BOTTOM = RENDERS ON TOP) */}
      <div className="cursor-layer">
        <CursorGlow />
      </div>

    </main>
  );
}

export default App;