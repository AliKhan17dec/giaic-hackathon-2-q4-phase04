"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Link from "next/link";
import { API_URL } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  owner_id: number;
}

export default function TaskPage({ params }: { params: { id: string } }) {
  const { user, token, logout, initialized } = useAuth();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const taskId = params.id;

  const handleComplete = async () => {
    if (!user || !token || !task) {
      setError("You must be logged in to update a task.");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${API_URL}/api/${user.id}/tasks/${taskId}/complete`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        },
      );

      if (response.status === 401 || response.status === 403) {
        logout();
        return;
      }

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to mark task as complete");
      }

      const updatedTask: Task = await response.json();
      setTask(updatedTask);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!user || !token) {
      setError("You must be logged in to delete a task.");
      return;
    }

    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/api/${user.id}/tasks/${taskId}`,
        {
          method: "DELETE",
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
        throw new Error(errData.detail || "Failed to delete task");
      }

      router.push("/tasks");
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    if (!initialized) return;

    if (!token || !user) {
      router.push("/login");
      return;
    }

    const fetchTask = async () => {
      try {
        const response = await fetch(
          `${API_URL}/api/${user.id}/tasks/${taskId}`,
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

        if (response.status === 404) {
          setError("Task not found.");
          return;
        }

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || "Failed to fetch task");
        }

        const data: Task = await response.json();
        setTask(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [initialized, user, token, router, logout, taskId]);

  if (loading) {
    return <div className="text-center">Loading task details...</div>;
  }

  if (error) {
    return <div className="text-center text-red-500">Error: {error}</div>;
  }

  if (!task) {
    return (
      <div className="flex w-full items-center justify-center">
        <div className="card w-full max-w-md text-center">
          <p className="text-lg font-semibold">Task not found.</p>
          <Link href="/tasks" className="mt-4 inline-block text-blue-900 hover:underline">
            Go to Task List
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full flex items-center justify-center">
      <div className="card w-full max-w-md">
        <h2 className="mb-6 text-center text-3xl font-bold">Task Details</h2>
        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium text-gray-700">Title:</p>
            <p className="text-lg text-gray-900">{task.title}</p>
          </div>
          {task.description && (
            <div>
              <p className="text-sm font-medium text-gray-700">Description:</p>
              <p className="text-gray-900">{task.description}</p>
            </div>
          )}
          <div>
            <p className="text-sm font-medium text-gray-700">Status:</p>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="completed-status"
                className="h-4 w-4 rounded border-gray-300 text-blue-900 focus:ring-blue-500"
                checked={task.completed}
                onChange={handleComplete}
                disabled={loading}
              />
              <label htmlFor="completed-status" className="text-lg font-semibold text-gray-900">
                {task.completed ? "Completed" : "Pending"}
              </label>
            </div>
          </div>
          <Link href="/tasks" className="mt-6 inline-block text-blue-900 hover:underline">
            Back to Task List
          </Link>
          <div className="mt-4 flex items-center space-x-2">
            <button
              onClick={handleDelete}
              className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
            >
              Delete Task
            </button>
            <Link href={`/tasks/edit/${taskId}`} className="btn-primary">
              Edit Task
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
