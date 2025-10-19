import type { APIRoute } from 'astro';

export const POST: APIRoute = async ({ request }) => {
  try {
    // Recibir datos como JSON
    const data = await request.json();
    const { name, email, message, car, plan } = data;

    if (!name || !email || !message) {
      return new Response(JSON.stringify({ error: 'Todos los campos son requeridos' }), {
        status: 400,
        headers: {
          'Content-Type': 'application/json'
        }
      });
    }

    // Preparar body como JSON para el backend
    const requestBody = {
      contact_name: name,
      contact_email: email,
      contact_message: message,
      car_data: car || null,
      plan_data: plan || null,
    };

    // Llamar al backend (será resuelto por NGINX en producción)
    const backendUrl = import.meta.env.API_URL || 'http://localhost:8000';
    const response = await fetch(`${backendUrl}/contact`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`);
    }

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error sending contact email:', error);
    return new Response(JSON.stringify({ error: 'Error al enviar el mensaje' }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }
};
