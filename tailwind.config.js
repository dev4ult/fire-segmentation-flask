/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/**/*.html'],
  daisyui: {
    themes: ['business'],
  },
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
};
