import React from 'react';
import ReactFlow, { Background, Handle, Position } from 'reactflow';
import 'reactflow/dist/style.css';

const CustomNode = ({ data, selected }) => {
  return (
    <div className={`w-48 p-brand-md rounded-xl glass-card border flex flex-col items-center text-center transition-all duration-300 ${data.borderColor}`}>
      <div className={`w-12 h-12 rounded-lg ${data.bgColor} flex items-center justify-center ${data.iconColor} mb-brand-md shadow-sm`}>
        <span className="material-symbols-outlined">{data.icon}</span>
      </div>
      <span className={`font-label-md text-label-md ${data.labelColor} uppercase tracking-widest mb-brand-xs font-bold`}>{data.type}</span>
      <h4 className="font-headline-md text-[18px] text-on-surface leading-tight font-semibold">{data.title}</h4>
      
      <Handle type="target" position={Position.Left} style={{ visibility: 'hidden' }} />
      <Handle type="source" position={Position.Right} style={{ visibility: 'hidden' }} />
    </div>
  );
};

const nodeTypes = {
  scientific: CustomNode,
};

const initialNodes = [
  {
    id: '1',
    type: 'scientific',
    data: { 
      icon: 'camera', 
      type: 'Input', 
      title: 'Image/Video',
      bgColor: 'bg-primary-container',
      iconColor: 'text-on-primary-container',
      borderColor: 'border-primary/20',
      labelColor: 'text-primary'
    },
    position: { x: 0, y: 0 },
  },
  {
    id: '2',
    type: 'scientific',
    data: { 
      icon: 'memory', 
      type: 'AI', 
      title: 'Preprocessing',
      bgColor: 'bg-secondary-container',
      iconColor: 'text-on-secondary-container',
      borderColor: 'border-secondary/20',
      labelColor: 'text-secondary'
    },
    position: { x: 300, y: 0 },
  },
  {
    id: '3',
    type: 'scientific',
    data: { 
      icon: 'urology', 
      type: 'Taxonomic', 
      title: 'Analysis',
      bgColor: 'bg-tertiary-container',
      iconColor: 'text-on-tertiary-container',
      borderColor: 'border-tertiary/20',
      labelColor: 'text-tertiary'
    },
    position: { x: 600, y: 0 },
  },
  {
    id: '4',
    type: 'scientific',
    data: { 
      icon: 'check_circle', 
      type: 'Result', 
      title: 'Species Result',
      bgColor: 'bg-primary',
      iconColor: 'text-on-primary',
      borderColor: 'border-primary/40',
      labelColor: 'text-primary'
    },
    position: { x: 900, y: 0 },
  },
];

const initialEdges = [
  { 
    id: 'e1-2', source: '1', target: '2', animated: true, 
    style: { stroke: '#dec0b6', strokeWidth: 2 } 
  },
  { 
    id: 'e2-3', source: '2', target: '3', animated: true,
    style: { stroke: '#dec0b6', strokeWidth: 2 }
  },
  { 
    id: 'e3-4', source: '3', target: '4', animated: true,
    style: { stroke: '#a43c12', strokeWidth: 2, opacity: 0.5 }
  },
];

const ArchitectureFlow = () => {
  return (
    <div className="w-full h-full relative pointer-events-none">
      <ReactFlow
        nodes={initialNodes}
        edges={initialEdges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        zoomOnScroll={false}
        zoomOnPinch={false}
        zoomOnDoubleClick={false}
        panOnDrag={false}
        panOnScroll={false}
        selectionKeyCode={null}
        multiSelectionKeyCode={null}
        preventScrolling={false}
        attributionPosition="bottom-right"
      >
      </ReactFlow>
    </div>
  );
};

export default ArchitectureFlow;
