import { supabase } from '../lib/supabase'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function authHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session) throw new Error('Not authenticated')
  return { Authorization: `Bearer ${session.access_token}` }
}

async function request(url, options = {}) {
  const res = await fetch(url, options)
  if (!res.ok) {
    let message = res.statusText
    try {
      const body = await res.json()
      message = body.detail || message
    } catch { /* ignore */ }
    throw new Error(message)
  }
  return res.json()
}

export async function createSession({ audioBlob, mode, durationSec }) {
  const headers = await authHeaders()
  const formData = new FormData()
  formData.append('audio_file', audioBlob, `recording.webm`)
  formData.append('mode', mode)
  if (durationSec != null) formData.append('duration_sec', String(durationSec))

  return request(`${API_URL}/sessions`, {
    method: 'POST',
    headers,
    body: formData,
  })
}

export async function listSessions({ limit = 20, offset = 0, mode } = {}) {
  const headers = await authHeaders()
  const params = new URLSearchParams({ limit, offset })
  if (mode) params.set('mode', mode)

  return request(`${API_URL}/sessions?${params}`, { headers })
}

export async function getSession(id) {
  const headers = await authHeaders()
  return request(`${API_URL}/sessions/${id}`, { headers })
}
