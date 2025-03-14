import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // Default port for Vite
    open: true, // Opens browser automatically
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000", // Flask backend
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  build: {
    outDir: "build", // Output folder for production
  },
  base: "/",
});
