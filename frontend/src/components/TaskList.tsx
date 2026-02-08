"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { API_URL } from "@/lib/api";
import { formatError } from "@/lib/formatError";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
}

export default function TaskList() {
  const { user, token, logout, initialized } = useAuth();
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Wait until AuthProvider has finished initializing (reading localStorage)
    if (!initialized) return;

    if (!token || !user) {
      router.push("/login");
      return;
    }

    const fetchTasks = async () => {
      try {
        const response = await fetch(
          `${API_URL}/api/${user.id}/tasks`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );

        if (response.status === 401 || response.status === 403) {
          logout();
          return;
        }

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || "Failed to fetch tasks");
        }

        const data: Task[] = await response.json();
        setTasks(data);
      } catch (err: any) {
        console.error("Failed to fetch tasks:", err);
        setError(formatError(err));
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [user, token, router, logout]);

  if (loading) {
    return <div className="text-center">Loading tasks...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500">Error: {error}</div>;
  }

  return (
    <div className="card w-full max-w-2xl">
      <h2 className="mb-6 text-center text-3xl font-bold">Your Tasks</h2>
      <button onClick={() => router.push("/tasks/new")} className="btn-primary mb-4 w-full">
        Create New Task
      </button>
      {tasks.length === 0 ? (
        <p className="text-center text-gray-600">No tasks found. Create one!</p>
      ) : (
        <ul className="space-y-4">
          {tasks.map((task) => (
            <li
              key={task.id}
              className="flex items-center justify-between rounded-md border border-gray-200 p-4 shadow-sm"
            >
              <div>
                <h3
                  className={`text-lg font-semibold ${task.completed ? "line-through text-gray-500" : "text-gray-800"
                    }`}
                >
                  {task.title}
                </h3>
                {task.description && (
                  <p className="text-sm text-gray-600">{task.description}</p>
                )}
              </div>
              <div className="flex space-x-2">
                <button onClick={() => router.push(`/tasks/${task.id}`)} className="rounded-md bg-blue-900 px-3 py-1 text-sm text-white hover:bg-blue-800">
                  View
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
