import { Button } from "@/components/ui/button";
import { GradientBackground, GradientCard, DatasetCard } from "@/components";
import Link from "next/link";

interface Dataset {
  id: number;
  title: string;
  description: string;
  imageCount: number;
  lastModified: string;
  status: "active" | "completed" | "paused";
  preview: string;
}

export default function DatasetsPage() {
  // Mock data for now
  //   const datasets: Dataset[] = [];
  const datasets: Dataset[] = [
    {
      id: 1,
      title: "Street Objects Detection",
      description:
        "Urban scene analysis with cars, pedestrians, and traffic signs",
      imageCount: 1250,
      lastModified: "2 hours ago",
      status: "active" as const,
      preview: "/globe.svg",
    },
    {
      id: 2,
      title: "Medical X-Ray Analysis",
      description: "Chest X-ray classification for pneumonia detection",
      imageCount: 890,
      lastModified: "1 day ago",
      status: "completed" as const,
      preview: "/globe.svg",
    },
    {
      id: 3,
      title: "Wildlife Monitoring",
      description: "Camera trap images for animal species identification",
      imageCount: 2100,
      lastModified: "3 days ago",
      status: "active" as const,
      preview: "/globe.svg",
    },
    {
      id: 4,
      title: "Product Quality Control",
      description: "Manufacturing defect detection in electronics",
      imageCount: 750,
      lastModified: "1 week ago",
      status: "paused" as const,
      preview: "/globe.svg",
    },
    {
      id: 5,
      title: "Satellite Imagery",
      description: "Land use classification from aerial photography",
      imageCount: 3200,
      lastModified: "2 weeks ago",
      status: "active" as const,
      preview: "/globe.svg",
    },
    {
      id: 6,
      title: "Food Recognition",
      description: "Restaurant menu item classification",
      imageCount: 1500,
      lastModified: "3 weeks ago",
      status: "completed" as const,
      preview: "/globe.svg",
    },
  ];

  return (
    <main className="relative min-h-screen w-full overflow-hidden bg-gradient-to-b from-background to-muted/30">
      {/* Decorative background effects */}
      <GradientBackground />

      <div className="container mx-auto max-w-6xl px-6 py-12">
        {/* Header */}
        <GradientCard className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
                Datasets
              </h1>
              <p className="mt-2 text-muted-foreground">
                Manage your image datasets and labeling projects
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Button asChild size="lg">
                <Link href="/datasets/upload">Upload Dataset</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="/">← Back to Home</Link>
              </Button>
            </div>
          </div>
        </GradientCard>

        {/* Datasets Section */}
        <div className="rounded-xl border bg-card shadow-sm">
          {/* Search and Filters */}
          <div className="border-b p-6">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex-1">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search datasets..."
                    className="w-full rounded-lg border border-input bg-background px-4 py-2 pl-10 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                  />
                  <svg
                    className="absolute left-3 top-2.5 h-4 w-4 text-muted-foreground"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                    />
                  </svg>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <select className="rounded-lg border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="paused">Paused</option>
                </select>
                <select className="rounded-lg border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
                  <option value="">Sort by</option>
                  <option value="name">Name</option>
                  <option value="modified">Last Modified</option>
                  <option value="images">Image Count</option>
                </select>
              </div>
            </div>
          </div>

          {/* Datasets Grid */}
          <div className="p-6">
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {datasets.map((dataset) => (
                <DatasetCard key={dataset.id} dataset={dataset} />
              ))}
            </div>
          </div>

          {/* Empty State (hidden for now since we have data) */}
          {datasets.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16 text-center">
              <div className="mb-4 rounded-full bg-muted p-6">
                <svg
                  className="h-12 w-12 text-muted-foreground"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <h3 className="text-lg font-semibold">No datasets found</h3>
              <p className="mt-2 text-muted-foreground">
                Get started by uploading your first dataset
              </p>
              <Button asChild className="mt-4">
                <Link href="/datasets/upload">Upload Dataset</Link>
              </Button>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
