interface FeatureCardProps {
  title: string;
  desc: string;
  color: "emerald" | "violet" | "sky" | "amber" | "rose" | "slate";
}

export function FeatureCard({ title, desc, color }: FeatureCardProps) {
  const colorMap: Record<typeof color, string> = {
    emerald: "from-emerald-500/10",
    violet: "from-violet-500/10",
    sky: "from-sky-500/10",
    amber: "from-amber-500/10",
    rose: "from-rose-500/10",
    slate: "from-slate-500/10",
  } as const;

  return (
    <div className="group relative overflow-hidden rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-md">
      <div
        className={`pointer-events-none absolute inset-0 -z-10 bg-gradient-to-br ${colorMap[color]} to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100`}
      />
      <h3 className="text-base font-semibold">{title}</h3>
      <p className="mt-2 text-sm text-muted-foreground">{desc}</p>
    </div>
  );
}
