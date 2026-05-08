'use client';
import { useState, useEffect } from 'react';

export default function GlobalLanguageToggle() {
  const [lang, setLang] = useState<'esp' | 'eng'>('esp');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem('appLang') as 'esp' | 'eng';
    if (stored) {
      setLang(stored);
    }
    
    const handleStorage = () => {
      const current = localStorage.getItem('appLang') as 'esp' | 'eng';
      if (current && current !== lang) {
        setLang(current);
      }
    };
    window.addEventListener('languageChange', handleStorage);
    return () => window.removeEventListener('languageChange', handleStorage);
  }, [lang]);

  const toggleLang = (newLang: 'esp' | 'eng') => {
    localStorage.setItem('appLang', newLang);
    setLang(newLang);
    window.dispatchEvent(new Event('languageChange'));
  };

  if (!mounted) return null;

  return (
    <div className="fixed top-4 right-4 z-[9999] flex bg-slate-800/80 backdrop-blur-md rounded-lg p-1 border border-slate-700/50 shadow-xl">
      <button 
        onClick={() => toggleLang('esp')}
        className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${lang === 'esp' ? 'bg-emerald-500 text-white shadow-md' : 'text-slate-400 hover:text-white'}`}
      >
        ESP
      </button>
      <button 
        onClick={() => toggleLang('eng')}
        className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${lang === 'eng' ? 'bg-emerald-500 text-white shadow-md' : 'text-slate-400 hover:text-white'}`}
      >
        ENG
      </button>
    </div>
  );
}
