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
                    <Link href="/chat" className="btn-ghost flex items-center space-x-1">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 8.25h9m-9 3H12m-9.75 1.51c0 1.733 1.395 3.132 3.128 3.132h5.344l2.922 2.922c.177.177.416.276.666.276.424 0 .768-.343.768-.768v-2.43c.996-.607 1.68-1.696 1.68-2.932v-6a3.132 3.132 0 0 0-3.128-3.128H3.628A3.132 3.132 0 0 0 .5 7.69v6.006Z" />
                        </svg>
                        <span>Chat</span>
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
