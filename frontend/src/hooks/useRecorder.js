import { useCallback, useRef, useState } from 'react'

function getSupportedMimeType() {
  const types = ['audio/webm', 'audio/mp4', 'audio/ogg']
  return types.find((t) => MediaRecorder.isTypeSupported(t)) ?? ''
}

export function useRecorder() {
  const [isRecording, setIsRecording] = useState(false)
  const [duration, setDuration] = useState(0)

  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])
  const timerRef = useRef(null)
  const mimeTypeRef = useRef('')

  const start = useCallback(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const mimeType = getSupportedMimeType()
    mimeTypeRef.current = mimeType

    const mr = new MediaRecorder(stream, mimeType ? { mimeType } : {})
    mediaRecorderRef.current = mr
    chunksRef.current = []

    mr.ondataavailable = (e) => {
      if (e.data.size > 0) chunksRef.current.push(e.data)
    }

    mr.start(100)
    setIsRecording(true)
    setDuration(0)

    timerRef.current = setInterval(() => {
      setDuration((d) => d + 1)
    }, 1000)
  }, [])

  const stop = useCallback(() => {
    return new Promise((resolve) => {
      const mr = mediaRecorderRef.current
      if (!mr) return resolve(null)

      mr.onstop = () => {
        const blob = new Blob(chunksRef.current, {
          type: mimeTypeRef.current || 'audio/webm',
        })
        resolve(blob)
      }

      mr.stop()
      mr.stream.getTracks().forEach((t) => t.stop())
      clearInterval(timerRef.current)
      setIsRecording(false)
    })
  }, [])

  return { isRecording, duration, start, stop }
}
