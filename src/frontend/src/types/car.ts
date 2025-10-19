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
export interface CarFromAPI {
    id: number;
    brand: string;
    model: string;
    description: string;
    price: number;
    promotion_price: number | null;
    km: number;
    year: number;
    car_code: string;
    image: string | null; // Base64 string
    features?: CarFeatures;
}

export interface CarAPIResponse {
    total: number;
    offset: number;
    limit: number;
    items: CarFromAPI[];
}

// Tipo para el auto procesado en el frontend
export interface Car {
    code: string;
    brand: string;
    model: string;
    description: string;
    price: number;
    promotionPrice: number | null;
    km: number;
    year: number;
    img: string; // Data URL o path a imagen por defecto
    features?: CarFeatures;
}

// Función helper para convertir de API a formato frontend
export function mapCarFromAPI(car: CarFromAPI): Car {
    return {
        code: car.car_code,
        brand: car.brand,
        model: car.model,
        description: car.description,
        price: car.price,
        promotionPrice: car.promotion_price,
        km: car.km,
        year: car.year,
        // Si viene base64, crear data URL; si no, usar imagen por defecto
        img: car.image
            ? `data:image/jpeg;base64,${car.image}`
            : "/assets/images/chevrolet-astra.webp",
        features: car.features,
    };
}
