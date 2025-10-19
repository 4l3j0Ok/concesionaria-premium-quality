import type { CarAPIResponse } from '../types/car';

const domain = import.meta.env.API_URL
const apiUrl = `${domain}/cars`


export const getCar = async (car_code?: string): Promise<CarAPIResponse> => {
  const url = car_code ? `${apiUrl}?car_code=${car_code}` : apiUrl

  try {
    const res = await fetch(url)
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`)
    }
    const data: CarAPIResponse = await res.json()
    return data
  } catch (error) {
    console.error('Error fetching car:', error)
    return { total: 0, offset: 0, limit: 0, items: [] }
  }
}