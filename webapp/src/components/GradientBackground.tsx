export function GradientBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 -z-10">
      <div className="absolute left-1/2 top-[-10%] h-[40rem] w-[40rem] -translate-x-1/2 rounded-full bg-[radial-gradient(circle_at_center,theme(colors.violet.500/.25),transparent_60%)] blur-3xl" />
      <div className="absolute right-[-10%] bottom-[-10%] h-[30rem] w-[30rem] rounded-full bg-[radial-gradient(circle_at_center,theme(colors.sky.500/.25),transparent_60%)] blur-3xl" />
    </div>
  );
}
