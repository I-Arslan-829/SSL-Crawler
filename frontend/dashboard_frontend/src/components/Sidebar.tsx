import React from "react";
import Link from "next/link";
import {sidebarPages} from "./sidebar.config"
export default function Sidebar() {
  return (
    <aside className="flex flex-col bg-sidebarLight dark:bg-sidebarDark h-auto w-sidebarwidth px-6 py-5 shadow-lg">
      <h2 className="text-2xl font-bold -mt-1 mb-2 ml-2 text-sidebarTextLight dark:text-sidebarTextDark">
        Certificate Analysis
      </h2>
      <nav className="flex flex-col gap-2">
        {sidebarPages.map(item => (
          <Link
            key={item.label}
            href={item.route}
            className="
              flex items-center flex items-center gap-2           
              px-4 py-2
              bg-navButtonLight dark:bg-navButtonDark
              text-navTextLight dark:text-navTextDark text-lg
              hover:bg-navButtonHoverLight dark:hover:bg-navButtonHoverDark
              rounded-2xl
              border-2 border-solid
              border-navButtonBorderLight dark:border-navButtonBorderDark
              transition
            "     //css of sidebar buttons
          >
            <item.icon size={15} />
             {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
