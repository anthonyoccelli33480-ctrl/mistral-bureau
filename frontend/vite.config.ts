import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// base is "/mistral-bureau/" for production builds (GitHub Pages project site)
// and "/" in dev so the local proxy keeps working.
export default defineConfig(({ command }) => ({
  base: command === "build" ? "/mistral-bureau/" : "/",
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5177,
    strictPort: false,
    proxy: { "/api": "http://127.0.0.1:8789" },
  },
}));
