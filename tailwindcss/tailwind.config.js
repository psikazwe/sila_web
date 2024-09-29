/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "../core/templates/**/**/*.{html, js}", "../core/static/*.{html, js}" ,
    "../administrator/templates/**/**/*.{html, js}", "../administrator/static/*.{html, js}" ,
    "../client/templates/**/**/*.{html, js}", "../client/static/*.{html, js}" ,
    "../staff/templates/**/**/*.{html, js}", "../staff/static/*.{html, js}" ,
  ],
  theme: {
    extend: {
      colors: {
        text:{
          "label": "#64748b",
          "mute": "#94a3b8",
          "heading": "#020617",
          "important": "#020617",
        },
        tone: '#119e4e47',
        darker: '#0f172a',
        primary:{
          '50': "#ecfdf5",
          '100': "#d1fae5",
          '200': "#a7f3d0",
          '300': "#6ee7b7",
          '400': "#34d399",
          '500': "#059669",
          '600': "#059669",
          '700': "#047857",
          '800': "#065f46",
          '900': "#064e3b",
          '950': "#022c22"
        },
        secondary:{
          "50":"#fff1f2",
          "100":"#ffe4e6",
          "200":"#fecdd3",
          "300":"#fda4af",
          "400":"#fb7185",
          "500":"#f43f5e",
          "600":"#e11d48",
          "700":"#be123c",
          "800":"#9f1239",
          "900":"#881337",
          "950":"#4c0519",
        },

        light: {
          'tertiary': '#f3f4f6',
          'background': '#ecfdf5',
        },
        dark: {
          "50":"#f8fafc",
          "100":"#f1f5f9",
          "200":"#e2e8f0",
          "300":"#cbd5e1",
          "400":"#94a3b8",
          "500":"#64748b",
          "600":"#475569",
          "700":"#334155",
          "800":"#1e293b",
          "900":"#0f172a",
          "950":"#020617",
        },
      },
      fontSize: {
        'xs': '0.85rem',
        'sm': '0.95rem',
      },
      keyframes: {
        slidein: {
          from: {
            opacity: "0",
            transform: "translateY(-10px)",
          },
          to: {
            opacity: "1",
            transform: "translateY(0)",
          },
        },
      },
      animation: {
        slidein: "slidein 600ms ease var(--slidein-delay, 0) forwards",
      },
    },
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
  ],
}

