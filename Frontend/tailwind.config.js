/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', 
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  safelist: [
    'input:-webkit-autofill',
    'input:-webkit-autofill:hover',
    'input:-webkit-autofill:focus',
    'input:-webkit-autofill:active',
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