export function LiveChart() {
  // Simple animated line using stroke-dashoffset
  return (
    <div className="relative h-40 w-full">
      {/* 160px height */}
      <svg viewBox="0 0 400 160" className="h-full w-full">
        <defs>
          <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="hsl(var(--chart-1, 142_76%_36%))" />
            <stop offset="100%" stopColor="hsl(var(--chart-2, 221_83%_53%))" />
          </linearGradient>
        </defs>
        {/* Grid */}
        <g stroke="currentColor" className="text-muted-foreground/20">
          {Array.from({ length: 5 }).map((_, i) => (
            <line key={i} x1="0" x2="400" y1={i * 40} y2={i * 40} />
          ))}
        </g>
        {/* Path */}
        <path
          d="M0 130 C 50 110, 80 100, 110 120 S 170 150, 200 120 260 60, 300 85 350 115, 400 90"
          fill="none"
          stroke="url(#grad)"
          strokeWidth="3"
          pathLength={1}
          className="[stroke-dasharray:1] [stroke-dashoffset:1] motion-safe:animate-[dash_2.8s_ease-in-out_infinite]"
        />
      </svg>
      {/* Keyframes for the dash animation */}
      <style>{`
        @keyframes dash {
          0% { stroke-dashoffset: 1; }
          60% { stroke-dashoffset: 0; }
          100% { stroke-dashoffset: 0; }
        }
      `}</style>
    </div>
  );
}
