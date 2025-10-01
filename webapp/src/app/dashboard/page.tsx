"use client";

import { useHealthQuery } from "@/lib/redux/services/health/health.service";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { GradientBackground, GradientCard, StatusBadge } from "@/components";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const { data: healthData, error, isLoading, refetch } = useHealthQuery();
  const [timeUntilRefresh, setTimeUntilRefresh] = useState(30);

  // Auto-refetch every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      refetch();
      setTimeUntilRefresh(30);
    }, 30000);

    return () => clearInterval(interval);
  }, [refetch]);

  // Countdown timer
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeUntilRefresh((prev) => {
        if (prev <= 1) {
          return 30; // Reset to 30 when it reaches 0
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const overallColor = isLoading
    ? "bg-yellow-500"
    : error
    ? "bg-red-500"
    : healthData?.status === "ok"
    ? "bg-green-500"
    : "bg-yellow-500"; // degraded

  const overallText = isLoading
    ? "Checking services..."
    : error
    ? "Service unavailable"
    : healthData?.status === "ok"
    ? "All systems operational"
    : "Service degraded";

  // Get components in a specific order for consistent display
  const componentOrder = ["db", "api", "s3"];
  const components = componentOrder
    .map((key) => ({ key, component: healthData?.components?.[key] }))
    .filter(({ component }) => component !== undefined);

  const indicatorColor = (status?: "ok" | "error") =>
    status === "ok" ? "bg-green-500" : "bg-red-500";

  const getComponentDisplayName = (key: string) => {
    const displayNames: Record<string, string> = {
      db: "Database",
      api: "API",
      s3: "S3 Storage",
    };
    return displayNames[key] || key.toUpperCase();
  };

  return (
    <main className="relative min-h-screen w-full overflow-hidden bg-gradient-to-b from-background to-muted/30">
      {/* Decorative background effects */}
      <GradientBackground />

      <div className="container mx-auto max-w-6xl px-6 py-12">
        {/* Header */}
        <GradientCard className="mb-12">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                System Health Dashboard
              </h1>
              <p className="mt-2 text-muted-foreground">
                Monitor API, database, and S3 storage status in real-time
              </p>
            </div>
            <Link href="/">
              <Button variant="outline" size="lg">
                ← Back to Home
              </Button>
            </Link>
          </div>
        </GradientCard>

        {/* Health Status Card */}
        <div className="rounded-xl border bg-card shadow-sm">
          <div className="p-6 border-b">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div
                  className={`w-3 h-3 rounded-full ${overallColor} animate-pulse`}
                />
                <h2 className="text-xl font-semibold">{overallText}</h2>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-sm text-muted-foreground">
                  Next check in{" "}
                  <span className="font-mono font-medium text-blue-600 dark:text-blue-400">
                    {timeUntilRefresh}s
                  </span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    refetch();
                    setTimeUntilRefresh(30);
                  }}
                  disabled={isLoading}
                >
                  {isLoading ? "Checking..." : "Refresh"}
                </Button>
              </div>
            </div>
          </div>

          <div className="p-6">
            {error && (
              <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 dark:border-red-800 dark:bg-red-900/20">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-red-500" />
                  <span className="text-sm font-medium text-red-600 dark:text-red-400">
                    Connection Error
                  </span>
                </div>
                <p className="mt-1 text-sm text-red-600 dark:text-red-400">
                  {typeof error === "object" &&
                  error !== null &&
                  "message" in error
                    ? (error as { message?: string }).message ?? "Unknown error"
                    : "Unable to contact the service"}
                </p>
              </div>
            )}

            <Accordion
              type="single"
              collapsible
              defaultValue="components"
              className="w-full"
            >
              <AccordionItem value="components" className="border-0">
                <AccordionTrigger className="px-0 py-4 hover:no-underline">
                  <div className="flex items-center justify-between w-full">
                    <div className="flex items-center gap-3">
                      <div className={`w-3 h-3 rounded-full ${overallColor}`} />
                      <span className="font-medium">Service Components</span>
                    </div>
                    {healthData && (
                      <div>
                        {healthData.status === "ok" ? (
                          <span className="px-2 py-0.5 rounded-full text-xs bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">
                            All Healthy
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded-full text-xs bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300">
                            Issues Detected
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </AccordionTrigger>
                <AccordionContent className="px-0 pb-4">
                  <div className="space-y-4 pt-2">
                    {components.map(({ key, component }) => (
                      <div key={key} className="group">
                        <div className="flex items-start justify-between gap-4 p-4 rounded-lg border bg-muted/30 transition-colors group-hover:bg-muted/50">
                          <div className="flex items-center gap-3 min-w-0">
                            <div
                              className={`w-2.5 h-2.5 rounded-full ${
                                isLoading
                                  ? "bg-yellow-500 animate-pulse"
                                  : error
                                  ? "bg-red-500"
                                  : indicatorColor(component?.status)
                              }`}
                            />
                            <div className="flex flex-col">
                              <span className="text-sm font-medium">
                                {getComponentDisplayName(key)}
                              </span>
                              <div className="text-xs text-muted-foreground flex items-center gap-3">
                                {typeof component?.latency_ms === "number" && (
                                  <span className="flex items-center gap-1">
                                    <span className="h-1 w-1 rounded-full bg-muted-foreground" />
                                    {component.latency_ms.toFixed(0)}ms
                                  </span>
                                )}
                                {component?.message && (
                                  <span className="truncate max-w-xs">
                                    {component.message}
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>
                          <StatusBadge status={component?.status} />
                        </div>
                      </div>
                    ))}
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-8 rounded-xl border bg-card p-6 shadow-sm">
          <h3 className="text-lg font-semibold mb-3">About This Dashboard</h3>
          <p className="text-sm text-muted-foreground">
            This dashboard monitors the health of LabelLoop&apos;s core
            infrastructure components. The system automatically checks API
            endpoints, database connectivity, and S3 storage availability every
            30 seconds to ensure optimal performance for your labeling
            workflows.
          </p>
        </div>
      </div>
    </main>
  );
}
