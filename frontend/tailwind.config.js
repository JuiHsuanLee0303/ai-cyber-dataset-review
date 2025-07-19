import { palette } from './src/themes/palette';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: palette.primary,
        secondary: palette.secondary,
        neutral: palette.neutral,
        white: palette.white,
        black: palette.black,
      },
    },
  },
  plugins: [],
} 