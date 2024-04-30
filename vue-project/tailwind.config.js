/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "light-accent1": "#2D6A4F",
        "light-accent2": "#1B4332",
        "g-a1": "#343535",
        "g-a2": "#3a3c3c",
        "g-a3": "#454647",
      }
    },
    container: {
      padding: "2rem",
      center: true,
    },
  },
  plugins: [],
}
