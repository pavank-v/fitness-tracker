import ".././globals.css";
import AuthHeader from "@/components/AuthHeader"


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
      <div>
        <AuthHeader />
        {children}
      </div>
  );
}