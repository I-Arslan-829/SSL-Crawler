// src/components/Header.tsx
"use client";
import { usePathname } from "next/navigation";
import {sidebarPages} from "./sidebar.config"
import ThemeToggle from "./ThemeToggle";



export default function Header() {
  const pathname =usePathname();
  // If your URLs have dynamic segments, add logic to format more gracefully.
  const currentpage=sidebarPages.find(page=> page.route===pathname)
  const pageName = currentpage ? currentpage.label : "Dashboard";

  return (
    <header className="w-[99%] ml-2 mt-2 rounded-xl flex items-center justify-between px-6 py-4 bg-sidebarLight dark:bg-sidebarDark shadow-md">
      <h1 className="text-2xl font-bold text-navTextLight dark:text-navTextDark">
        {pageName}
      </h1> 
      <ThemeToggle />
    </header>
  );
}
