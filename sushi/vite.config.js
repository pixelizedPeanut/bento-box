import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        // Tells Vite to switch to the modern, faster Dart Sass compilation API
        api: "modern-compiler",
        additionalData: `@use "@/assets/styles/_variables.scss" as *;`,
      },
    },
  },
});
