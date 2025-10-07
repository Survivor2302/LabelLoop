<template>
  <main
    class="relative min-h-screen w-full overflow-hidden bg-gradient-to-b from-background to-muted/30"
  >
    <!-- Decorative background effects -->
    <GradientBackground />

    <div class="px-6 py-16 grid gap-y-12">
      <!-- Header -->
      <GradientCard class="mb-16">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">About LabelLoop</h1>
            <p class="mt-2 text-muted-foreground">Learn more about our mission and technology</p>
          </div>
          <RouterLink to="/">
            <Button variant="outline" size="lg"> ← Back to Home </Button>
          </RouterLink>
        </div>
      </GradientCard>

      <!-- Mission -->
      <div class="rounded-xl border bg-card p-8 shadow-sm mb-12">
        <h2 class="text-2xl font-semibold mb-4">Our Mission</h2>
        <p class="text-muted-foreground leading-relaxed mb-4">
          LabelLoop is designed to accelerate computer vision development through active learning.
          We believe that the process of labeling data and training models should be a continuous,
          collaborative loop rather than separate, disconnected steps.
        </p>
        <p class="text-muted-foreground leading-relaxed">
          By combining intuitive labeling tools with real-time model training, we help teams create
          high-quality datasets faster while continuously improving model performance.
        </p>
      </div>

      <!-- Key Features -->
      <div class="grid gap-6 sm:grid-cols-2 mb-12">
        <div class="rounded-xl border bg-card p-6 shadow-sm">
          <div class="mb-4 h-12 w-12 rounded-lg bg-emerald-500/10 flex items-center justify-center">
            <div class="h-6 w-6 rounded-full bg-emerald-500" />
          </div>
          <h3 class="text-lg font-semibold mb-2">Active Learning</h3>
          <p class="text-sm text-muted-foreground leading-relaxed">
            Our system learns from every label, prioritizing the most informative samples for
            annotation and accelerating dataset creation.
          </p>
        </div>

        <div class="rounded-xl border bg-card p-6 shadow-sm">
          <div class="mb-4 h-12 w-12 rounded-lg bg-violet-500/10 flex items-center justify-center">
            <div class="h-6 w-6 rounded-full bg-violet-500" />
          </div>
          <h3 class="text-lg font-semibold mb-2">Real-time Training</h3>
          <p class="text-sm text-muted-foreground leading-relaxed">
            Models update continuously as you label, providing increasingly accurate suggestions and
            reducing manual annotation effort.
          </p>
        </div>

        <div class="rounded-xl border bg-card p-6 shadow-sm">
          <div class="mb-4 h-12 w-12 rounded-lg bg-sky-500/10 flex items-center justify-center">
            <div class="h-6 w-6 rounded-full bg-sky-500" />
          </div>
          <h3 class="text-lg font-semibold mb-2">Team Collaboration</h3>
          <p class="text-sm text-muted-foreground leading-relaxed">
            Built for teams with role-based access, task assignment, and review workflows to ensure
            dataset quality at scale.
          </p>
        </div>

        <div class="rounded-xl border bg-card p-6 shadow-sm">
          <div class="mb-4 h-12 w-12 rounded-lg bg-amber-500/10 flex items-center justify-center">
            <div class="h-6 w-6 rounded-full bg-amber-500" />
          </div>
          <h3 class="text-lg font-semibold mb-2">Enterprise Ready</h3>
          <p class="text-sm text-muted-foreground leading-relaxed">
            Secure infrastructure, audit logs, and flexible deployment options for organizations of
            any size.
          </p>
        </div>
      </div>

      <!-- Tech Stack -->
      <div class="rounded-xl border bg-card p-8 shadow-sm">
        <h2 class="text-2xl font-semibold mb-6">Technology Stack</h2>
        <div class="grid gap-6 sm:grid-cols-3">
          <div>
            <h4 class="font-semibold mb-2 text-sm text-muted-foreground uppercase tracking-wide">
              Frontend
            </h4>
            <ul class="space-y-1 text-sm">
              <li>Vue.js 3 with TypeScript</li>
              <li>Vite for fast development</li>
              <li>Tailwind CSS for styling</li>
              <li>Pinia for state management</li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold mb-2 text-sm text-muted-foreground uppercase tracking-wide">
              Backend
            </h4>
            <ul class="space-y-1 text-sm">
              <li>FastAPI (Python)</li>
              <li>PostgreSQL database</li>
              <li>MinIO for object storage</li>
              <li>Docker for deployment</li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold mb-2 text-sm text-muted-foreground uppercase tracking-wide">
              ML Pipeline
            </h4>
            <ul class="space-y-1 text-sm">
              <li>PyTorch for training</li>
              <li>Active learning strategies</li>
              <li>Real-time inference</li>
              <li>Model versioning</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { GradientBackground, GradientCard } from '@/components'
import { Button } from '@/components/ui/button'
import { RouterLink } from 'vue-router'
</script>
