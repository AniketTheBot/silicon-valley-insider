import { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function CursorGlow() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const updateMousePosition = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener("mousemove", updateMousePosition);
    return () => window.removeEventListener("mousemove", updateMousePosition);
  }, []);

  return (
    <>
      {/* Ambient Glow - Large and subtle */}
      <motion.div
        className="pointer-events-none fixed inset-0 z-10" // z-10 matches App.jsx
        animate={{
          background: `radial-gradient(600px at ${mousePosition.x}px ${mousePosition.y}px, rgba(0, 243, 255, 0.15), transparent 80%)`,
        }}
      />

      {/* The Dot - Small and Sharp - HIGHEST Z-INDEX */}
      <motion.div
        className="pointer-events-none fixed top-0 left-0 z-[100] h-4 w-4 rounded-full bg-cyan-400 mix-blend-screen shadow-[0_0_10px_#00f3ff]"
        animate={{
          x: mousePosition.x - 8,
          y: mousePosition.y - 8,
        }}
        transition={{ type: "spring", stiffness: 500, damping: 28 }}
      />
    </>
  );
}
