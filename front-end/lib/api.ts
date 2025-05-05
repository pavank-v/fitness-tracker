import axios, { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../lib/constant";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

const api: AxiosInstance = axios.create({
  baseURL: BASE_URL as string,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem(ACCESS_TOKEN);
      if (token) {
        config.headers = config.headers || {}; 
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

const AUTH_ENDPOINTS = ["/auth/token/", "/auth/user/"];

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (!originalRequest || originalRequest.url === undefined) {
      return Promise.reject(error);
    }

    const isAuthEndpoint = AUTH_ENDPOINTS.some(endpoint => 
      originalRequest.url?.startsWith(endpoint) || originalRequest.url === endpoint
    );

    if (isAuthEndpoint) {
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      if (typeof window !== "undefined") {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        
        if (refreshToken) {
          try {
            const res = await api.post("/auth/token/refresh/", { 
              refresh: refreshToken 
            });

            if (res.status === 200 && res.data?.access) {
              const newAccessToken = res.data.access;
              localStorage.setItem(ACCESS_TOKEN, newAccessToken);

              originalRequest.headers = originalRequest.headers || {};
              originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

              return api(originalRequest);
            }
          } catch (refreshError) {
            localStorage.removeItem(ACCESS_TOKEN);
            localStorage.removeItem(REFRESH_TOKEN);
            
            if (typeof window !== "undefined") {
              window.location.href = "/login"; 
            }
          }
        } else {
          if (typeof window !== "undefined") {
            window.location.href = "/login";
          }
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;