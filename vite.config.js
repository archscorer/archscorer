import { defineConfig } from "vite";
import { createVuePlugin as vue } from "vite-plugin-vue2"; //vue 2
import { VuetifyResolver } from "unplugin-vue-components/resolvers";
import Components from "unplugin-vue-components/vite";
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8008'
      },
      '^/accounts': {
        target: 'http://localhost:8008',
        changeOrigin: true
      },
      '^/static': {
        target: 'http://localhost:8008',
        changeOrigin: true
      }
    },
    cors: {
      preflightContinue: true,
      // methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    }
  },
  build: {
    outDir: 'django/frontend',
    assetsDir: 'static',
  },
  plugins: [
    vue(),
    Components({
      resolvers: [
        // Vuetify
        VuetifyResolver(),
      ],
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
