import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bills: {
          blue: "#00338D",
          navy: "#00143D",
          red: "#C60C30",
          white: "#FFFFFF",
          silver: "#F2F4F8",
          steel: "#7A8BA6",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "Impact", "sans-serif"],
        body: ["var(--font-body)", "system-ui", "sans-serif"],
      },
      letterSpacing: {
        tightest: "-0.04em",
      },
      boxShadow: {
        card: "0 1px 2px rgba(0,20,61,0.06), 0 4px 16px rgba(0,20,61,0.08)",
        lift: "0 2px 6px rgba(0,20,61,0.08), 0 12px 32px rgba(0,20,61,0.14)",
      },
    },
  },
  plugins: [],
};

export default config;
