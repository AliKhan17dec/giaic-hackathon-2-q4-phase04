"use client";

import { useState, useEffect, FormEvent } from "react";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import axios from "axios";

// Assuming these types are defined elsewhere or will be created
interface Message {
  role: "user" | "assistant" | "tool"; // Added 'tool' role
  content: string;
}

interface ChatResponse {
  ai_response: string;
  conversation_id: string; // UUID string
  tool_calls: { tool_name: string; tool_args: any }[]; // Detailed tool_calls structure
}

// New types for conversation history
interface ConversationHistoryMessage {
  id: string;
  conversation_id: string;
  role: "user" | "assistant" | "tool";
  content: string;
  tool_calls?: any[];
  created_at: string;
  updated_at: string;
}

interface ConversationHistory {
  id: string;
  user_id: string;
  created_at: string;
  updated_at: string;
  messages?: ConversationHistoryMessage[]; // Eager loaded messages
}


export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    try {
      const decoded: any = jwtDecode(token);
      const currentUserId = decoded.user_id;
      setUserId(currentUserId);
    } catch (e) {
      console.error("Failed to decode token:", e);
      router.push("/login");
    }
  }, [router]);

  // Effect to fetch conversation history
  useEffect(() => {
    if (!userId) return;

    const fetchConversationHistory = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          // No token available, skip conversation history
          setLoading(false);
          return;
        }

        const headers = { Authorization: `Bearer ${token}` };

        // Fetch conversations for the user
        const conversationsResponse = await axios.get<ConversationHistory[]>(
          `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/conversations`,
          { headers }
        );

        if (conversationsResponse.data.length > 0) {
          // Get the most recent conversation
          const latestConversation = conversationsResponse.data.sort(
            (a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
          )[0];
          setConversationId(latestConversation.id);

          // Fetch messages for the latest conversation
          const messagesResponse = await axios.get<ConversationHistoryMessage[]>(
            `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/conversations/${latestConversation.id}/messages`,
            { headers }
          );

          // Map fetched messages to local Message interface
          const loadedMessages: Message[] = messagesResponse.data.flatMap((msg) => {
            const msgs: Message[] = [{ role: msg.role, content: msg.content }];
            if (msg.tool_calls && msg.tool_calls.length > 0) {
              msg.tool_calls.forEach(call => {
                msgs.push({
                  role: "tool",
                  content: `Tool Call: ${call.tool_name}(${JSON.stringify(call.tool_args)})`
                });
              });
            }
            return msgs;
          });
          setMessages(loadedMessages);
        }
      } catch (err: any) {
        // Handle authentication and conversation history errors silently
        // This allows users to still use chat even if conversation history fails
        console.warn("Conversation history unavailable:", err?.response?.status || err?.message);
        setError(null);
      } finally {
        setLoading(false);
      }
    };

    fetchConversationHistory();
  }, [userId]);


  const sendMessage = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !userId) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("token");
      const response = await axios.post<ChatResponse>(
        `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`,
        {
          message: input,
          conversation_id: conversationId,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const aiResponseContent = response.data.ai_response;
      const toolCalls = response.data.tool_calls;
      const newMessages: Message[] = [];

      // Add AI's text response if available
      if (aiResponseContent) {
        newMessages.push({ role: "assistant", content: aiResponseContent });
      }

      // Add tool calls as messages if available
      if (toolCalls && toolCalls.length > 0) {
        toolCalls.forEach(call => {
          newMessages.push({
            role: "tool",
            content: `Tool Call: ${call.tool_name}(${JSON.stringify(call.tool_args)})`
          });
        });
      }

      setMessages((prev) => [...prev, ...newMessages]);
      setConversationId(response.data.conversation_id);
    } catch (err) {
      console.error("Error sending message:", err);
      setError("Failed to get response from AI. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (!userId) {
    return <div className="flex justify-center items-center h-screen">Loading user session...</div>;
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-white shadow p-4 text-center text-xl font-semibold">
        AI Chat Assistant
      </header>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"
              }`}
          >
            <div
              className={`max-w-xs px-4 py-2 rounded-lg shadow ${msg.role === "user"
                ? "bg-blue-500 text-white"
                : msg.role === "assistant"
                  ? "bg-gray-300 text-gray-800"
                  : "bg-purple-300 text-purple-800" // Style for tool calls
                }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="max-w-xs px-4 py-2 rounded-lg shadow bg-gray-300 text-gray-800">
              AI is thinking...
            </div>
          </div>
        )}
        {error && (
          <div className="text-red-500 text-center">{error}</div>
        )}
      </div>
      <form onSubmit={sendMessage} className="bg-white p-4 flex items-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 border rounded-lg p-2 mr-2 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          disabled={loading}
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        >
          Send
        </button>
      </form>
    </div>
  );
}