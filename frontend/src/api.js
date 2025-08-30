import axios from 'axios'


const API = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:5000/api' })


export const uploadCSV = (file) => {
const form = new FormData()
form.append('file', file)
return API.post('/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } })
}


export const getTransactions = () => API.get('/transactions')
export const getSu