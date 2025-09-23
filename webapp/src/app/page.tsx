import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-6 p-8">
      <h1 className="text-3xl sm:text-4xl font-bold tracking-tight">
        Bienvenue 👋
      </h1>
      <p className="text-center text-muted-foreground max-w-xl">
        Ceci est une page d&apos;accueil très simple pour démarrer rapidement.
      </p>
      <div className="flex items-center gap-3">
        <Button asChild>
          <Link href="/dashboard">Commencer</Link>
        </Button>
      </div>
    </main>
  );
}
