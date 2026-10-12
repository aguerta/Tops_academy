/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ka-blue': '#1865f2',
        'ka-blue-hover': '#1456c7',
        'ka-blue-light': '#f0f7ff',
        'ka-mastered': '#583b8b',
        'ka-proficient': '#8377b2',
        'ka-familiar': '#e07a21',
        'ka-attempted': '#f3801e',
        'ka-not-started': '#88939e',
        'ka-green-border': '#14a34b',
        'ka-green-badge': '#008a00',
        'ka-green-text': '#0b6b2d',
        'ka-red-border': '#d92938',
        'ka-red-badge': '#dc2626',
        'ka-red-text': '#991b1b',
        'ka-text-primary': '#21242c',
        'ka-text-secondary': '#59606d',
        'ka-text-muted': '#88939e',
        'ka-border-subtle': '#eaedf1',
        'ka-border-card': '#e4e7eb',
      }
    },
  },
  plugins: [],
}
