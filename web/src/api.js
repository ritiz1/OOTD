const API_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')
const storageKey = 'wear-this-session'

export const getSession = () => {
  try { return JSON.parse(localStorage.getItem(storageKey)) } catch { return null }
}
export const setSession = (session) => localStorage.setItem(storageKey, JSON.stringify(session))
export const clearSession = () => localStorage.removeItem(storageKey)
export const mediaUrl = (url) => !url || /^https?:\/\//.test(url) ? url : `${API_URL}${url}`

async function raw(path, options = {}, retried = false) {
  const session = getSession()
  const headers = new Headers(options.headers)
  if (session?.access) headers.set('Authorization', `Bearer ${session.access}`)
  if (options.body && !(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  let response = await fetch(`${API_URL}${path}`, { ...options, headers })
  if (response.status === 401 && session?.refresh && !retried) {
    const refresh = await fetch(`${API_URL}/api/auth/token/refresh/`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ refresh: session.refresh }),
    })
    if (refresh.ok) {
      const { access } = await refresh.json()
      setSession({ ...session, access })
      return raw(path, options, true)
    }
    clearSession()
  }
  if (response.status === 204) return null
  const body = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(body.detail || Object.values(body).flat().join(' ') || 'Something went wrong.')
  return body
}

export const api = {
  login: (credentials) => raw('/api/auth/token/', { method: 'POST', body: JSON.stringify(credentials) }),
  register: (data) => raw('/api/auth/register/', { method: 'POST', body: JSON.stringify(data) }),
  me: () => raw('/api/auth/me/'),
  updateMe: (data) => raw('/api/auth/me/', { method: 'PATCH', body: JSON.stringify(data) }),
  items: (params = {}) => raw(`/api/wardrobe/items/?${new URLSearchParams(params)}`),
  item: (id) => raw(`/api/wardrobe/items/${id}/`),
  deleteItem: (id) => raw(`/api/wardrobe/items/${id}/`, { method: 'DELETE' }),
  describe: (image) => { const form = new FormData(); form.append('image', image); return raw('/api/wardrobe/describe/', { method: 'POST', body: form }) },
  recommend: (schedule) => raw('/api/wardrobe/recommend/', { method: 'POST', body: JSON.stringify({ schedule }) }),
}
