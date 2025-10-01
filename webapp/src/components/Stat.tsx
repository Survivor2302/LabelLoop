interface StatProps {
  label: string;
  value: string;
  trend: "up" | "down";
}

export function Stat({ label, value, trend }: StatProps) {
  const color = trend === "up" ? "text-emerald-600" : "text-rose-600";
  const arrow = trend === "up" ? "▲" : "▼";

  return (
    <div className="rounded-lg border bg-background p-3">
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <span>{label}</span>
        <span className={color}>{arrow}</span>
      </div>
      <div className="mt-1 text-lg font-semibold">{value}</div>
    </div>
  );
}
