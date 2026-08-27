/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Playfair Display'", "serif"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
      },
      colors: {
        navy: {
          950: "#0a1628",
          900: "#0f1f3a",
          800: "#152a4a",
          700: "#1a3158",
        },
        gold: {
          500: "#c9a84c",
          400: "#e0c872",
        },
      },
    },
  },
  plugins: [],
};
