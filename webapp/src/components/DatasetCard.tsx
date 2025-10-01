import Link from "next/link";

interface Dataset {
  id: number;
  title: string;
  description: string;
  imageCount: number;
  lastModified: string;
  status: "active" | "completed" | "paused";
  preview: string;
}

interface DatasetCardProps {
  dataset: Dataset;
}

export function DatasetCard({ dataset }: DatasetCardProps) {
  const statusColors = {
    active:
      "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
    completed:
      "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
    paused:
      "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300",
  };

  const statusLabels = {
    active: "Active",
    completed: "Completed",
    paused: "Paused",
  };

  return (
    <Link href={`/datasets/${dataset.id}`}>
      <div className="group relative overflow-hidden rounded-xl border bg-card shadow-sm transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
        {/* Preview Image */}
        <div className="relative aspect-[16/10] w-full overflow-hidden bg-muted">
          <div
            className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-60 transition-opacity duration-300 group-hover:opacity-80"
            style={{ backgroundImage: `url(${dataset.preview})` }}
          />
          {/* Overlay gradient */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent" />

          {/* Status badge */}
          <div className="absolute right-3 top-3">
            <span
              className={`px-2 py-1 rounded-full text-xs font-medium ${
                statusColors[dataset.status]
              }`}
            >
              {statusLabels[dataset.status]}
            </span>
          </div>

          {/* Hover overlay */}
          <div className="absolute inset-0 bg-black/0 transition-colors duration-300 group-hover:bg-black/10" />
        </div>

        {/* Content */}
        <div className="p-4">
          <h3 className="font-semibold text-sm leading-tight group-hover:text-primary transition-colors duration-200">
            {dataset.title}
          </h3>
          <p className="mt-1 text-xs text-muted-foreground line-clamp-2">
            {dataset.description}
          </p>

          {/* Stats */}
          <div className="mt-3 flex items-center justify-between text-xs text-muted-foreground">
            <div className="flex items-center gap-1">
              <svg
                className="h-3 w-3"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <span>{dataset.imageCount.toLocaleString()} images</span>
            </div>
            <span>{dataset.lastModified}</span>
          </div>
        </div>

        {/* Hover effect border */}
        <div className="absolute inset-0 rounded-xl border-2 border-transparent transition-colors duration-300 group-hover:border-primary/20" />
      </div>
    </Link>
  );
}
