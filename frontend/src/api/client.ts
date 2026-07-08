import axios from "axios";
import toast from "react-hot-toast";

import { ENV } from "@/config/env";

import { tokenStorage } from "./storage";


export const apiClient = axios.create({
  baseURL: ENV.apiBaseUrl,

  headers: {
    "Content-Type": "application/json",
  },

  timeout: 30000,
});


apiClient.interceptors.request.use(
  (config) => {
    const token =
      tokenStorage.get();

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
    }

    return config;
  },
);


apiClient.interceptors.response.use(
  (response) =>
    response,


  (error) => {
    const status =
      error.response?.status;


    if (status === 401) {
      tokenStorage.clear();

      window.location.href =
        "/login";

      return Promise.reject(error);
    }


    if (status >= 500) {
      toast.error(
        "Server error. Please try again later.",
      );
    }


    if (!error.response) {
      toast.error(
        "Network error. Check your connection.",
      );
    }


    return Promise.reject(error);
  },
);