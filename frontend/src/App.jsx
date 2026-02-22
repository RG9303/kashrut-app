import React, {useState} from 'react'
import RearCameraCapture from './components/RearCameraCapture'

export default function App(){
  const [dataUrl, setDataUrl] = useState(null)
  const [result, setResult] = useState(null)

  const onCaptured = async (durl) => {
    setDataUrl(durl)
    // POST to API
    try{
      const blob = await (await fetch(durl)).blob()
      const fd = new FormData()
      fd.append('files', blob, 'capture.png')
      const res = await fetch('http://localhost:8000/analyze_insects', { method: 'POST', body: fd })
      const json = await res.json()
      setResult(json)
    }catch(e){
      console.error(e)
      alert('Error posting to API. Start backend on port 8000.')
    }
  }

  return (
    <div style={{padding:20}}>
      <h1>Kashrut Mobile Capture</h1>
      <p>Use the rear camera if available. If running locally, ensure FastAPI server is on <strong>http://localhost:8000</strong>.</p>
      <RearCameraCapture onCaptured={onCaptured} />

      {dataUrl && <div style={{marginTop:12}}>
        <h3>Captured</h3>
        <img src={dataUrl} style={{maxWidth:300}} />
      </div>}

      {result && <div style={{marginTop:12}}>
        <h3>API Result</h3>
        <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(result, null, 2)}</pre>
      </div>}
    </div>
  )
}
