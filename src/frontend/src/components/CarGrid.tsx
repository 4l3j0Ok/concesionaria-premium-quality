import { useState, useEffect } from "react";
import type { Car } from "../types/car";
import "../components/CarGrid.css";

interface Props {
    apiUrl: string;
    showOnlyOffers?: boolean;
}

export default function CarGrid({ apiUrl, showOnlyOffers = false }: Props) {
    const [cars, setCars] = useState<Car[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchCars = async () => {
            try {
                setLoading(true);
                const response = await fetch(apiUrl);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();

                // Mapear los datos de la API
                const mappedCars = data.items.map((car: any) => ({
                    code: car.car_code,
                    brand: car.brand,
                    model: car.model,
                    year: car.year,
                    km: car.km,
                    price: car.price,
                    promotionPrice: car.promotion_price,
                    img: car.image ? `data:image/webp;base64,${car.image}` : null,
                    description: car.description,
                    features: car.features,
                }));

                // Filtrar por ofertas si es necesario
                const displayCars = showOnlyOffers
                    ? mappedCars.filter(
                        (car: Car) => car.promotionPrice && car.promotionPrice < car.price
                    )
                    : mappedCars;

                setCars(displayCars);
                setError(null);
            } catch (err) {
                console.error("Error fetching cars:", err);
                setError("Error al cargar los vehículos");
                setCars([]);
            } finally {
                setLoading(false);
            }
        };

        fetchCars();
    }, [apiUrl, showOnlyOffers]);

    if (loading) {
        return (
            <section className="car-grid">
                {Array.from({ length: 6 }).map((_, i) => (
                    <div key={i} className="skeleton-card">
                        <div className="skeleton-image"></div>
                        <div className="skeleton-title"></div>
                        <div className="skeleton-price"></div>
                        <div className="skeleton-details"></div>
                    </div>
                ))}
            </section>
        );
    }

    if (error) {
        return (
            <section className="car-grid">
                <div className="no-cars-message">
                    <p>{error}</p>
                    <p>Por favor, verifica que la API esté funcionando correctamente.</p>
                </div>
            </section>
        );
    }

    if (cars.length === 0) {
        return (
            <section className="car-grid">
                <div className="no-cars-message">
                    <p>No hay vehículos disponibles en este momento.</p>
                </div>
            </section>
        );
    }

    return (
        <section className="car-grid">
            {cars.map((car) => (
                <a key={car.code} href={`/cars/${car.code}`} className="car-link">
                    <div
                        className="car"
                        id={`${car.brand}-${car.model}`}
                        style={{ viewTransitionName: `car-card-${car.code}` }}
                    >
                        {car.img ? (
                            <img
                                src={car.img}
                                alt={`${car.brand} ${car.model}`}
                                className="car-image"
                                loading="lazy"
                                style={{ viewTransitionName: `image-${car.code}` }}
                            />
                        ) : (
                            <div className="car-image-placeholder"></div>
                        )}
                        <h2 style={{ viewTransitionName: `car-name-${car.code}` }}>
                            {car.brand} {car.model}
                        </h2>
                        <div className="price-container">
                            {car.promotionPrice && car.promotionPrice < car.price ? (
                                <>
                                    <p className="old-price">${car.price.toLocaleString()}</p>
                                    <p className="price">${car.promotionPrice.toLocaleString()}</p>
                                </>
                            ) : (
                                <p className="price">${car.price.toLocaleString()}</p>
                            )}
                        </div>
                        <p className="car-details">
                            {car.year} • {car.km.toLocaleString()} km
                        </p>
                    </div>
                </a>
            ))}
        </section>
    );
}
