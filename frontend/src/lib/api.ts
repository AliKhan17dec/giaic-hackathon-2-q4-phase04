import axios from "axios";

export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function apiUrl(path: string) {
    if (!path) return API_URL;
    return `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;
}

export function authApiUrl(path: string) {
    const token = localStorage.getItem("token");
    if (!token) {
        // Handle cases where token is not available, e.g., redirect to login
        throw new Error("No authentication token found.");
    }

    const instance = axios.create({
        baseURL: API_URL,
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });

    return instance;
}