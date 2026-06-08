import React, { useState, useEffect } from 'react';
import ClassificationForm from './components/ClassificationForm';
import ArchitectureFlow from './components/ArchitectureFlow';
import { motion, AnimatePresence } from 'framer-motion';
import { History, Trash2, Clock, MapPin, Database } from 'lucide-react';
import specimenImage from './assets/istockphoto-1333419569-612x612.jpg';

export default function App() {
  const [archives, setArchives] = useState([]);

  // Load archives on mount
  useEffect(() => {
    const saved = localStorage.getItem('coral-archives');
    if (saved) {
      try {
        setArchives(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to load archives', e);
      }
    }
  }, []);

  const addToArchives = (entry) => {
    setArchives(prev => {
      const updated = [entry, ...prev].slice(0, 20); // Keep last 20
      localStorage.setItem('coral-archives', JSON.stringify(updated));
      return updated;
    });
  };

  const clearArchives = () => {
    if (window.confirm('Initialize archive purge? This action is irreversible.')) {
      setArchives([]);
      localStorage.removeItem('coral-archives');
    }
  };

  return (
    <div className="min-h-screen flex flex-col selection:bg-brand-accent selection:text-white">
      {/* Editorial Header */}
      <header className="w-full top-0 sticky z-50 nav-blur border-b border-brand-deep/5">
        <nav className="flex justify-between items-center px-brand-margin-mobile md:px-brand-margin-desktop py-brand-lg w-full max-w-screen-2xl mx-auto">
          <div className="flex items-center gap-12">
            <span className="text-2xl font-bold tracking-tighter uppercase text-brand-deep flex items-center gap-2">
              <div className="w-2 h-2 bg-brand-accent rounded-full animate-pulse" />
              CoralID
            </span>
            <div className="hidden md:flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-brand-deep/40">
              <a className="text-brand-deep font-bold border-b border-brand-accent px-4 py-3" href="#">Laboratory</a>
              <a className="hover:text-brand-accent transition-colors px-4 py-3" href="#">Taxon_Registry</a>
              <a className="hover:text-brand-accent transition-colors px-4 py-3" href="#">Documentation</a>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden sm:block text-right">
              <div className="font-mono text-[9px] uppercase tracking-tighter text-brand-deep/30">System_Status</div>
              <div className="font-mono text-[10px] uppercase font-bold text-brand-teal">Lvl_4_Operational</div>
            </div>
            <button aria-label="User Profile" className="w-11 h-11 rounded-full border border-brand-deep/10 flex items-center justify-center hover:bg-brand-deep hover:text-white transition-all">
              <span className="material-symbols-outlined text-lg">fingerprint</span>
            </button>
          </div>
        </nav>
      </header>

      <main className="flex-grow">
        {/* Asymmetric Hero */}
        <section className="relative pt-24 pb-32 px-brand-margin-mobile md:px-brand-margin-desktop max-w-screen-2xl mx-auto">
          <div className="editorial-grid">
            <div className="col-span-12 lg:col-span-7 space-y-12">
              <div className="inline-flex items-center gap-4 px-4 py-2 bg-brand-deep text-brand-sand rounded-full">
                <div className="w-1.5 h-1.5 bg-brand-teal rounded-full animate-ping" />
                <span className="font-mono text-[9px] uppercase tracking-[0.3em] font-bold">V.4 Inference Engine Active</span>
              </div>
              
              <div className="space-y-6">
                <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold tracking-tighter leading-[1.05] text-brand-deep">
                  Autonomous <br className="hidden md:block" />
                  <span className="text-brand-accent italic">Taxonomy</span>
                </h1>
                <p className="text-lg md:text-xl text-brand-deep/70 max-w-xl leading-relaxed font-light">
                  Bridging marine biology and computer vision. Our neural architecture identifies reef specimens with scientific precision in milliseconds.
                </p>
              </div>

              <div className="flex flex-wrap gap-8 pt-6">
                <div className="space-y-2">
                  <div className="font-mono text-[10px] uppercase tracking-widest text-brand-deep/40">Dataset_Volume</div>
                  <div className="text-3xl font-bold text-brand-deep">500K+</div>
                  <div className="text-[10px] uppercase tracking-tighter opacity-40">Verified Samples</div>
                </div>
                <div className="w-px h-16 bg-brand-deep/10 hidden sm:block" />
                <div className="space-y-2">
                  <div className="font-mono text-[10px] uppercase tracking-widest text-brand-deep/40">Precision_Rate</div>
                  <div className="text-3xl font-bold text-brand-deep">98.4%</div>
                  <div className="text-[10px] uppercase tracking-tighter opacity-40">Taxonomic Accuracy</div>
                </div>
              </div>
            </div>

            <div className="col-span-12 lg:col-span-5 relative mt-12 lg:mt-0">
              <ClassificationForm onComplete={addToArchives} />
              {/* Decorative Tech Specs */}
              <div className="absolute -bottom-12 -right-12 hidden xl:block opacity-10 font-mono text-[10px] leading-relaxed">
                ANALYSIS_PROTO_V4 <br />
                LAYER_NORM: TRUE <br />
                ACTIVATION: SWISH <br />
                DROPOUT: 0.2 <br />
                BATCH_SIZE: 32
              </div>
            </div>
          </div>
        </section>

        {/* Technical Flow - Full Width Inset */}
        <section className="bg-brand-deep py-32 overflow-hidden">
          <div className="max-w-screen-2xl mx-auto px-brand-margin-mobile md:px-brand-margin-desktop">
            <div className="editorial-grid items-end mb-24">
              <div className="col-span-12 lg:col-span-6">
                <h2 className="text-3xl md:text-5xl lg:text-6xl font-bold text-brand-sand tracking-tighter leading-[1.1] mb-8">
                  The Multi-Stage <br className="hidden md:block" />
                  <span className="opacity-40">Validation Pipeline</span>
                </h2>
              </div>
              <div className="col-span-12 lg:col-span-6 lg:pb-2">
                <p className="text-brand-sand/60 max-w-md font-light">
                  Raw visual telemetry is processed through a sequence of normalization, feature extraction, and probabilistic matching before final taxonomic assignment.
                </p>
              </div>
            </div>
            
            <div className="relative h-[500px] w-full scientific-card bg-white border-white/10 overflow-hidden">
              <ArchitectureFlow />
            </div>
          </div>
        </section>

        {/* Feature Editorial */}
        <section className="py-32 px-brand-margin-mobile md:px-brand-margin-desktop max-w-screen-2xl mx-auto">
          <div className="editorial-grid">
            <div className="col-span-12 md:col-span-8 relative group">
              <div className="aspect-[16/9] overflow-hidden scientific-card border-none">
                <img 
                  className="w-full h-full object-cover transition-all duration-1000 group-hover:scale-105" 
                  src={specimenImage} 
                  alt="Zoanthus genus specimen in a colorful small colony"
                />
              </div>
              <div className="mt-8 flex justify-between items-start">
                <div>
                  <h3 className="text-2xl font-bold text-brand-deep mb-2">Global Reef Repository</h3>
                  <p className="text-brand-deep/60 max-w-sm text-sm">Our unified database synchronizes global taxonomic data for real-time reef health monitoring.</p>
                </div>
                <div className="font-mono text-[9px] uppercase tracking-widest text-brand-accent font-bold px-3 py-1 border border-brand-accent/20 rounded">
                  Live_Data_Stream
                </div>
              </div>
            </div>
            <div className="col-span-12 md:col-span-4 space-y-12 flex flex-col justify-center">
              <div className="space-y-6">
                <div className="w-12 h-12 border border-brand-deep/10 rounded-full flex items-center justify-center text-brand-accent">
                  <span className="material-symbols-outlined">analytics</span>
                </div>
                <h3 className="text-3xl font-bold leading-tight">Empirical <br />Consistency</h3>
                <p className="text-brand-deep/70 text-sm leading-relaxed">
                  Every identification is cross-referenced with a multi-modal training set of 500k+ scientifically verified samples, ensuring enterprise-grade taxonomic integrity.
                </p>
                <a className="inline-flex items-center gap-4 text-brand-deep font-mono text-[10px] uppercase tracking-widest font-bold group px-4 py-3 -ml-4" href="#">
                  Technical_Whitepaper
                  <div className="w-8 h-[1px] bg-brand-accent group-hover:w-12 transition-all" />
                </a>
              </div>
            </div>
          </div>
        </section>
        {/* Archives Section */}
        <section className="py-32 px-brand-margin-mobile md:px-brand-margin-desktop max-w-screen-2xl mx-auto border-t border-brand-deep/5">
          <div className="editorial-grid items-start mb-16">
            <div className="col-span-12 md:col-span-6 space-y-4">
              <div className="flex items-center gap-3 text-brand-accent">
                <History size={20} />
                <h2 className="text-3xl md:text-5xl font-bold tracking-tighter">Research Archives</h2>
              </div>
              <p className="text-brand-deep/60 max-w-md">Chronological log of taxonomic classifications and visual telemetry data.</p>
            </div>
            <div className="col-span-12 md:col-span-6 flex md:justify-end items-center">
              {archives.length > 0 && (
                <button 
                  onClick={clearArchives}
                  className="flex items-center gap-2 font-mono text-[9px] uppercase tracking-widest text-brand-deep/40 hover:text-error transition-colors px-4 py-2 border border-brand-deep/10 rounded-full"
                >
                  <Trash2 size={12} /> Purge_History
                </button>
              )}
            </div>
          </div>

          {archives.length > 0 ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-brand-lg">
              <AnimatePresence>
                {archives.map((entry, i) => (
                  <motion.div
                    key={entry.timestamp}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ delay: i * 0.05 }}
                    className="scientific-card bg-white overflow-hidden group hover:border-brand-accent/40"
                  >
                    <div className="aspect-square relative overflow-hidden bg-brand-sand">
                      <img src={entry.image} alt={entry.prediction} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
                      <div className="absolute top-2 right-2 px-2 py-1 bg-brand-deep/80 backdrop-blur text-brand-sand font-mono text-[8px] uppercase tracking-tighter rounded">
                        {(entry.confidence * 100).toFixed(0)}%
                      </div>
                    </div>
                    <div className="p-4 space-y-3">
                      <div>
                        <h4 className="font-bold text-brand-deep capitalize truncate">{entry.prediction}</h4>
                        <div className="flex items-center gap-2 text-brand-deep/40 font-mono text-[8px] uppercase tracking-widest mt-1">
                          <Clock size={10} />
                          {new Date(entry.timestamp).toLocaleDateString()}
                        </div>
                      </div>
                      <div className="pt-3 border-t border-brand-sand flex justify-between items-center">
                        <div className="flex items-center gap-1 text-[8px] font-mono text-brand-teal font-bold uppercase">
                          <Database size={8} /> Verified
                        </div>
                        <div className="flex items-center gap-1 text-[8px] font-mono text-brand-deep/30 uppercase">
                          <MapPin size={8} /> Sector_7
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          ) : (
            <div className="w-full py-24 border border-dashed border-brand-deep/10 rounded-xl flex flex-col items-center justify-center text-center space-y-4">
              <div className="w-12 h-12 bg-brand-sand rounded-full flex items-center justify-center text-brand-deep/20">
                <Database size={24} strokeWidth={1} />
              </div>
              <div className="space-y-1">
                <h4 className="font-mono text-[10px] uppercase tracking-[0.2em] font-bold text-brand-deep/40">Archive_Empty</h4>
                <p className="text-xs text-brand-deep/30">Initialize specimen analysis to populate research logs.</p>
              </div>
            </div>
          )}
        </section>

      </main>

      {/* Minimal Footer */}
      <footer className="bg-brand-sand py-24 border-t border-brand-deep/5">
        <div className="max-w-screen-2xl mx-auto px-brand-margin-mobile md:px-brand-margin-desktop flex flex-col md:flex-row justify-between items-end gap-12">
          <div className="space-y-8 w-full md:w-auto">
            <span className="text-4xl font-bold tracking-tighter text-brand-deep uppercase block text-center md:text-left">CoralID</span>
            <div className="flex flex-wrap justify-center md:justify-start gap-4 font-mono text-[9px] uppercase tracking-widest text-brand-deep/40">
              <a href="#" className="hover:text-brand-accent transition-colors px-3 py-3">Privacy_Protocol</a>
              <a href="#" className="hover:text-brand-accent transition-colors px-3 py-3">Usage_Terms</a>
              <a href="#" className="hover:text-brand-accent transition-colors px-3 py-3">Attribution_Registry</a>
            </div>
          </div>
          <div className="text-right space-y-4">
            <div className="font-mono text-[9px] uppercase tracking-tighter text-brand-deep/30">© 2024 Marine_Taxonomy_System</div>
            <div className="text-[10px] text-brand-deep/40 max-w-xs ml-auto">
              Hardware-accelerated computer vision platform for biological research and reef conservation.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
