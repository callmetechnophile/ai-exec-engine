import { CheckCircle2, Circle, Loader2 } from "lucide-react";

export default function AgentActivityTimeline({ currentState, logs }: { currentState: string, logs: string[] }) {
  const agents = [
    "Initializing",
    "Retrieval Agent",
    "Extraction Agent",
    "Research Agent",
    "Optimization Agent",
    "Validation Agent",
    "Simulation Agent",
    "Deployment Agent",
    "Planning Agent",
    "Complete"
  ];
  
  const currentIndex = agents.indexOf(currentState);

  return (
    <div className="w-full flex flex-col gap-6 bg-card/50 p-6 rounded-xl border border-border/50">
      <h3 className="text-xl font-bold">Autonomous Agent Pipeline</h3>
      
      {/* Horizontal Pipeline */}
      <div className="flex justify-between items-center relative w-full px-4 overflow-hidden">
        <div className="absolute top-1/2 left-0 right-0 h-1 bg-muted -z-10 -translate-y-1/2" />
        {agents.map((agent, idx) => {
          const isPast = idx < currentIndex;
          const isCurrent = idx === currentIndex;
          const isFuture = idx > currentIndex;
          
          return (
            <div key={idx} className="flex flex-col items-center gap-2 bg-background p-2 rounded-full z-10">
              {isPast ? (
                <CheckCircle2 className="h-6 w-6 text-emerald-400 bg-background rounded-full" />
              ) : isCurrent ? (
                <Loader2 className="h-6 w-6 animate-spin text-purple-400 bg-background rounded-full" />
              ) : (
                <Circle className="h-6 w-6 text-muted-foreground bg-background rounded-full" />
              )}
              <span className={`text-[10px] md:text-xs font-semibold uppercase tracking-wider ${isCurrent ? "text-purple-400" : isPast ? "text-emerald-400" : "text-muted-foreground"}`}>
                {agent.replace(" Agent", "")}
              </span>
            </div>
          );
        })}
      </div>
      
      {/* Live Logs Console */}
      <div className="bg-black/80 rounded-md p-4 mt-4 h-48 overflow-y-auto border border-border">
        <div className="flex flex-col gap-1">
          {logs.map((log, i) => (
            <div key={i} className="text-xs font-mono text-green-400">
              <span className="text-gray-500 mr-2">[{new Date().toLocaleTimeString()}]</span>
              {log}
            </div>
          ))}
          {currentState !== "Complete" && currentState !== "ERROR" && (
            <div className="text-xs font-mono text-green-400/50 animate-pulse">_</div>
          )}
        </div>
      </div>
    </div>
  );
}
