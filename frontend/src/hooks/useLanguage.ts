import { useState, useEffect } from 'react';

export function useLanguage() {
  const [lang, setLang] = useState<'esp' | 'eng'>('esp');

  useEffect(() => {
    const stored = localStorage.getItem('appLang') as 'esp' | 'eng';
    if (stored) setLang(stored);

    const handleStorageChange = () => {
      const current = localStorage.getItem('appLang') as 'esp' | 'eng';
      if (current) setLang(current);
    };

    window.addEventListener('languageChange', handleStorageChange);
    return () => window.removeEventListener('languageChange', handleStorageChange);
  }, []);

  return { lang };
}
