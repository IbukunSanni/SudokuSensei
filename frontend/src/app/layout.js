import "./globals.css";

export const metadata = {
  title: "Sudoku Sensei",
  description: "An educational Sudoku solver",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
