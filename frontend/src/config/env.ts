const env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL,
  appName: import.meta.env.VITE_APP_NAME,
  appVersion: import.meta.env.VITE_APP_VERSION,
} as const;

function requireEnv(value: string | undefined, name: string): string {
  if (!value || value.trim() === "") {
    throw new Error(`Missing required environment variable: ${name}`);
  }

  return value;
}

export const ENV = {
  apiBaseUrl: requireEnv(env.apiBaseUrl, "VITE_API_BASE_URL"),
  appName: requireEnv(env.appName, "VITE_APP_NAME"),
  appVersion: requireEnv(env.appVersion, "VITE_APP_VERSION"),
} as const;