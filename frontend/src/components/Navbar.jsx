/**
 * WasteSegregator AI — Enterprise Responsive Navigation Bar
 * Symmetrical 3-zone architecture with equal spacing at both ends
 * and perfectly centered desktop navigation links.
 */
import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  ScanLine,
  History,
  Info,
  Sliders,
  Sparkles,
  Cpu,
  Recycle,
  Menu,
  X
} from 'lucide-react';
import { checkHealth } from '../services/api';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [health, setHealth] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    checkHealth()
      .then(setHealth)
      .catch(() => setHealth(null));
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  const navItems = [
    { to: '/', label: 'Home', icon: Sparkles, exact: true },
    { to: '/detect', label: 'Scanner', icon: ScanLine },
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/history', label: 'History', icon: History },
    { to: '/training', label: 'Benchmarks', icon: Cpu },
    { to: '/settings', label: 'Settings', icon: Sliders },
    { to: '/about', label: 'About', icon: Info },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-2xs">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-[1fr_auto_1fr] items-center h-[60px] w-full">
          {/* Left Zone: Brand Logo & Title (Flushed left, identical width to Right Zone) */}
          <div className="flex items-center justify-start min-w-0">
            <div
              onClick={() => navigate('/')}
              className="flex items-center gap-2 sm:gap-2.5 cursor-pointer select-none group flex-shrink-0"
            >
              <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-emerald-500 flex items-center justify-center text-white shadow-xs group-hover:scale-105 transition-transform duration-150 flex-shrink-0">
                <Recycle className="w-4 h-4 sm:w-5 sm:h-5 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="font-extrabold text-slate-900 text-sm sm:text-[15px] tracking-tight leading-none group-hover:text-blue-600 transition-colors whitespace-nowrap">
                  WasteSegregator <span className="text-blue-600 font-extrabold">AI</span>
                </span>
                <span className="text-[10px] text-slate-400 font-medium tracking-wide mt-0.5 hidden 2xl:block">
                  Computer Vision & Municipal Sorting
                </span>
              </div>
            </div>
          </div>

          {/* Center Zone: Desktop Nav Links (dead-centered with equal space on both sides) */}
          <nav className="hidden lg:flex items-center justify-center gap-0.5 xl:gap-1 flex-shrink-0">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.exact}
                  className={({ isActive }) =>
                    `px-2 xl:px-2.5 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 whitespace-nowrap transition-all duration-150 border ${
                      isActive
                        ? 'bg-blue-50 text-blue-700 font-bold border-blue-200/80 shadow-2xs'
                        : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                    }`
                  }
                >
                  <Icon className="w-3.5 h-3.5 flex-shrink-0" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>

          {/* Right Zone: System Status & Action CTA (Flushed right, identical width to Left Zone) */}
          <div className="flex items-center justify-end gap-2 min-w-0">
            {/* Live API Status Badge */}
            <div
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-semibold border flex-shrink-0 ${
                health?.status === 'healthy'
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-rose-50 text-rose-700 border-rose-200'
              }`}
            >
              <span
                className={`w-1.5 h-1.5 rounded-full ${
                  health?.status === 'healthy' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'
                }`}
              />
              <span className="hidden sm:inline">
                {health?.status === 'healthy' ? 'API Online' : 'API Offline'}
              </span>
            </div>

            {/* Quick Action Button (Desktop CTA) */}
            <button
              onClick={() => navigate('/detect')}
              className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 active:scale-95 text-white rounded-lg text-xs font-bold shadow-xs transition-all whitespace-nowrap cursor-pointer flex-shrink-0"
            >
              <ScanLine className="w-3.5 h-3.5" />
              <span>Detect Waste</span>
            </button>

            {/* Mobile / Tablet Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200 transition-colors flex-shrink-0"
              aria-label="Toggle navigation menu"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile / Tablet Dropdown Menu */}
        {mobileMenuOpen && (
          <div className="lg:hidden border-t border-slate-200 py-2 space-y-1 animate-in fade-in slide-in-from-top-2 duration-150">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.exact}
                  className={({ isActive }) =>
                    `px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-2.5 transition-colors ${
                      isActive
                        ? 'bg-blue-50 text-blue-700 font-bold border border-blue-200/80'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`
                  }
                >
                  <Icon className="w-4 h-4 flex-shrink-0" />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </div>
        )}
      </div>
    </header>
  );
};

export default Navbar;
