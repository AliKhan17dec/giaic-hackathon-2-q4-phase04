"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { API_URL } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  owner_id: number;
}

export default function EditTaskForm({ taskId }: { taskId: number }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [completed, setCompleted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { user, token, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!user || !token) {
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
        setTitle(data.title);
        setDescription(data.description || "");
        setCompleted(data.completed);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [user, token, router, logout, taskId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!user || !token) {
      setError("You must be logged in to edit a task.");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/api/${user.id}/tasks/${taskId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ title, description, completed }),
        },
      );

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to update task");
      }

      router.push("/tasks"); // Redirect to tasks list after updating
    } catch (err: any) {
      setError(err.message);
    }
  };

  if (loading) {
    return <div className="text-center">Loading task for editing...</div>;
  }

  if (error && error !== "Task not found.") {
    return <div className="text-center text-red-500">Error: {error}</div>;
  }

  return (
    <div className="card w-full max-w-md">
      <h2 className="mb-6 text-center text-2xl font-bold">Edit Task</h2>
      {error === "Task not found." ? (
        <p className="text-center text-red-500">{error}</p>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="title"
              className="block text-sm font-medium text-gray-700"
            >
              Title
            </label>
            <input
              type="text"
              id="title"
              className="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div>
            <label
              htmlFor="description"
              className="block text-sm font-medium text-gray-700"
            >
              Description (Optional)
            </label>
            <textarea
              id="description"
              rows={3}
              className="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            ></textarea>
          </div>
          <div className="flex items-center">
            <input
              type="checkbox"
              id="completed"
              className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              checked={completed}
              onChange={(e) => setCompleted(e.target.checked)}
            />
            <label
              htmlFor="completed"
              className="ml-2 block text-sm font-medium text-gray-700"
            >
              Completed
            </label>
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button type="submit" className="btn-primary w-full">
            Update Task
          </button>
        </form>
      )}
    </div>
  );
}
