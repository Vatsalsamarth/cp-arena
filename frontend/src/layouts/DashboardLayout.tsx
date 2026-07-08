import { Outlet } from "react-router-dom";

import { Navbar } from "@/components/layout/Navbar";
import { Sidebar } from "@/components/layout/Sidebar";


export function DashboardLayout() {
  return (
    <div className="min-h-screen bg-background text-foreground">

      <Navbar />

      <div className="flex">

        <Sidebar />

        <main className="min-h-[calc(100vh-4rem)] flex-1 overflow-x-hidden p-4 md:p-6">
          <Outlet />
        </main>

      </div>

    </div>
  );
}