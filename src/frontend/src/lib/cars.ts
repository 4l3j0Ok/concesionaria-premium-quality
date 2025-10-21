import type { Car, CarAPIResponse } from '../types/car';
import { API_URL } from "astro:env/server";

const isProd = import.meta.env.PROD;

const domain = API_URL.endsWith('/')
  ? API_URL.slice(0, -1)
  : API_URL;
const apiUrl = `${domain}/cars`

// devolvemos un array o un solo coche según se le pase el código
export const getCar = async (car_code?: string): Promise<Car | Car[] | null> => {
  const url = car_code ? `${apiUrl}?car_code=${car_code}` : apiUrl

  try {
    const res = await fetch(url)
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`)
    }
    const data: CarAPIResponse = await res.json()

    // En desarrollo, agregamos el dominio del backend a las URLs de las imágenes
    // En producción, las URLs son relativas y nginx las sirve correctamente
    if (!isProd) {
      data.items = data.items.map(car => ({
        ...car,
        image: car.image.startsWith('/') ? `${domain}${car.image}` : car.image
      }))
    }

    return data.items;
  } catch (error) {
    console.error('Error fetching car:', error)
    return [];
  }
}