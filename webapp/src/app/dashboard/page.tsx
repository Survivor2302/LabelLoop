"use client";

import { useHealthQuery } from "@/lib/redux/services/health/health.service";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const { data: healthData, error, isLoading, refetch } = useHealthQuery();
  const [timeUntilRefresh, setTimeUntilRefresh] = useState(30);

  useEffect(() => {
    console.log(JSON.stringify(healthData, null, 2));
  }, [healthData]);

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
    ? "Vérification en cours..."
    : error
    ? "Service indisponible"
    : healthData?.status === "ok"
    ? "Service opérationnel"
    : "Service dégradé";

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
      s3: "S3",
    };
    return displayNames[key] || key.toUpperCase();
  };

  const statusBadge = (status?: "ok" | "error") => {
    if (status === "ok") {
      return (
        <span className="px-2 py-0.5 rounded-full text-xs bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">
          OK
        </span>
      );
    }
    if (status === "error") {
      return (
        <span className="px-2 py-0.5 rounded-full text-xs bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300">
          Erreur
        </span>
      );
    }
    return null;
  };

  return (
    <main className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <Link href="/">
            <Button variant="outline">← Retour</Button>
          </Link>
        </div>

        <div className="grid gap-6">
          <div className="rounded-xl border bg-white dark:bg-neutral-900 shadow-sm">
            <div className="p-6 border-b flex items-center justify-between">
              <h2 className="text-xl font-semibold">Service Health</h2>
              <div className="flex items-center gap-3">
                <div className="text-sm text-muted-foreground">
                  Prochaine vérification dans{" "}
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
                  {isLoading ? "Vérification..." : "Actualiser"}
                </Button>
              </div>
            </div>

            <div className="p-4">
              {error && (
                <div className="mb-4 bg-red-50 dark:bg-red-900/20 p-3 rounded text-sm text-red-600 dark:text-red-400">
                  <strong>Erreur:</strong>{" "}
                  {typeof error === "object" &&
                  error !== null &&
                  "message" in error
                    ? (error as { message?: string }).message ??
                      "Erreur inconnue"
                    : "Impossible de contacter le service"}
                </div>
              )}

              <Accordion
                type="single"
                collapsible
                defaultValue="components"
                className="w-full rounded-lg border"
              >
                <AccordionItem value="components">
                  <AccordionTrigger className="px-4 py-3">
                    <div className="flex items-center justify-between w-full">
                      <div className="flex items-center gap-3">
                        <div
                          className={`w-3 h-3 rounded-full ${overallColor}`}
                        />
                        <span className="font-medium">{overallText}</span>
                      </div>
                      {healthData && (
                        <div>
                          {healthData.status === "ok" ? (
                            <span className="px-2 py-0.5 rounded-full text-xs bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300">
                              OK
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded-full text-xs bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300">
                              Dégradé
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="px-4 pb-4">
                    <div className="space-y-5 pt-2">
                      {components.map(({ key, component }, index) => (
                        <div key={key}>
                          <div className="flex items-start justify-between gap-4">
                            <div className="flex items-center gap-3 min-w-0">
                              <div
                                className={`w-2.5 h-2.5 rounded-full ${
                                  isLoading
                                    ? "bg-yellow-500"
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
                                  {typeof component?.latency_ms ===
                                    "number" && (
                                    <span>
                                      {component.latency_ms.toFixed(0)} ms
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
                            {statusBadge(component?.status)}
                          </div>
                          {index < components.length - 1 && (
                            <div className="h-px bg-border mt-5" />
                          )}
                        </div>
                      ))}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
