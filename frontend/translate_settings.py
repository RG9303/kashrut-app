import os
with open('src/app/settings/page.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { useState, useEffect } from 'react';", "import { useState, useEffect } from 'react';\nimport { useLanguage } from '@/hooks/useLanguage';")

new_hook_code = """
export default function SettingsPage() {
  const { lang } = useLanguage();
  const TEXTS = {
    esp: {
      back: "Volver",
      prefs: "Preferencias",
      account: "Cuenta de Usuario",
      name: "Nombre",
      namePlace: "Tu nombre completo",
      email: "Correo Electrónico",
      emailPlace: "correo@ejemplo.com",
      origin: "Kashrut y Origen",
      custom: "Costumbre",
      ashk: "Ashkenazí",
      sef: "Sefaradí",
      country: "País de Residencia",
      mexico: "México",
      usa: "Estados Unidos",
      arg: "Argentina",
      isr: "Israel",
      spa: "España",
      other: "Otro País",
      interests: "Intereses y Módulos",
      interestsDesc: "Activa estas opciones para personalizar tu experiencia y prepararnos para futuras actualizaciones.",
      guide: "Guía de Chaguim",
      guideDesc: "Alertas y preparación para Festividades",
      recipes: "Recetas Kosher",
      recipesDesc: "Sugerencias basadas en tus costumbres",
      saved: "¡Preferencias Guardadas!",
      save: "Guardar Configuración"
    },
    eng: {
      back: "Back",
      prefs: "Preferences",
      account: "User Account",
      name: "Name",
      namePlace: "Your full name",
      email: "Email Address",
      emailPlace: "email@example.com",
      origin: "Kashrut and Origin",
      custom: "Custom",
      ashk: "Ashkenazi",
      sef: "Sephardic",
      country: "Country of Residence",
      mexico: "Mexico",
      usa: "United States",
      arg: "Argentina",
      isr: "Israel",
      spa: "Spain",
      other: "Other Country",
      interests: "Interests and Modules",
      interestsDesc: "Activate these options to customize your experience and prepare for future updates.",
      guide: "Chaguim Guide",
      guideDesc: "Alerts and preparation for Holidays",
      recipes: "Kosher Recipes",
      recipesDesc: "Suggestions based on your customs",
      saved: "Preferences Saved!",
      save: "Save Configuration"
    }
  };
  const t = TEXTS[lang as keyof typeof TEXTS] || TEXTS['esp'];
"""

content = content.replace("export default function SettingsPage() {", new_hook_code)

reps = {
    "> Volver": "> {t.back}",
    ">Preferencias<": ">{t.prefs}<",
    ">Cuenta de Usuario<": ">{t.account}<",
    ">Nombre<": ">{t.name}<",
    'placeholder="Tu nombre completo"': 'placeholder={t.namePlace}',
    ">Correo Electrónico<": ">{t.email}<",
    'placeholder="correo@ejemplo.com"': 'placeholder={t.emailPlace}',
    ">Kashrut y Origen<": ">{t.origin}<",
    ">Costumbre<": ">{t.custom}<",
    ">Ashkenazí<": ">{t.ashk}<",
    ">Sefaradí<": ">{t.sef}<",
    ">País de Residencia<": ">{t.country}<",
    ">México<": ">{t.mexico}<",
    ">Estados Unidos<": ">{t.usa}<",
    ">Argentina<": ">{t.arg}<",
    ">Israel<": ">{t.isr}<",
    ">España<": ">{t.spa}<",
    ">Otro País<": ">{t.other}<",
    ">Intereses y Módulos<": ">{t.interests}<",
    "Activa estas opciones para personalizar tu experiencia y prepararnos para futuras actualizaciones.": "{t.interestsDesc}",
    ">Guía de Chaguim<": ">{t.guide}<",
    ">Alertas y preparación para Festividades<": ">{t.guideDesc}<",
    ">Recetas Kosher<": ">{t.recipes}<",
    ">Sugerencias basadas en tus costumbres<": ">{t.recipesDesc}<",
    "¡Preferencias Guardadas!": "{t.saved}",
    "Guardar Configuración": "{t.save}"
}
for k,v in reps.items():
    content = content.replace(k,v)

with open('src/app/settings/page.tsx', 'w') as f:
    f.write(content)

print("Settings translated.")
