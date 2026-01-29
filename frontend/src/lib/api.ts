export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function apiUrl(path: string) {
    if (!path) return API_URL;
    return `${API_URL}${path.startsWith("/") ? "" : "/"}${path}`;
}
