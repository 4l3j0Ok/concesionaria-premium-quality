// Tipos para las características del vehículo
export interface CarFeatures {
    fuel_type?: string; // Tipo de combustiblec
    transmission?: string; // Tipo de transmisión: manual, automática, et.
    body_type?: string; // Tipo de carrocería: SUV, sedán, hatchback, etc.
    passengers?: number; // Número de pasajeros
    doors?: number; // Número de puertas
    air_conditioning?: boolean; // Aire acondicionado
    airbags?: number; // Número de airbags
    abs?: boolean; // Frenos ABS
}

// Tipos para los datos que vienen de la API
export interface Car {
    id: number;
    brand: string;
    model: string;
    description: string;
    price: number;
    promotion_price: number | null;
    km: number;
    year: number;
    car_code: string;
    image: string;
    features?: CarFeatures;
}

export interface CarAPIResponse {
    total: number;
    offset: number;
    limit: number;
    items: Car[];
}
