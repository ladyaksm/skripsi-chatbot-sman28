export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // WAJIB BANGET
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0f7f9",
          100: "#ddeef3",
          200: "#bce0eb",
          300: "#409db9ff",
          400: "#3387a0ff",
          500: "#34656d",
          600: "#2d545e",
          700: "#254550",
          800: "#1d3640",
          900: "#152a30",
        },
        secondary: {
          50: "#fffbf5",
          100: "#fef6eb",
          200: "#fdebd1",
          300: "#fcd9a8",
          400: "#fac17f",
          500: "#faeab1",
          600: "#f5d9a1",
          700: "#e8c088",
          800: "#d9a870",
          900: "#c99058",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
