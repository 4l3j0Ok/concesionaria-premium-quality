export interface FinancingPlanData {
  id: string;
  name: string;
  rate: string;
  rateLabel: string;
  months: number;
  downPayment: number;
  gradient: string;
  features: string[];
  featured?: boolean;
}

export const FINANCING_PLANS: FinancingPlanData[] = [
  {
    id: "basic",
    name: "Plan Básico",
    rate: "12%",
    rateLabel: "TNA",
    months: 36,
    downPayment: 20,
    gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    features: [
      "Hasta 36 meses",
      "20% de anticipo",
      "Cuotas fijas",
      "Seguro incluido",
    ],
  },
  {
    id: "premium",
    name: "Plan Premium",
    rate: "8%",
    rateLabel: "TNA",
    months: 60,
    downPayment: 15,
    gradient: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    features: [
      "Hasta 60 meses",
      "15% de anticipo",
      "Cuotas fijas",
      "Seguro premium incluido",
      "Mantenimiento 1er año",
    ],
    featured: true,
  },
  {
    id: "promo",
    name: "Plan Promocional",
    rate: "0%",
    rateLabel: "TNA",
    months: 24,
    downPayment: 30,
    gradient: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
    features: [
      "Hasta 24 meses",
      "30% de anticipo",
      "Cuotas fijas",
      "Seguro incluido",
      "Solo autos seleccionados",
    ],
  },
];

// Mapa de gradientes por nombre de plan para búsqueda rápida
export const PLAN_GRADIENTS: Record<string, string> = FINANCING_PLANS.reduce(
  (acc, plan) => {
    acc[plan.name] = plan.gradient;
    return acc;
  },
  {} as Record<string, string>
);

// Función helper para obtener un plan por nombre
export function getPlanByName(name: string): FinancingPlanData | undefined {
  return FINANCING_PLANS.find((plan) => plan.name === name);
}

// Función helper para obtener el gradiente de un plan
export function getPlanGradient(planName: string): string {
  return PLAN_GRADIENTS[planName] || FINANCING_PLANS[0].gradient;
}
