import {
  createBrowserRouter,
  Navigate,
  Outlet,
  RouterProvider,
} from "react-router-dom";

import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { DashboardLayout } from "@/layouts/DashboardLayout";

import { LoginPage } from "@/pages/LoginPage";
import { DashboardPage } from "@/pages/dashboard/DashboardPage";

function RootLayout() {
  return (
    <div className="dark min-h-screen bg-background text-foreground">
      <Outlet />
    </div>
  );
}

const router = createBrowserRouter([
  {
    element: <RootLayout />,

    children: [
      {
        path: "/login",
        element: <LoginPage />,
      },

      {
        element: <ProtectedRoute />,

        children: [
          {
            element: <DashboardLayout />,

            children: [
              {
                path: "/",
                element: <DashboardPage />,
              },
            ],
          },
        ],
      },

      {
        path: "*",
        element: <Navigate to="/" replace />,
      },
    ],
  },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}