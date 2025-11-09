// src/components/ThemeProvider.tsx
"use client";
import React, { createContext, useContext, useEffect, useState } from "react";

const ThemeContext = createContext<{isDark: boolean, toggle: () => void}>({isDark: false, toggle: () => {}});

export function ThemeProvider({children}:{children:React.ReactNode}) {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem("theme");
    setIsDark(stored==="dark");
  }, []);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [isDark]);

  const toggle = () => setIsDark(d => !d);

  return (
    <ThemeContext.Provider value={{isDark, toggle}}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
