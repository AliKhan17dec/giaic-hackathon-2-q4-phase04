"use client";

import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import * as jwtDecode from "jwt-decode";

// jwt-decode can be bundled differently depending on the build system
// Provide a small safe wrapper that tries the common export shapes.
function safeJwtDecode(token: string): any {
  try {
    // direct function (common)
    const anyJwt: any = jwtDecode as any;

    const isClass = (fn: any) => {
      if (typeof fn !== "function") return false;
      try {
        return /^\s*class\s+/.test(Function.prototype.toString.call(fn));
      } catch {
        return false;
      }
    };

    // 1) package exports the function directly (skip class constructors)
    if (typeof anyJwt === "function" && !isClass(anyJwt)) return anyJwt(token);

    // 2) package exposes default function
    if (anyJwt && typeof anyJwt.default === "function" && !isClass(anyJwt.default)) return anyJwt.default(token);

    // 3) some builds export named `jwt_decode`
    if (anyJwt && typeof anyJwt.jwt_decode === "function" && !isClass(anyJwt.jwt_decode)) return anyJwt.jwt_decode(token);

    // 4) sometimes the function is the only function property on the exported object
    if (anyJwt && typeof anyJwt === "object") {
      for (const k of Object.keys(anyJwt)) {
        const fn = anyJwt[k];
        if (typeof fn === "function" && !isClass(fn)) return fn(token);
      }
    }

    // last-resort: try global names (unlikely in Next but harmless)
    const globalDecoder = (globalThis as any).jwt_decode || (globalThis as any).jwtDecode;
    if (typeof globalDecoder === "function" && !isClass(globalDecoder)) return globalDecoder(token);

    throw new Error("jwt-decode not available or has unexpected shape");
  } catch (err) {
    throw err;
  }
}

interface AuthContextType {
  token: string | null;
  user: { username: string; id: number } | null;
  initialized: boolean;
  login: (newToken: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<{ username: string; id: number } | null>(
    null,
  );
  const [initialized, setInitialized] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      setToken(storedToken);
      try {
        const decoded: any = safeJwtDecode(storedToken);
        setUser({ username: decoded.sub, id: decoded.user_id }); // Assuming user_id is in the token
      } catch (error) {
        console.error("Failed to decode token:", error);
        localStorage.removeItem("token");
      }
    }
    setInitialized(true);
  }, []);

  const login = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    try {
      const decoded: any = safeJwtDecode(newToken);
      setUser({ username: decoded.sub, id: decoded.user_id });
      setInitialized(true);
      router.push("/tasks");
    } catch (error) {
      console.error("Failed to decode token:", error);
      localStorage.removeItem("token");
      setToken(null);
      setUser(null);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider value={{ token, user, initialized, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
