import {
  LayoutDashboard,
  Trophy,
  Code2,
  User,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const links = [
  {
    name: "Dashboard",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    name: "Problems",
    path: "/problems",
    icon: Code2,
  },
  {
    name: "Leaderboard",
    path: "/leaderboard",
    icon: Trophy,
  },
  {
    name: "Profile",
    path: "/profile",
    icon: User,
  },
];

export function Sidebar() {
  return (
    <aside className="hidden w-64 border-r border-border bg-card p-6 md:block">
      <nav className="space-y-2">
        {links.map((link) => {
          const Icon = link.icon;

          return (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "hover:bg-muted"
                }`
              }
            >
              <Icon className="h-4 w-4" />

              {link.name}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}