import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, CheckCircle, AlertCircle, X, ChevronRight, UploadCloud } from 'lucide-react';
import { cn } from '../lib/utils';

const API_BASE_URL = 'http://localhost:8000';

const ClassificationForm = ({ onComplete }) => {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const processFile = (selectedFile) => {
    if (selectedFile) {
      setFile(selectedFile);
      setResult(null);
      setError(null);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result);
      reader.readAsDataURL(selectedFile);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post(`${API_BASE_URL}/predict`, formData);
      const data = response.data;
      setResult(data);
      if (onComplete) {
        onComplete({
          ...data,
          image: preview,
          timestamp: new Date().toISOString()
        });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis engine unreachable.');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="w-full relative group">
      <AnimatePresence mode="wait">
        {!result && !error ? (
          <motion.div 
            key="upload"
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 1.02 }}
            className="relative"
          >
            <div 
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={(e) => { e.preventDefault(); setIsDragging(false); processFile(e.dataTransfer.files[0]); }}
              className={cn(
                "relative aspect-[4/5] md:aspect-square scientific-card overflow-hidden flex flex-col items-center justify-center p-brand-xl cursor-pointer group max-w-md mx-auto lg:ml-auto lg:mr-0",
                isDragging && "border-brand-accent bg-brand-accent/5",
                preview ? "border-transparent shadow-2xl" : "bg-white"
              )}
            >
              {/* Technical Grid Background */}
              {!preview && (
                <div className="absolute inset-0 opacity-[0.03] pointer-events-none" 
                  style={{ backgroundImage: 'linear-gradient(#000 1px, transparent 1px), linear-gradient(90deg, #000 1px, transparent 1px)', backgroundSize: '20px 20px' }} 
                />
              )}
              {preview ? (
                <div className="absolute inset-0">
                  <img src={preview} alt="Preview" className="w-full h-full object-cover" />
                  {loading && <div className="scan-line" />}
                  <div className="absolute inset-0 bg-brand-deep/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <button aria-label="Clear image" onClick={(e) => { e.stopPropagation(); reset(); }} className="bg-white/90 backdrop-blur p-brand-md rounded-full text-brand-deep hover:bg-white transition-all">
                      <X size={20} />
                    </button>
                  </div>
                </div>
              ) : (
                <div className="text-center space-y-brand-lg">
                  <div className="w-24 h-24 mx-auto bg-brand-sand rounded-full flex items-center justify-center text-brand-accent transition-transform duration-700 group-hover:scale-110 group-hover:rotate-12">
                    <UploadCloud size={32} strokeWidth={1.5} />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2">Ingest Specimen</h3>
                    <p className="text-sm text-brand-deep/60 px-brand-lg max-w-xs mx-auto">
                      Drag macro visual data or click to initialize scientific classification.
                    </p>
                  </div>
                </div>
              )}
              <input aria-label="Upload coral image" type="file" className="absolute inset-0 opacity-0 cursor-pointer z-20" onChange={(e) => processFile(e.target.files?.[0])} accept="image/*" />
              
              {/* Technical Overlay */}
              <div className="absolute top-0 left-0 w-full p-brand-md flex justify-between pointer-events-none opacity-40">
                <div className="font-mono text-[10px] uppercase tracking-tighter">Lat: 18.2341 / Long: -66.5213</div>
                <div className="font-mono text-[10px] uppercase tracking-tighter">Mode: CV_INFERENCE_V4</div>
              </div>
            </div>

            {file && (
              <motion.button 
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={handleSubmit}
                disabled={loading}
                className="w-full mt-brand-lg bg-brand-deep text-brand-sand font-mono text-sm tracking-widest py-brand-lg uppercase font-bold hover:bg-brand-accent transition-all flex items-center justify-center gap-3 overflow-hidden group/btn"
              >
                {loading ? <Loader2 className="animate-spin" size={18} /> : <div className="w-2 h-2 bg-brand-accent rounded-full group-hover/btn:scale-150 transition-transform" />}
                {loading ? 'Analyzing Neural Patterns...' : 'Commence Analysis'}
              </motion.button>
            )}
          </motion.div>
        ) : result ? (
          <motion.div 
            key="result"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="scientific-card bg-white p-brand-xl space-y-brand-xl shadow-2xl relative overflow-hidden"
          >
            {/* Background Texture */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-brand-teal/5 rounded-full blur-3xl -mr-16 -mt-16" />
            
            <div className="flex justify-between items-start relative z-10">
              <div className="px-brand-lg py-1 border border-brand-teal/30 text-brand-teal font-mono text-[10px] uppercase tracking-[0.2em] font-bold rounded-full">
                Taxon Identified
              </div>
              <button aria-label="Reset analysis" onClick={reset} className="text-brand-deep/40 hover:text-brand-accent transition-colors">
                <X size={20} />
              </button>
            </div>

            <div className="space-y-sm text-left relative z-10">
              <h3 className="text-5xl font-bold tracking-tighter capitalize leading-none text-brand-deep">
                {result.prediction}
              </h3>
              <p className="font-mono text-[10px] text-brand-accent uppercase tracking-widest">Scientific Classification Protocol Complete</p>
            </div>

            <div className="grid grid-cols-2 gap-brand-xl relative z-10">
              <div className="space-y-sm">
                <p className="font-mono text-[10px] text-brand-deep/40 uppercase tracking-widest">Confidence</p>
                <div className="flex items-end gap-1">
                  <span className="text-3xl font-bold text-brand-deep">{(result.confidence * 100).toFixed(1)}</span>
                  <span className="text-lg text-brand-deep/40 mb-1">%</span>
                </div>
              </div>
              <div className="space-y-sm">
                <p className="font-mono text-[10px] text-brand-deep/40 uppercase tracking-widest">Engine Status</p>
                <div className="flex items-center gap-2 text-brand-teal">
                  <CheckCircle size={18} />
                  <span className="font-mono text-xs font-bold">OPTIMAL</span>
                </div>
              </div>
            </div>

            <div className="space-y-md border-t border-brand-sand pt-brand-xl relative z-10">
              <p className="font-mono text-[10px] text-brand-deep/40 uppercase tracking-widest">Secondary Probabilities</p>
              <div className="space-y-3">
                {Object.entries(result.all_scores || {})
                  .sort((a, b) => b[1] - a[1])
                  .slice(1, 3)
                  .map(([name, score]) => (
                    <div key={name} className="group">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="capitalize opacity-60">{name}</span>
                        <span className="font-mono text-[10px] opacity-40">{(score * 100).toFixed(0)}%</span>
                      </div>
                      <div className="h-[1px] w-full bg-brand-sand overflow-hidden">
                        <div className="h-full bg-brand-deep/10 w-full scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-700" style={{ width: `${score * 100}%` }} />
                      </div>
                    </div>
                  ))
                }
              </div>
            </div>

            <button className="w-full py-brand-lg bg-brand-sand text-brand-deep font-mono text-[10px] uppercase tracking-widest font-bold hover:bg-brand-deep hover:text-white transition-all flex items-center justify-center gap-sm">
              Generate Detailed Datasheet <ChevronRight size={14} />
            </button>
          </motion.div>
        ) : (
          <motion.div 
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="scientific-card bg-white p-brand-xl text-center space-y-brand-xl"
          >
            <div className="w-20 h-20 bg-brand-accent/10 text-brand-accent rounded-full flex items-center justify-center mx-auto">
              <AlertCircle size={32} />
            </div>
            <div className="space-y-sm">
              <h3 className="text-xl font-bold">Analysis Terminated</h3>
              <p className="text-sm text-brand-deep/60 leading-relaxed max-w-xs mx-auto">{error}</p>
            </div>
            <button onClick={reset} className="w-full py-brand-lg bg-brand-deep text-brand-sand font-mono text-xs uppercase tracking-widest font-bold hover:bg-brand-accent transition-all">Reinitialize</button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default ClassificationForm;
