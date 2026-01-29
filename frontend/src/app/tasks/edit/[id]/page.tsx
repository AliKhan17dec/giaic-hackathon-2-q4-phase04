"use client";

import EditTaskForm from "@/components/EditTaskForm";

export default function EditTaskPage({ params }: { params: { id: string } }) {
    const id = Number(params.id);
    return (
        <div className="flex w-full items-center justify-center">
            <EditTaskForm taskId={id} />
        </div>
    );
}
