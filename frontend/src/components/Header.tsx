"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function Header() {
    const { user, logout, initialized } = useAuth();
    const router = useRouter();

    const handleLogout = async () => {
        logout();
        router.push("/");
    };

    return (
        <header className="w-full bg-blue-900 text-white">
            <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
                <Link href="/" className="flex items-center space-x-3">
                    <div className="h-10 w-10 rounded-md bg-white text-blue-900 flex items-center justify-center font-bold">G</div>
                    <div className="text-lg font-semibold">Giaic Tasks</div>
                </Link>

                <nav className="flex items-center space-x-3">
                    <Link href="/" className="btn-ghost">
                        Home
                    </Link>
                    <Link href="/tasks" className="btn-ghost">
                        Tasks
                    </Link>

                    {initialized && user ? (
                        <div className="flex items-center space-x-2">
                            <span className="hidden sm:inline-block">{user.username}</span>
                            <button onClick={handleLogout} className="ml-2 rounded-md bg-white px-3 py-1 text-blue-900">
                                Logout
                            </button>
                        </div>
                    ) : (
                        <div className="flex items-center space-x-2">
                            <Link href="/login" className="rounded-md bg-white px-3 py-1 text-blue-900">
                                Log in
                            </Link>
                            <Link href="/signup" className="rounded-md bg-blue-800 px-3 py-1 text-white">
                                Sign up
                            </Link>
                        </div>
                    )}
                </nav>
            </div>
        </header>
    );
}
