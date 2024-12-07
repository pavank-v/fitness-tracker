/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', 
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#1a1a1a',
        primary: '#111111',    
        secondary: '#2a2a2a',  
      },
    },
  },
  plugins: [],
}