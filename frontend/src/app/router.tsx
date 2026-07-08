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
import { ProblemsPage } from "@/pages/problems/ProblemsPage";
import { ProblemDetailPage } from "@/pages/problems/ProblemDetailPage";

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

              {
                path: "/problems",
                element: <ProblemsPage />,
              },

              {
                path: "/problems/:slug",
                element: <ProblemDetailPage />,
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