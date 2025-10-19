// @ts-check
import { defineConfig, envField } from 'astro/config';
import node from '@astrojs/node';
import icon from 'astro-icon';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  output: 'server',

  adapter: node({
    mode: 'standalone'
  }),
  integrations: [icon(), react()],
  env: {
    schema: {
      API_URL: envField.string({ context: "server", access: "secret" }),
      APP_VERSION: envField.string({ context: "client", access: "public" }),
    }
  },
});