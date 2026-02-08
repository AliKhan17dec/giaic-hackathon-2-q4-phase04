"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { API_URL } from "@/lib/api";
import { formatError } from "@/lib/formatError";

export default function NewTaskForm() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const { user, token } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!user || !token) {
      setError("You must be logged in to create a task.");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/api/${user.id}/tasks`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ title, description }),
        },
      );

      if (!response.ok) {
        let errText = "Failed to create task";
        try {
          const errData = await response.json();
          if (typeof errData === "string") errText = errData;
          else if (errData && typeof errData.detail === "string") errText = errData.detail;
          else if (errData && errData.detail && typeof errData.detail.message === "string") errText = errData.detail.message;
          else errText = JSON.stringify(errData);
        } catch {
          /* ignore JSON parse error */
        }
        throw new Error(errText);
      }

      setTitle("");
      setDescription("");
      router.push("/tasks"); // Redirect to tasks list after creating
    } catch (err: any) {
      console.error("Failed to create task:", err);
      setError(formatError(err));
    }
  };

  return (
    <div className="card w-full max-w-md">
      <h2 className="mb-6 text-center text-2xl font-bold">Create New Task</h2>
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
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button type="submit" className="btn-primary w-full">
          Create Task
        </button>
      </form>
    </div>
  );
}
