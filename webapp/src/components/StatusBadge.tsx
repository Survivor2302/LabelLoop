interface StatusBadgeProps {
  status?: "ok" | "error";
  variant?: "default" | "healthy" | "error";
}

export function StatusBadge({ status, variant = "default" }: StatusBadgeProps) {
  if (variant === "healthy") {
    return (
      <span className="px-2 py-0.5 rounded-full text-xs bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">
        Healthy
      </span>
    );
  }

  if (variant === "error") {
    return (
      <span className="px-2 py-0.5 rounded-full text-xs bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300">
        Error
      </span>
    );
  }

  if (status === "ok") {
    return (
      <span className="px-2 py-0.5 rounded-full text-xs bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">
        Healthy
      </span>
    );
  }

  if (status === "error") {
    return (
      <span className="px-2 py-0.5 rounded-full text-xs bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300">
        Error
      </span>
    );
  }

  return null;
}
