<template>
  <main
    class="relative min-h-screen w-full overflow-hidden bg-gradient-to-b from-background to-muted/30"
  >
    <!-- Decorative background effects -->
    <GradientBackground />

    <div class="px-6 py-16 grid gap-y-8">
      <!-- Hero -->
      <div class="px-6 py-6">
        <GradientCard class="mb-12">
          <div class="flex flex-col items-center gap-6 text-center">
            <span
              class="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs text-muted-foreground backdrop-blur"
            >
              <span class="h-2 w-2 animate-pulse rounded-full bg-emerald-500" />
              Active learning for vision datasets
            </span>
            <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">
              LabelLoop — Label smarter. Train as you go.
            </h1>
            <p class="max-w-2xl text-muted-foreground">
              Upload images, label collaboratively, and watch a model learn in real time. Each label
              improves suggestions for the next image — accelerating your path to production-quality
              datasets.
            </p>
            <div class="flex flex-wrap items-center justify-center gap-3">
              <Button as-child variant="outline" size="lg">
                <RouterLink to="/datasets">Get started with a dataset</RouterLink>
              </Button>
            </div>
          </div>
        </GradientCard>
      </div>

      <!-- System Health Dashboard -->
      <section class="px-6">
        <div class="border bg-card p-6">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <h3 class="text-lg font-semibold">System Health Dashboard</h3>
              <p class="mt-1 text-sm text-muted-foreground">
                Monitor API, database, and S3 storage status in real-time
              </p>
            </div>
            <Button as-child size="lg" variant="outline">
              <RouterLink to="/dashboard">View Health Status</RouterLink>
            </Button>
          </div>
        </div>
      </section>

      <!-- Inline demo visual -->
      <section class="px-6 pb-12">
        <div class="grid w-full gap-6 sm:grid-cols-2">
          <!-- Left: live training chart -->
          <div class="relative border bg-card p-8">
            <div class="mb-6 flex items-center justify-between">
              <h3 class="text-base font-medium">Model training signal</h3>
              <span class="rounded-md bg-emerald-500/10 px-2 py-1 text-xs text-emerald-600">
                online
              </span>
            </div>
            <div class="h-full flex flex-col justify-center">
              <div class="mb-6">
                <LiveChart />
              </div>
              <div class="grid grid-cols-3 gap-6 text-left text-sm">
                <Stat label="mAP" value="37.4%" trend="up" />
                <Stat label="Latency" value="38ms" trend="down" />
                <Stat label="Images labeled" value="1,284" trend="up" />
              </div>
            </div>
          </div>

          <!-- Right: suggestion preview -->
          <div class="relative overflow-hidden border bg-card p-8">
            <div class="mb-6 flex items-center justify-between">
              <h3 class="text-base font-medium">Smart suggestions</h3>
              <span class="rounded-md bg-violet-500/10 px-2 py-1 text-xs text-violet-600">
                improving
              </span>
            </div>
            <div class="relative aspect-[16/10] w-full border bg-muted mb-6">
              <!-- Mock image -->
              <div
                class="absolute inset-0 bg-[url('/globe.svg')] bg-contain bg-center bg-no-repeat opacity-20"
              />
              <!-- Mock boxes -->
              <div
                class="absolute left-[12%] top-[18%] h-[26%] w-[30%] animate-[pulse_2.2s_ease-in-out_infinite] rounded-md border-2 border-emerald-500/80 shadow-[0_0_0_3px_rgba(16,185,129,0.15)]"
              />
              <div
                class="absolute right-[16%] bottom-[14%] h-[28%] w-[34%] animate-[pulse_2.6s_ease-in-out_infinite] rounded-md border-2 border-sky-500/80 shadow-[0_0_0_3px_rgba(14,165,233,0.15)]"
              />
            </div>
            <p class="text-sm text-muted-foreground">
              Receive bounding box proposals and labels as the model learns from your input.
            </p>
          </div>
        </div>
      </section>

      <!-- Features -->
      <section class="px-6 pb-12 grid gap-y-4">
        <div class="mb-8 text-center">
          <h2 class="text-2xl font-semibold tracking-tight sm:text-3xl">Why LabelLoop</h2>
          <p class="mx-auto mt-2 max-w-2xl text-muted-foreground">
            Everything you need to curate, label, and iterate on high-quality computer vision
            datasets.
          </p>
        </div>
        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
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

      <!-- Workflow -->
      <section class="px-6 pb-12 grid gap-y-4">
        <div class="mb-8 text-center">
          <h2 class="text-2xl font-semibold tracking-tight sm:text-3xl">
            From raw images to ready-to-train
          </h2>
          <p class="mx-auto mt-2 max-w-2xl text-muted-foreground">
            A simple loop that compounds: import, label, train, and ship.
          </p>
        </div>
        <ol class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
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
        <div class="mt-8 flex justify-center">
          <Button as-child size="lg" variant="outline">
            <RouterLink to="/dashboard">Get started with a dataset</RouterLink>
          </Button>
        </div>
      </section>

      <!-- CTA Footer -->
      <section class="px-6 pb-16">
        <GradientCard>
          <h3 class="text-2xl font-semibold tracking-tight">Ready to label smarter?</h3>
          <p class="mt-2 max-w-2xl text-muted-foreground">
            Kick off a project in minutes. Bring your images, invite your team, and let the loop do
            the heavy lifting.
          </p>
          <div class="mt-6 flex flex-wrap gap-3">
            <Button as-child variant="outline" size="lg">
              <RouterLink to="/dashboard">Create your first dataset</RouterLink>
            </Button>
          </div>
        </GradientCard>
      </section>
    </div>
  </main>
</template>

<script setup lang="ts">
import {
  GradientBackground,
  GradientCard,
  FeatureCard,
  StepCard,
  Stat,
  LiveChart,
} from '@/components'
import { Button } from '@/components/ui/button'
import { RouterLink } from 'vue-router'
</script>
