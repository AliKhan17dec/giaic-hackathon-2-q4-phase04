"use client";

import EditTaskForm from "@/components/EditTaskForm";
import { use as useReact } from "react";

export default function EditTaskPage(props: { params: Promise<{ id: string }> | { id: string } }) {
    const params = props.params;
    const resolved = useReact(params as any) as { id: string };
    const id = resolved.id;
    return (
        <div className="flex w-full items-center justify-center">
            <EditTaskForm taskId={id} />
        </div>
    );
}
