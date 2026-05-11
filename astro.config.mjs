import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import node from '@astrojs/node';

export default defineConfig({
  integrations: [react(), tailwind()],
<<<<<<< HEAD
  output: 'static',
=======
  output: 'hybrid',
  adapter: node({
    mode: 'standalone'
  }),
>>>>>>> c76a3f1d61e5b62006056371c82f07ea9b70ab85
  vite: {
    server: {
      fs: {
        allow: ['..']
      }
    }
  }
});
