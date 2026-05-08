import os

with open('src/app/logos/page.tsx', 'r') as f:
    content = f.read()

content = content.replace("import React, { useState } from 'react';", "import React, { useState } from 'react';\nimport { useLanguage } from '@/hooks/useLanguage';")

new_hook_code = """
export default function LogosPage() {
  const { lang } = useLanguage();
  const isEng = lang === 'eng';
  
  const TEXTS = {
    esp: {
      global: "Globales",
      israel: "Israelíes",
      local: "Locales",
      title: "Catálogo Enciclopédico",
      subtitle: "Diccionario Kashrut Global",
      searchPlaceholder: "Busca cualquier certificado...",
      searchHint: "Escribe cualquier letra (ej. OU, cRc) para abrir instantáneamente la enciclopedia oculta del sello.",
      results: "Resultados Enciclopédicos",
      studyDetails: "Estudiar Detalle",
      notFound: "No encontrado en Enciclopedia",
      notFoundDesc: "No tenemos este sello pre-programado. Utiliza la cámara principal en la pantalla de \\"Inicio\\" para que la Inteligencia Artificial analice visualmente el sello desconocido que tienes en tus manos.",
      backToScanner: "Volver al Escáner IA",
      globalSeals: "Sellos Globales",
      israelAgencies: "Agencias en Israel",
      localLatam: "Locales (Latinoamérica)",
      clickForEncyclopedia: "Clic para Enciclopedia",
      historyOfAgency: "Historia de la Agencia",
      halachicLevel: "Nivel Halájico (Strictness)",
      rabbinicAuth: "Autoridad Rabínica",
      mainRegion: "Región Principal",
      closeEncyclopedia: "Cerrar Enciclopedia"
    },
    eng: {
      global: "Global",
      israel: "Israeli",
      local: "Local",
      title: "Encyclopedic Catalog",
      subtitle: "Global Kashrut Dictionary",
      searchPlaceholder: "Search any certificate...",
      searchHint: "Type any letter (e.g. OU, cRc) to instantly open the hidden encyclopedia of the seal.",
      results: "Encyclopedic Results",
      studyDetails: "Study Detail",
      notFound: "Not Found in Encyclopedia",
      notFoundDesc: "We do not have this seal pre-programmed. Use the main camera on the \\"Home\\" screen for Artificial Intelligence to visually analyze the unknown seal you have in your hands.",
      backToScanner: "Back to AI Scanner",
      globalSeals: "Global Seals",
      israelAgencies: "Agencies in Israel",
      localLatam: "Local (Latin America)",
      clickForEncyclopedia: "Click for Encyclopedia",
      historyOfAgency: "Agency History",
      halachicLevel: "Halachic Level (Strictness)",
      rabbinicAuth: "Rabbinic Authority",
      mainRegion: "Main Region",
      closeEncyclopedia: "Close Encyclopedia"
    }
  };
  
  const t = TEXTS[isEng ? 'eng' : 'esp'];
"""

content = content.replace("export default function LogosPage() {", new_hook_code)

# Fix logos array categories if we want (it's hard to dynamically translate the object fields without rewriting).
# But we can at least translate the UI texts.
reps = {
    ">Catálogo Enciclopédico<": ">{t.title}<",
    "Diccionario Kashrut Global": "{t.subtitle}",
    'placeholder="Busca cualquier certificado..."': 'placeholder={t.searchPlaceholder}',
    "Escribe cualquier letra (ej. OU, cRc) para abrir instantáneamente la enciclopedia oculta del sello.": "{t.searchHint}",
    "Resultados Enciclopédicos (": "{t.results} (",
    ">Estudiar Detalle<": ">{t.studyDetails}<",
    ">No encontrado en Enciclopedia<": ">{t.notFound}<",
    "No tenemos este sello pre-programado. Utiliza la cámara principal en la pantalla de \"Inicio\" para que la Inteligencia Artificial analice visualmente el sello desconocido que tienes en tus manos.": "{t.notFoundDesc}",
    ">Volver al Escáner IA<": ">{t.backToScanner}<",
    "> Sellos Globales": "> {t.globalSeals}",
    "> Agencias en Israel": "> {t.israelAgencies}",
    "> Locales (Latinoamérica)": "> {t.localLatam}",
    "Clic para Enciclopedia": "{t.clickForEncyclopedia}",
    "Historia de la Agencia": "{t.historyOfAgency}",
    "Nivel Halájico (Strictness)": "{t.halachicLevel}",
    "Autoridad Rabínica": "{t.rabbinicAuth}",
    "Región Principal": "{t.mainRegion}",
    "Cerrar Enciclopedia": "{t.closeEncyclopedia}"
}

for k, v in reps.items():
    content = content.replace(k, v)

# Let's write it back
with open('src/app/logos/page.tsx', 'w') as f:
    f.write(content)

print("Logos UI translated.")
