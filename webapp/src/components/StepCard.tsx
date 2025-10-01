interface StepCardProps {
  step: string;
  title: string;
  desc: string;
}

export function StepCard({ step, title, desc }: StepCardProps) {
  return (
    <li className="relative rounded-xl border bg-card p-6 shadow-sm">
      <span className="mb-2 inline-flex h-8 w-8 items-center justify-center rounded-md border text-xs font-medium text-muted-foreground">
        {step}
      </span>
      <h4 className="text-sm font-semibold">{title}</h4>
      <p className="mt-1 text-sm text-muted-foreground">{desc}</p>
    </li>
  );
}
