// src/app/layout.tsx
import "./globals.css";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import { ThemeProvider } from "@/components/ThemeProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-bgLight dark:bg-bgDark">

        <ThemeProvider>
          <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col">
              {/* HEADER IS HERE, AT THE TOP OF MAIN CONTENT */}
              <Header />
              <main className="pt-5 pb-5 flex-1 flex flex-col items-center justify-start">
                {children}
              </main>
            </div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}


// function ThemeInitScript() {
//   return (
//     <script
//       dangerouslySetInnerHTML={{
//         __html: `
//           (function() {
//             try {
//               var theme = localStorage.getItem('theme');
//               if (theme === 'dark') {
//                 document.documentElement.classList.add('dark');
//               } else {
//                 document.documentElement.classList.remove('dark');
//               }
//             } catch (e) {}
//           })();
//         `,
//       }}
//     />
//   );
// }

// // Now use this in your layout file:
// import "../globals.css";
// import Sidebar from "@/components/Sidebar";
// import ThemeToggle from "@/components/ThemeToggle";
// import { ThemeProvider } from "@/components/ThemeProvider";

// export default function RootLayout({ children }: { children: React.ReactNode }) {
//   return (
//     <html lang="en" suppressHydrationWarning>
//       <body className="bg-gray-50 dark:bg-gray-900 transition-all">
//         <ThemeInitScript />
//         <ThemeProvider>
//           <div className="flex min-h-screen">
//             <Sidebar />
//             <main className="flex-1 flex flex-col items-center justify-center relative">
//               <ThemeToggle />
//               {children}
//             </main>
//           </div>
//         </ThemeProvider>
//       </body>
//     </html>
//   );
// }




