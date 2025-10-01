import { Button } from "@/components/ui/button";
import {
  GradientBackground,
  GradientCard,
  FeatureCard,
  StepCard,
  Stat,
  LiveChart,
} from "@/components";
import Link from "next/link";

export default function Home() {
  return (
    <main className="relative min-h-screen w-full overflow-hidden bg-gradient-to-b from-background to-muted/30">
      {/* Decorative background effects */}
      <GradientBackground />

      {/* Hero */}
      <div className="container mx-auto max-w-6xl px-6 py-12">
        <GradientCard className="mb-12">
          <div className="flex flex-col items-center gap-6 text-center">
            <span className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs text-muted-foreground backdrop-blur">
              <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />
              Active learning for vision datasets
            </span>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
              LabelLoop — Label smarter. Train as you go.
            </h1>
            <p className="max-w-2xl text-muted-foreground">
              Upload images, label collaboratively, and watch a model learn in
              real time. Each label improves suggestions for the next image —
              accelerating your path to production-quality datasets.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-3">
              <Button asChild size="lg">
                <Link href="/datasets">Get started with a dataset</Link>
              </Button>
            </div>
          </div>
        </GradientCard>
      </div>

      {/* Inline demo visual */}
      <section className="container mx-auto max-w-6xl px-6 pb-24">
        <div className="grid w-full gap-6 sm:grid-cols-2">
          {/* Left: live training chart */}
          <div className="relative rounded-xl border bg-card p-5 shadow-sm">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted-foreground">
                Model training signal
              </h3>
              <span className="rounded-md bg-emerald-500/10 px-2 py-1 text-xs text-emerald-600">
                online
              </span>
            </div>
            <LiveChart />
            <div className="mt-4 grid grid-cols-3 gap-3 text-left text-sm">
              <Stat label="mAP" value="37.4%" trend="up" />
              <Stat label="Latency" value="38ms" trend="down" />
              <Stat label="Images labeled" value="1,284" trend="up" />
            </div>
          </div>

          {/* Right: suggestion preview */}
          <div className="relative overflow-hidden rounded-xl border bg-card p-5 shadow-sm">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="text-sm font-medium text-muted-foreground">
                Smart suggestions
              </h3>
              <span className="rounded-md bg-violet-500/10 px-2 py-1 text-xs text-violet-600">
                improving
              </span>
            </div>
            <div className="relative aspect-[16/10] w-full rounded-lg border bg-muted">
              {/* Mock image */}
              <div className="absolute inset-0 bg-[url('/globe.svg')] bg-contain bg-center bg-no-repeat opacity-20" />
              {/* Mock boxes */}
              <div className="absolute left-[12%] top-[18%] h-[26%] w-[30%] animate-[pulse_2.2s_ease-in-out_infinite] rounded-md border-2 border-emerald-500/80 shadow-[0_0_0_3px_rgba(16,185,129,0.15)]" />
              <div className="absolute right-[16%] bottom-[14%] h-[28%] w-[34%] animate-[pulse_2.6s_ease-in-out_infinite] rounded-md border-2 border-sky-500/80 shadow-[0_0_0_3px_rgba(14,165,233,0.15)]" />
            </div>
            <p className="mt-3 text-sm text-muted-foreground">
              Receive bounding box proposals and labels as the model learns from
              your input.
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="container mx-auto max-w-6xl px-6 pb-24">
        <div className="mb-10 text-center">
          <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
            Why LabelLoop
          </h2>
          <p className="mx-auto mt-2 max-w-2xl text-muted-foreground">
            Everything you need to curate, label, and iterate on high-quality
            computer vision datasets.
          </p>
        </div>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <FeatureCard
            title="Collaborative labeling"
            desc="Assign tasks, review suggestions, and merge with confidence."
            color="emerald"
          />
          <FeatureCard
            title="Active learning"
            desc="Focus effort where it matters. The model guides the queue."
            color="violet"
          />
          <FeatureCard
            title="Versioned datasets"
            desc="Branch, compare, and track improvements over time."
            color="sky"
          />
          <FeatureCard
            title="Flexible exports"
            desc="COCO, YOLO, and custom schemas for your pipeline."
            color="amber"
          />
          <FeatureCard
            title="Keyboard-first UX"
            desc="Label at speed with thoughtful shortcuts and previews."
            color="rose"
          />
          <FeatureCard
            title="Secure & compliant"
            desc="Granular roles and audit trails for enterprise teams."
            color="slate"
          />
        </div>
      </section>

      {/* Workflow */}
      <section className="container mx-auto max-w-6xl px-6 pb-24">
        <div className="mb-8 text-center">
          <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
            From raw images to ready-to-train
          </h2>
          <p className="mx-auto mt-2 max-w-2xl text-muted-foreground">
            A simple loop that compounds: import, label, train, and ship.
          </p>
        </div>
        <ol className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <StepCard
            step="01"
            title="Import a dataset"
            desc="Upload images or connect cloud storage."
          />
          <StepCard
            step="02"
            title="Label together"
            desc="Use shortcuts and suggestions to move fast."
          />
          <StepCard
            step="03"
            title="Train continuously"
            desc="Model improves after every confirmed label."
          />
          <StepCard
            step="04"
            title="Export & deploy"
            desc="Push versions to your training pipeline."
          />
        </ol>
        <div className="mt-8 flex justify-center">
          <Button asChild size="lg">
            <Link href="/dashboard">Get started with a dataset</Link>
          </Button>
        </div>
      </section>

      {/* System Health Dashboard */}
      <section className="container mx-auto max-w-6xl px-6 pb-12">
        <div className="rounded-xl border bg-card p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold">System Health Dashboard</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                Monitor API, database, and S3 storage status in real-time
              </p>
            </div>
            <Button asChild variant="outline">
              <Link href="/dashboard">View Health Status</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* CTA Footer */}
      <section className="container mx-auto max-w-6xl px-6 pb-24">
        <GradientCard>
          <h3 className="text-2xl font-semibold tracking-tight">
            Ready to label smarter?
          </h3>
          <p className="mt-2 max-w-2xl text-muted-foreground">
            Kick off a project in minutes. Bring your images, invite your team,
            and let the loop do the heavy lifting.
          </p>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button asChild size="lg">
              <Link href="/dashboard">Create your first dataset</Link>
            </Button>
          </div>
        </GradientCard>
      </section>
    </main>
  );
}
