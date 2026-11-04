/**
 * AutomataX Layout Component
 * AI-Based Smart Garbage Waste Segregator
 */
import React from 'react';
import Navbar from './Navbar';
import { PLATFORM_INFO } from '../utils/constants';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans antialiased">
      {/* Top Navbar */}
      <Navbar />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-5 sm:py-6">
        {children}
      </main>

      {/* Academic Footer */}
      <footer className="bg-white border-t border-slate-200 py-5 mt-auto text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-slate-700 text-sm">WasteSegregator AI</span>
            <span>•</span>
            <span className="text-slate-500">Intelligent Computer Vision & Autonomous Segregation</span>
          </div>
          <div className="flex items-center gap-3 text-slate-400">
            <span>Model: <strong className="text-slate-700">YOLO11n (15-Class Flagship)</strong></span>
            <span>•</span>
            <span>Taxonomy: <strong className="text-emerald-700 font-semibold">15 Municipal Classes</strong></span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;

