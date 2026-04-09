export default function Privacidad() {
  return (
    <div className="min-h-screen text-slate-100 bg-[#0a1128] p-8 lg:p-20 font-sans">
      <div className="max-w-3xl mx-auto space-y-8 bg-slate-900/50 p-8 rounded-3xl border border-slate-800">
        <h1 className="text-3xl font-black text-emerald-400">Política de Privacidad</h1>
        
        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">1. Uso de la Cámara</h2>
          <p className="text-slate-300 leading-relaxed">
            La aplicación Ayin Lens requiere acceso a la cámara de su dispositivo exclusivamente para escanear y analizar en tiempo real la posible presencia de insectos o la validación de sellos Kosher. 
          </p>
          <p className="text-slate-300 leading-relaxed">
            Las imágenes capturadas son procesadas por nuestros servidores mediante Inteligencia Artificial (Gemini API) para devolverle un resultado automático. <strong>Nosotros no almacenamos, compartimos, ni vendemos ninguna de las fotografías, videos o rostros capturados por la cámara de los usuarios.</strong> Todo procesamiento fotográfico es de carácter efímero y se utiliza únicamente para el análisis instantáneo solicitado por el usuario.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">2. Datos Personales</h2>
          <p className="text-slate-300 leading-relaxed">
            No recopilamos información personal sensible como nombres reales, direcciones, correos electrónicos ni ubicaciones GPS en segundo plano. La app funciona respetando en su totalidad la confidencialidad de nuestros usuarios.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-xl font-bold text-white">3. Contacto</h2>
          <p className="text-slate-300 leading-relaxed">
            Si tiene alguna duda sobre nuestra política de privacidad o sobre el tratamiento de nuestra tecnología, por favor póngase en contacto a través de nuestros canales oficiales.
          </p>
        </section>
        
        <p className="text-sm text-slate-500 pt-10 border-t border-slate-800">
          Última actualización: Abril de 2026
        </p>
      </div>
    </div>
  );
}
