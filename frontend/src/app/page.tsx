import Link from "next/link";

export default function Home() {
  return (
    <section className="flex min-h-[70vh] items-center justify-center">
      <div className="card w-full max-w-4xl">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-extrabold">Organize work, ship faster</h1>
            <p className="mt-2 text-gray-600">A lightweight multi-user todo app — secure, fast, and designed for teams.</p>

            <div className="mt-6 flex flex-wrap gap-3">
              <Link href="/signup" className="btn-primary">
                Get Started
              </Link>
              <Link href="/tasks" className="inline-flex items-center justify-center rounded-md border border-gray-200 px-4 py-2 text-gray-700 hover:bg-gray-50">
                View Tasks
              </Link>
            </div>
          </div>

          <div className="mt-6 md:mt-0 w-full md:w-1/3">
            <div className="rounded-md border border-gray-100 bg-blue-50 p-4 text-sm text-gray-700">
              <strong>Tip:</strong> Use the Tasks page to create, edit and share progress.
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
