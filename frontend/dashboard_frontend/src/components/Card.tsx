"use client";
import React from "react";

interface CardProps {
  title: string;
  value: React.ReactNode;
  className?: string;
  onClick?: () => void;
}

export default function Card({ title, value, className = "", onClick }: CardProps) {
  const handleClick = () => {
    if (onClick) onClick();
    else alert("Not developed yet!");
  };

  return (
    <button
      className={`
        pt-5 pl-5 text-lg flex flex-col items-start justify-start
        rounded-xl shadow-xl font-semibold
        bg-sidebarLight dark:bg-sidebarDark
        text-navTextLight dark:text-navTextDark
        transition cursor-pointer select-none
        ${className}
      `}
      onClick={handleClick}
      type="button"
    >
      <span className="text-xl mb-1">{title}</span>
      <span className="text-4xl font-bold  h-[100%] ">{value}</span>
    </button>
  );
}



