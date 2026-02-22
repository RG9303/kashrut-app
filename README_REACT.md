React Frontend (quickstart)

This project contains a Python backend (Streamlit + engine) and a new FastAPI microservice at `api/app.py` that exposes endpoints for image analysis.

Goal: create a small React app that:
- accesses the device camera using the rear camera (if available) via `facingMode: { ideal: 'environment' }`
- captures an image and POSTs it to the FastAPI endpoint `/analyze_insects` or `/analyze_product`

Quick steps to create a React app and integrate camera capture:

1) Create React app (using Vite or CRA). Example using Vite:

```bash
# from repo root
npm create vite@latest frontend --template react
cd frontend
npm install
```

2) Example component to capture rear camera and POST image:

```jsx
// src/components/RearCameraCapture.jsx
import React, { useRef, useState, useEffect } from 'react'

export default function RearCameraCapture({ onCaptured }){
  const videoRef = useRef(null)
  const [stream, setStream] = useState(null)

  useEffect(() => {
    async function start() {
      try {
        const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } } })
        setStream(s)
        if (videoRef.current) videoRef.current.srcObject = s
      } catch (e) {
        // fallback to any camera
        const s = await navigator.mediaDevices.getUserMedia({ video: true })
        setStream(s)
        if (videoRef.current) videoRef.current.srcObject = s
      }
    }
    start()
    return () => {
      if (stream) stream.getTracks().forEach(t => t.stop())
    }
  }, [])

  const capture = () => {
    const video = videoRef.current
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    canvas.getContext('2d').drawImage(video,0,0)
    const dataUrl = canvas.toDataURL('image/png')
    onCaptured(dataUrl)
  }

  return (
    <div>
      <video ref={videoRef} autoPlay playsInline style={{width:'100%',maxHeight:400}} />
      <button onClick={capture}>Capturar</button>
    </div>
  )
}
```

3) Example posting to API (backend default host: http://localhost:8000):

```js
async function postDataUrlToApi(dataUrl){
  const blob = await (await fetch(dataUrl)).blob()
  const fd = new FormData()
  fd.append('files', blob, 'capture.png')
  const res = await fetch('http://localhost:8000/analyze_insects', { method: 'POST', body: fd })
  const json = await res.json()
  return json
}
```

4) Start FastAPI server (from repo root):

```bash
# ensure dependencies installed in your venv
python -m pip install -r requirements.txt
uvicorn api.app:app --reload --port 8000
```

5) Run the React app and test capture + POST.

Notes:
- `facingMode: { ideal: 'environment' }` will request rear camera on supporting browsers.
- Use HTTPS in production.
- You can deploy the React frontend to Vercel and API to Render/Heroku/Cloud Run.

If you want, I can scaffold the `frontend` React app in this repo and wire an example page that captures and posts images, then commit and push the changes.