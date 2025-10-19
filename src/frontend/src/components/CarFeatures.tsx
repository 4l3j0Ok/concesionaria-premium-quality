import * as Accordion from "@radix-ui/react-accordion";
import { Icon } from "@iconify/react";
import type { CarFeatures } from "../types/car";
import "./CarFeatures.css";

interface Props {
  features?: CarFeatures;
}

export default function CarFeaturesAccordion({ features }: Props) {
  if (!features) {
    return null;
  }

  // Función helper para formatear valores booleanos
  const formatBoolean = (value?: boolean) => (value ? "Sí" : "No");

  // Estructura de características agrupadas
  const featureGroups = [
    {
      id: "general",
      title: "Información General",
      icon: "mdi:car",
      items: [
        { label: "Tipo de Carrocería", value: features.body_type },
        { label: "Tipo de Combustible", value: features.fuel_type },
        { label: "Transmisión", value: features.transmission },
      ].filter((item) => item.value),
    },
    {
      id: "capacity",
      title: "Capacidad",
      icon: "mdi:account-group",
      items: [
        { label: "Pasajeros", value: features.passengers },
        { label: "Puertas", value: features.doors },
      ].filter((item) => item.value),
    },
    {
      id: "safety",
      title: "Confort y Seguridad",
      icon: "mdi:shield-check",
      items: [
        {
          label: "Aire Acondicionado",
          value: formatBoolean(features.air_conditioning),
        },
        { label: "Airbags", value: features.airbags },
        { label: "Frenos ABS", value: formatBoolean(features.abs) },
      ].filter((item) => item.value && item.value !== "No"),
    },
  ];

  // Filtrar grupos vacíos
  const validGroups = featureGroups.filter((group) => group.items.length > 0);

  if (validGroups.length === 0) {
    return null;
  }

  return (
    <section className="car-features">
      <h2>Características</h2>
      <Accordion.Root
        type="multiple"
        defaultValue={[validGroups[0]?.id]}
        className="accordion-root"
      >
        {validGroups.map((group) => (
          <Accordion.Item
            key={group.id}
            value={group.id}
            className="accordion-item"
          >
            <Accordion.Header className="accordion-header">
              <Accordion.Trigger className="accordion-trigger">
                <Icon icon={group.icon} className="accordion-icon" />
                <span className="accordion-title">{group.title}</span>
              </Accordion.Trigger>
            </Accordion.Header>
            <Accordion.Content className="accordion-content">
              <dl className="features-list">
                {group.items.map((item, index) => (
                  <div key={index} className="feature-item">
                    <dt>{item.label}</dt>
                    <dd>{item.value}</dd>
                  </div>
                ))}
              </dl>
            </Accordion.Content>
          </Accordion.Item>
        ))}
      </Accordion.Root>
    </section>
  );
}
