import { useEffect, useState, useRef, useCallback } from "react";
import ForceGraph3D from "react-force-graph-3d";
import axios from "axios";

// 1. WE ADDED { focusNode } HERE so the component can receive the signal
export default function GraphView({ focusNode }) {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });

  const fetchGraphData = useCallback(async () => {
    try {
      const res = await axios.get("http://72.61.232.29:8000/graph");
      setGraphData({
         nodes: res.data.nodes.map(n => ({...n})),
         links: res.data.links.map(l => ({...l}))
      });
    } catch (error) {
      console.error("Failed to fetch graph:", error);
    }
  }, []);

  // 2. FETCH ONCE. REMOVED THE INTERVAL.
  // This stops the "Jitter" and lets you interact with the graph.
  useEffect(() => {
    fetchGraphData();
  }, [fetchGraphData]);

  // 3. CAMERA ZOOM LOGIC (Uncommented and Fixed)
    useEffect(() => {
    // Check if focusNode exists (it might be null at start)
    if (focusNode && fgRef.current) {
      
      // Handle both cases: Just a string (old way) or Object (new way)
      const targetId = typeof focusNode === 'object' ? focusNode.id : focusNode;

      // Find the actual node object in our data
      const node = graphData.nodes.find(n => n.id === targetId);
      
      if (node) {
        // Calculate a nice distance
        const distance = 40; 
        const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);

        // Smooth fly animation
        fgRef.current.cameraPosition(
          { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // New Position
          node, // Look at the Node
          3000  // Fly time in ms
        );
      }
    }
  }, [focusNode, graphData]);

  return (
    <div className="fixed inset-0 z-0">
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        nodeLabel="id"
        nodeAutoColorBy="group"
        
        // Visual Styling
        nodeOpacity={0.9}
        nodeResolution={16}
        
        // Lines
        linkWidth={1.5}
        linkColor={() => "#555"}
        
        // Particles (Traffic)
        linkDirectionalParticles={2}
        linkDirectionalParticleSpeed={0.005}
        linkDirectionalParticleWidth={2}
        linkDirectionalParticleColor={() => "#00f3ff"}
        
        backgroundColor="#000000"
        
        // Node Styling
        nodeThreeObjectExtend={true}
        nodeRelSize={6}
        
        // 4. CHANGED: Wait longer for physics to settle, but don't auto-zoom-out if we are focused
        cooldownTicks={100}
        onEngineStop={() => {
            // Only zoom to fit if we haven't focused on a specific node yet
            if (!focusNode) {
                fgRef.current.zoomToFit(400);
            }
        }}
      />
    </div>
  );
}