with open('src/app/page.tsx', 'r') as f:
    content = f.read()

reps = {
    '<Camera className="w-5 h-5 text-emerald-500" /> Inicio (Escáner)': '<Camera className="w-5 h-5 text-emerald-500" /> {t.sidebarTitle}',
    '<span className="text-xl w-5 flex justify-center">🍷</span> Mega-Guía Chaguim': '<span className="text-xl w-5 flex justify-center">🍷</span> {t.megaGuide}',
    '<span className="text-xl w-5 flex justify-center">👨‍🍳</span> Recetario Kosher': '<span className="text-xl w-5 flex justify-center">👨‍🍳</span> {t.kosherRecipe}',
    '<span className="text-[10px] bg-slate-800 px-2 py-0.5 rounded-full ml-auto font-bold uppercase tracking-widest border border-slate-700">Pronto</span>': '<span className="text-[10px] bg-slate-800 px-2 py-0.5 rounded-full ml-auto font-bold uppercase tracking-widest border border-slate-700">{t.soon}</span>',
    '<span className="text-xl w-5 flex justify-center">📅</span> Calendario Hebreo': '<span className="text-xl w-5 flex justify-center">📅</span> {t.hebrewCalendar}',
    '<span className="text-xl w-5 flex justify-center">🔖</span> Catálogo de Logos': '<span className="text-xl w-5 flex justify-center">🔖</span> {t.logosCatalog}',
    '<span className="text-xl w-5 flex justify-center">🐛</span> Escáner de Insectos': '<span className="text-xl w-5 flex justify-center">🐛</span> {t.insectScanner}',
    '<ShieldAlert className="w-5 h-5 text-rose-500" /> Alertas de Kashrut': '<ShieldAlert className="w-5 h-5 text-rose-500" /> {t.kashrutAlerts}',
    '<p className="text-xs text-rose-400/80 leading-relaxed pr-2">Avisos urgentes sobre productos que perdieron certificación.</p>': '<p className="text-xs text-rose-400/80 leading-relaxed pr-2">{t.kashrutAlertsDesc}</p>',
    '<span className="text-[10px] bg-rose-500/20 text-rose-300 px-2.5 py-1 rounded-full w-fit mt-2 font-bold uppercase tracking-wider border border-rose-500/30">Próximamente</span>': '<span className="text-[10px] bg-rose-500/20 text-rose-300 px-2.5 py-1 rounded-full w-fit mt-2 font-bold uppercase tracking-wider border border-rose-500/30">{t.soon}</span>'
}

for k, v in reps.items():
    content = content.replace(k, v)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)

print("Sidebar texts replaced in page.tsx")
