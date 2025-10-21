import { useEffect, useState } from "react";
import { Icon } from "@iconify/react";
import type { Car } from "../types/car";
import type { FinancingPlan } from "../types/plan";
import { getPlanGradient } from "../data/financingPlans";
import "./Contact.css";


const STORAGE_CAR_KEY = "contact_car";
const STORAGE_PLAN_KEY = "contact_plan";

export default function Contact() {
  const [attachedCar, setAttachedCar] = useState<Car | null>(null);
  const [attachedPlan, setAttachedPlan] = useState<FinancingPlan | null>(null);
  const [isRemoving, setCarIsRemoving] = useState(false);
  const [isRemovingPlan, setPlanIsRemoving] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

  useEffect(() => {
    // Función para cargar el carro y plan desde localStorage
    const loadComponentsFromStorage = () => {
      const storedCar = localStorage.getItem(STORAGE_CAR_KEY);
      const storedPlan = localStorage.getItem(STORAGE_PLAN_KEY);
      if (storedCar) {
        try {
          const car = JSON.parse(storedCar);
          setAttachedCar(car);
          setCarIsRemoving(false);
        } catch (e) {
          console.error("Error parsing stored car:", e);
          localStorage.removeItem(STORAGE_CAR_KEY);
        }
      }
      if (storedPlan) {
        try {
          const plan = JSON.parse(storedPlan);
          setAttachedPlan(plan);
          setPlanIsRemoving(false);
        } catch (e) {
          console.error("Error parsing stored plan:", e);
          localStorage.removeItem(STORAGE_PLAN_KEY);
        }
      }
    };

    // Escuchar cambios en el storage (de otras pestañas y eventos manuales)
    const handleStorageChange = () => {
      loadComponentsFromStorage();
    };
    window.addEventListener("storage", handleStorageChange);

    loadComponentsFromStorage();

    // Limpiar el listener al desmontar para evitar fugas de memoria
    return () => {
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  const handleRemoveCar = () => {
    setCarIsRemoving(true);
    // Esperar a que termine la animación antes de remover
    setTimeout(() => {
      setAttachedCar(null);
      localStorage.removeItem(STORAGE_CAR_KEY);
      setCarIsRemoving(false);
    }, 300); // Duración de la animación bounceOut
  };
  const handleRemovePlan = () => {
    setPlanIsRemoving(true);
    // Esperar a que termine la animación antes de remover
    setTimeout(() => {
      setAttachedPlan(null);
      localStorage.removeItem(STORAGE_PLAN_KEY);
      setPlanIsRemoving(false);
    }, 300); // Duración de la animación bounceOut
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitMessage(null);

    const form = e.currentTarget;
    const formData = new FormData(form);

    // Preparar datos como JSON
    const requestData = {
      name: formData.get('name') as string,
      email: formData.get('email') as string,
      message: formData.get('message') as string,
      car: attachedCar || undefined,
      plan: attachedPlan || undefined,
    };

    try {
      // Enviar al endpoint de Astro (servidor) como JSON
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (response.ok) {
        setSubmitMessage({ type: 'success', text: '¡Mensaje enviado correctamente! Te responderemos pronto.' });
        form.reset();
        // Limpiar attachments después de enviar
        if (attachedCar) {
          localStorage.removeItem(STORAGE_CAR_KEY);
          setAttachedCar(null);
        }
        if (attachedPlan) {
          localStorage.removeItem(STORAGE_PLAN_KEY);
          setAttachedPlan(null);
        }
      } else {
        setSubmitMessage({ type: 'error', text: 'Error al enviar el mensaje. Por favor, intenta nuevamente.' });
      }
    } catch (error) {
      console.error('Error sending contact form:', error);
      setSubmitMessage({ type: 'error', text: 'Error al enviar el mensaje. Por favor, intenta nuevamente.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="contact" id="contact">
      <h2>Contacto</h2>
      <form className="contact-form" id="contact-form" onSubmit={handleSubmit}>
        {attachedCar && (
          <div
            className={`car-attachment${isRemoving ? ' removing' : ''}`}
            id="car-attachment"
          >
            <div className="attachment-header">
              <div className="attachment-info">
                <Icon icon="mdi:information" />
                <span>Estás consultando sobre este vehículo:</span>
              </div>
              <button
                type="button"
                className="remove-attachment"
                onClick={handleRemoveCar}
                aria-label="Quitar vehículo de la consulta"
              >
                <Icon icon="mdi:close" />
              </button>
            </div>
            <a href={`/cars/${attachedCar.code}`} className="attachment-link">
              <div className="car-tag">
                {attachedCar.image && (
                  <img
                    src={attachedCar.image}
                    alt={`${attachedCar.brand} ${attachedCar.model}`}
                    className="car-tag-image"
                  />
                )}
                <div className="car-tag-info">
                  <strong>
                    {attachedCar.brand} {attachedCar.model}
                  </strong>
                  <span className="car-tag-details">
                    {attachedCar.year} •{" "}
                    {attachedCar.km.toLocaleString()} km
                  </span>
                </div>
              </div>
            </a>
          </div>
        )}
        {attachedPlan && (
          <div
            className={`plan-attachment${isRemovingPlan ? ' removing' : ''}`}
            id="plan-attachment"
          >
            <div className="attachment-header">
              <div className="attachment-info">
                <Icon icon="mdi:information" />
                <span>Estás consultando sobre este plan de financiación:</span>
              </div>
              <button
                type="button"
                className="remove-attachment"
                onClick={handleRemovePlan}
                aria-label="Quitar plan de la consulta"
              >
                <Icon icon="mdi:close" />
              </button>
            </div>
            <a href={`/financing#plans`} className="attachment-link">
              <div className="plan-tag">
                <div
                  className="plan-tag-header"
                  style={{
                    background: getPlanGradient(attachedPlan.name),
                    backgroundImage: getPlanGradient(attachedPlan.name)
                  }}
                >
                  <strong>{attachedPlan.name}</strong>
                  <div className="plan-tag-rate">
                    <span className="rate-value">{attachedPlan.rate}</span>
                    <span className="rate-label">{attachedPlan.rateLabel}</span>
                  </div>
                </div>
                <div className="plan-tag-details">
                  <span>• Hasta {attachedPlan.months} meses</span>
                  <span>• {attachedPlan.downPayment}% de anticipo</span>
                </div>
              </div>
            </a>
          </div>
        )}
        <label htmlFor="name">Nombre y apellido:</label>
        <input
          type="text"
          name="name"
          placeholder="Juan Pérez"
          required
          id="name"
          autoComplete="name"
          disabled={isSubmitting}
        />
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          name="email"
          placeholder="juan.perez@example.com"
          required
          id="email"
          autoComplete="email"
          disabled={isSubmitting}
        />
        <label htmlFor="message">Mensaje:</label>
        <textarea
          name="message"
          placeholder="Hola, quisiera contactarme por..."
          required
          id="message"
          autoComplete="off"
          disabled={isSubmitting}
        />
        {submitMessage && (
          <div className={`submit-message ${submitMessage.type}`}>
            {submitMessage.text}
          </div>
        )}
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Enviando...' : 'Enviar'}
        </button>
      </form>
    </section >
  );
}
