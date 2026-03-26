'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { User, Globe, Bell, CalendarHeart, ChefHat, Save, ArrowLeft, CheckCircle2 } from 'lucide-react';

export default function SettingsPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  
  // Shared preferences
  const [userOrigin, setUserOrigin] = useState('ashkenazi');
  const [userCountry, setUserCountry] = useState('México');
  
  // New features
  const [chaguimAlerts, setChaguimAlerts] = useState(false);
  const [kosherRecipes, setKosherRecipes] = useState(false);
  
  const [saved, setSaved] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    const storedName = localStorage.getItem('userName');
    const storedEmail = localStorage.getItem('userEmail');
    const storedOrigin = localStorage.getItem('userOrigin');
    const storedCountry = localStorage.getItem('userCountry');
    const storedChaguim = localStorage.getItem('chaguimAlerts');
    const storedRecipes = localStorage.getItem('kosherRecipes');

    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedName) setName(storedName);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedEmail) setEmail(storedEmail);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedOrigin) setUserOrigin(storedOrigin);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedCountry) setUserCountry(storedCountry);
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedChaguim) setChaguimAlerts(storedChaguim === 'true');
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (storedRecipes) setKosherRecipes(storedRecipes === 'true');
  }, []);

  const handleSave = () => {
    localStorage.setItem('userName', name);
    localStorage.setItem('userEmail', email);
    localStorage.setItem('userOrigin', userOrigin);
    localStorage.setItem('userCountry', userCountry);
    localStorage.setItem('chaguimAlerts', chaguimAlerts.toString());
    localStorage.setItem('kosherRecipes', kosherRecipes.toString());
    
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-4 lg:p-10 max-w-[800px] mx-auto relative">
      <header className="w-full flex justify-between items-center mb-8">
        <Link href="/" className="text-slate-400 hover:text-white transition flex items-center gap-2 font-medium">
          <ArrowLeft className="w-5 h-5" /> Volver
        </Link>
        <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
          Preferencias
        </h1>
        <div className="w-16"></div> {/* Spacer for alignment */}
      </header>

      <div className="w-full bg-slate-800/80 border border-slate-700/50 rounded-[2.5rem] p-6 lg:p-10 backdrop-blur-xl shadow-2xl flex flex-col gap-8">
        
        {/* Account Section */}
        <section>
          <div className="flex items-center gap-3 mb-4 text-emerald-400">
            <User className="w-6 h-6" />
            <h2 className="text-xl font-bold text-white tracking-tight">Cuenta de Usuario</h2>
          </div>
          <div className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-semibold text-slate-400">Nombre</label>
              <input 
                type="text" 
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Tu nombre completo"
                className="w-full bg-slate-900/80 border border-slate-700 text-white rounded-xl py-3 px-4 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-semibold text-slate-400">Correo Electrónico</label>
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="correo@ejemplo.com"
                className="w-full bg-slate-900/80 border border-slate-700 text-white rounded-xl py-3 px-4 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors"
              />
            </div>
          </div>
        </section>

        <div className="h-px w-full bg-slate-700/50"></div>

        {/* Kashrut Preferences */}
        <section>
          <div className="flex items-center gap-3 mb-4 text-emerald-400">
            <Globe className="w-6 h-6" />
            <h2 className="text-xl font-bold text-white tracking-tight">Kashrut y Origen</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-semibold text-slate-400">Costumbre</label>
              <select
                value={userOrigin}
                onChange={(e) => setUserOrigin(e.target.value)}
                className="w-full bg-slate-900/80 border border-slate-700 text-white rounded-xl py-3 px-4 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors appearance-none cursor-pointer"
              >
                <option value="ashkenazi" className="bg-slate-800">Ashkenazí</option>
                <option value="sefaradi" className="bg-slate-800">Sefaradí</option>
              </select>
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-sm font-semibold text-slate-400">País de Residencia</label>
              <select
                value={userCountry}
                onChange={(e) => setUserCountry(e.target.value)}
                className="w-full bg-slate-900/80 border border-slate-700 text-white rounded-xl py-3 px-4 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors appearance-none cursor-pointer"
              >
                <option value="México" className="bg-slate-800">México</option>
                <option value="Estados Unidos" className="bg-slate-800">Estados Unidos</option>
                <option value="Argentina" className="bg-slate-800">Argentina</option>
                <option value="Israel" className="bg-slate-800">Israel</option>
                <option value="España" className="bg-slate-800">España</option>
                <option value="Otro" className="bg-slate-800">Otro País</option>
              </select>
            </div>
          </div>
        </section>

        <div className="h-px w-full bg-slate-700/50"></div>

        {/* Modular Interests */}
        <section>
          <div className="flex items-center gap-3 mb-4 text-emerald-400">
            <Bell className="w-6 h-6" />
            <h2 className="text-xl font-bold text-white tracking-tight">Intereses y Módulos</h2>
          </div>
          <p className="text-sm text-slate-400 mb-5">
            Activa estas opciones para personalizar tu experiencia y prepararnos para futuras actualizaciones.
          </p>
          
          <div className="flex flex-col gap-3">
            <div 
              onClick={() => setChaguimAlerts(!chaguimAlerts)}
              className="flex items-center justify-between p-4 bg-slate-900/50 border border-slate-700/50 rounded-2xl cursor-pointer hover:bg-slate-800/50 transition">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
                  <CalendarHeart className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-white font-medium">Guía de Chaguim</div>
                  <div className="text-xs text-slate-400 mt-0.5">Alertas y preparación para Festividades</div>
                </div>
              </div>
              <div className={`w-12 h-6 rounded-full p-1 relative transition-colors duration-300 ${chaguimAlerts ? 'bg-emerald-500' : 'bg-slate-600'}`}>
                <div className={`w-4 h-4 rounded-full bg-white shadow-md transform transition-transform duration-300 ${chaguimAlerts ? 'translate-x-6' : 'translate-x-0'}`}></div>
              </div>
            </div>

            <div 
              onClick={() => setKosherRecipes(!kosherRecipes)}
              className="flex items-center justify-between p-4 bg-slate-900/50 border border-slate-700/50 rounded-2xl cursor-pointer hover:bg-slate-800/50 transition">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
                  <ChefHat className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-white font-medium">Recetas Kosher</div>
                  <div className="text-xs text-slate-400 mt-0.5">Sugerencias basadas en tus costumbres</div>
                </div>
              </div>
              <div className={`w-12 h-6 rounded-full p-1 relative transition-colors duration-300 ${kosherRecipes ? 'bg-emerald-500' : 'bg-slate-600'}`}>
                <div className={`w-4 h-4 rounded-full bg-white shadow-md transform transition-transform duration-300 ${kosherRecipes ? 'translate-x-6' : 'translate-x-0'}`}></div>
              </div>
            </div>
          </div>
        </section>

        {/* Save Button */}
        <div className="mt-4 pt-4 border-t border-slate-700/50">
          <button 
            onClick={handleSave}
            className={`w-full font-bold py-4 rounded-2xl transition-all active:scale-95 flex items-center justify-center gap-2 text-lg focus:outline-none shadow-lg ${
              saved 
                ? 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-[0_8px_25px_rgba(16,185,129,0.3)]' 
                : 'bg-gradient-to-r from-emerald-500 to-emerald-600 hover:brightness-110 text-white shadow-[0_8px_25px_rgba(16,185,129,0.3)]'
            }`}
          >
            {saved ? (
              <>
                <CheckCircle2 className="w-6 h-6" />
                ¡Preferencias Guardadas!
              </>
            ) : (
              <>
                <Save className="w-6 h-6" />
                Guardar Configuración
              </>
            )}
          </button>
        </div>

      </div>
    </main>
  );
}
