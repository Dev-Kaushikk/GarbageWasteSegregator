/**
 * AutomataX-Styled Compact Top Navigation Bar
 * AI-Based Smart Garbage Waste Segregator
 */
import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard,
  ScanLine,
  History,
  BarChart3,
  Info,
  Sliders,
  Sparkles,
  Database,
  Cpu,
  Recycle
} from 'lucide-react';
import { checkHealth } from '../services/api';

const Navbar = () => {
  const navigate = useNavigate();
  const [health, setHealth] = useState(null);

  useEffect(() => {
    checkHealth()
      .then(setHealth)
      .catch(() => setHealth(null));
  }, []);

  const navItems = [
    { to: '/', label: 'Home', icon: Sparkles, exact: true },
    { to: '/detect', label: 'Waste Scanner', icon: ScanLine },
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/history', label: 'History', icon: History },
    { to: '/training', label: 'Model Benchmark', icon: Cpu },
    { to: '/settings', label: 'Engine Settings', icon: Sliders },
    { to: '/about', label: 'About', icon: Info },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-2xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-[60px]">
          {/* Brand Logo & Name */}
          <div
            onClick={() => navigate('/')}
            className="flex items-center gap-2.5 cursor-pointer select-none group flex-shrink-0"
          >
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-emerald-500 flex items-center justify-center text-white shadow-xs group-hover:scale-105 transition-all duration-150">
              <Recycle className="w-5 h-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-slate-800 text-[15px] tracking-tight leading-none group-hover:text-blue-600 transition-colors">
                WasteSegregator <span className="text-blue-600 font-bold">AI</span>
              </span>
              <span className="text-[10px] text-slate-400 font-medium tracking-wide mt-0.5">
                Computer Vision & Municipal Waste Sorting
              </span>
            </div>
          </div>

          {/* Nav Links */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.exact}
                  className={({ isActive }) =>
                    `px-2.5 sm:px-3 py-1.5 rounded-lg text-xs sm:text-[13px] font-semibold flex items-center gap-1.5 whitespace-nowrap transition-all duration-150 border ${
                      isActive
                        ? 'bg-blue-50 text-blue-700 font-bold border-blue-200/70 shadow-2xs'
                        : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
                    }`
                  }
                >
                  <Icon className="w-3.5 h-3.5 flex-shrink-0" />
                  <span className="whitespace-nowrap">{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Right Status Pill & CTA */}
          <div className="flex items-center gap-2.5 flex-shrink-0">
            {/* System Status Pill (Compact) */}
            <div
              className={`hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold border ${
                health?.status === 'healthy'
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-rose-50 text-rose-700 border-rose-200'
              }`}
            >
              {health?.status === 'healthy' ? (
                <>
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                  <span>API Online</span>
                </>
              ) : (
                <>
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
                  <span>API Offline</span>
                </>
              )}
            </div>

            {/* Quick Action Button (Compact) */}
            <button
              onClick={() => navigate('/detect')}
              className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white rounded-lg text-xs font-bold shadow-xs transition-all duration-150 flex items-center gap-1.5 whitespace-nowrap"
            >
              <ScanLine className="w-3.5 h-3.5 flex-shrink-0" />
              <span>Detect Waste</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
