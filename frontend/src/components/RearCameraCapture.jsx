import React, { useRef, useState, useEffect } from 'react'

export default function RearCameraCapture({ onCaptured }){
  const videoRef = useRef(null)
  const [stream, setStream] = useState(null)

  useEffect(() => {
    let mounted = true
    async function start() {
      try {
        const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: 'environment' } } })
        if (!mounted) return
        setStream(s)
        if (videoRef.current) videoRef.current.srcObject = s
      } catch (e) {
        try{
          const s = await navigator.mediaDevices.getUserMedia({ video: true })
          if (!mounted) return
          setStream(s)
          if (videoRef.current) videoRef.current.srcObject = s
        }catch(err){
          console.error('No camera access', err)
        }
      }
    }
    start()
    return () => {
      mounted = false
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
      <video ref={videoRef} autoPlay playsInline style={{width:'100%',maxHeight:400, background:'#000'}} />
      <div style={{display:'flex', gap:8, marginTop:8}}>
        <button onClick={capture}>Capturar</button>
      </div>
    </div>
  )
}
