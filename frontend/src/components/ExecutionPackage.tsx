import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Download, CheckCircle2, Info, AlertTriangle, Cpu, Server, History, Activity } from "lucide-react";
import FrappeGantt from "@/components/gantt/FrappeGantt";
import AgentActivityTimeline from "./AgentActivityTimeline";
import ValidationPanel from "./ValidationPanel";

export default function ExecutionPackage({ query, budget, complexity, time }: any) {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [state, setState] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (taskId && state?.status !== "DONE" && state?.status !== "ERROR") {
      interval = setInterval(async () => {
        try {
          const res = await fetch(`http://localhost:8000/api/orchestrator-status/${taskId}`);
          const data = await res.json();
          setState(data);
        } catch (e) {
          console.error("Polling error", e);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [taskId, state?.status]);

  const handleGenerate = async () => {
    setTaskId(null);
    setState({ current_agent: "Initializing", status: "RUNNING", logs: ["Initializing multi-agent orchestrator..."] });
    setErrorMsg("");
    try {
      const payload = { query, budget, complexity, time };
      const res = await fetch("http://localhost:8000/api/start-orchestrator", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Failed to start orchestrator");
      setTaskId(data.task_id);
    } catch (err: any) {
      setErrorMsg(err.message);
      setState(null);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-emerald-400";
    if (score >= 50) return "text-yellow-400";
    return "text-destructive";
  };

  const downloadFile = (path: string) => {
    if (!path) return;
    const filename = path.split('/').pop();
    const type = path.split('/')[1];
    window.open(`http://localhost:8000/api/export/${type}/${filename}`, "_blank");
  };

  if (!state && !taskId) {
    return (
      <div className="w-full flex flex-col items-center border-t border-border/50 pt-16 mt-8">
        <h2 className="text-4xl font-extrabold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">
          Multi-Agent Engineering Execution
        </h2>
        <p className="text-muted-foreground text-center max-w-2xl mb-8">
          Deploy an entire autonomous AI engineering team. They will sequentially retrieve data, extract components, conduct research, optimize the architecture, validate for contradictions, and output a perfect execution package.
        </p>
        <Button size="lg" className="h-14 px-8 text-lg rounded-full" onClick={handleGenerate}>
          Deploy Engineering Team
        </Button>
        {errorMsg && <p className="text-destructive mt-4">{errorMsg}</p>}
      </div>
    );
  }

  if (state?.status === "RUNNING") {
    return (
      <div className="w-full flex flex-col items-center border-t border-border/50 pt-16 mt-8 animate-in fade-in duration-500">
        <AgentActivityTimeline currentState={state.current_agent} logs={state.logs || []} />
      </div>
    );
  }

  return (
    <div className="w-full flex flex-col gap-12 border-t border-border/50 pt-16 mt-8 animate-in fade-in slide-in-from-bottom-8 duration-700">
      
      <div className="text-center">
        <h2 className="text-4xl font-extrabold mb-2">Execution Package Ready</h2>
        <p className="text-muted-foreground">Your autonomous engineering audit is complete.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Score Card */}
        <Card className="bg-card/50 border-border/50 col-span-1 flex flex-col items-center justify-center p-8 text-center">
          <CardTitle className="text-lg text-muted-foreground mb-4">Execution Readiness Score</CardTitle>
          <div className={`text-7xl font-black ${getScoreColor(state.execution_score)}`}>
            {state.execution_score}%
          </div>
          <p className="text-sm mt-4 text-muted-foreground">Based on project complexity, components availability, and budget realism.</p>
        </Card>

        {/* Exports */}
        <Card className="bg-card/50 border-border/50 col-span-2">
          <CardHeader>
            <CardTitle>Download Documentation</CardTitle>
            <CardDescription>Export your finalized architectural plan</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-4">
            <Button variant="outline" className="h-16 justify-start px-6" onClick={() => downloadFile(state.pdf_export_path)}>
              <Download className="mr-4 text-red-400" /> Complete PDF Report
            </Button>
            <Button variant="outline" className="h-16 justify-start px-6" onClick={() => downloadFile(state.markdown_export_path)}>
              <Download className="mr-4 text-blue-400" /> Markdown (Obsidian/GitHub)
            </Button>
            <Button variant="outline" className="h-16 justify-start px-6" onClick={() => downloadFile(state.csv_export_path)}>
              <Download className="mr-4 text-green-400" /> Timeline CSV (Notion)
            </Button>
            <Button variant="outline" className="h-16 justify-start px-6" onClick={() => downloadFile(state.json_export_path)}>
              <Download className="mr-4 text-yellow-400" /> Raw JSON Schema
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Alternative Components & Decision Trace */}
      <Card className="bg-card/50 border-border/50">
        <CardHeader>
          <CardTitle className="flex items-center gap-2"><History className="text-purple-400" /> Architectural Decision Trace</CardTitle>
          <CardDescription>Explainable AI rationale behind optimization tradeoffs.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="bg-muted/50 text-muted-foreground uppercase">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">Engineering Decision</th>
                  <th className="px-4 py-3">AI Rationale</th>
                  <th className="px-4 py-3 rounded-tr-lg">Responsible Agent</th>
                </tr>
              </thead>
              <tbody>
                {state.decision_trace?.map((trace: any, idx: number) => (
                  <tr key={idx} className="border-b border-border/50">
                    <td className="px-4 py-3 font-medium text-primary">{trace.decision}</td>
                    <td className="px-4 py-3 text-muted-foreground">{trace.rationale}</td>
                    <td className="px-4 py-3 text-xs"><Badge variant="outline">{trace.agent}</Badge></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Insights & Recommendations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="bg-card/50 border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><AlertTriangle className="text-yellow-400" /> Critical Risks & Insights</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {state.research_insights?.map((insight: any, idx: number) => {
              const text = typeof insight === 'string' ? insight : (insight.insight || insight.description || JSON.stringify(insight));
              return (
              <div key={idx} className="bg-yellow-500/10 border border-yellow-500/20 p-3 rounded-lg text-sm text-yellow-100">
                {text}
              </div>
            )})}
          </CardContent>
        </Card>

        <Card className="bg-card/50 border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><CheckCircle2 className="text-emerald-400" /> Engineering Recommendations</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {state.engineering_recommendations?.map((rec: any, idx: number) => {
              const text = typeof rec === 'string' ? rec : (rec.recommendation || rec.description || JSON.stringify(rec));
              return (
              <div key={idx} className="bg-emerald-500/10 border border-emerald-500/20 p-3 rounded-lg text-sm text-emerald-100">
                {text}
              </div>
            )})}
          </CardContent>
        </Card>
      </div>

      {/* Simulation & Deployment Intelligence */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <Card className="bg-card/50 border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><Activity className="text-orange-400" /> Engineering Feasibility Simulation</CardTitle>
            <CardDescription>AI simulated runtime bottlenecks.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {state.simulation_results?.length === 0 && <p className="text-sm text-muted-foreground">No critical bottlenecks simulated.</p>}
            {state.simulation_results?.map((res: any, idx: number) => {
              const text = typeof res === 'string' ? res : (res.result || res.description || JSON.stringify(res));
              return (
              <div key={idx} className="bg-orange-500/10 border border-orange-500/20 p-3 rounded-lg text-sm text-orange-200">
                {text}
              </div>
            )})}
          </CardContent>
        </Card>

        <Card className="bg-card/50 border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><Server className="text-cyan-400" /> Deployment Intelligence</CardTitle>
            <CardDescription>Production scaling architecture.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {state.deployment_recommendations?.map((rec: any, idx: number) => {
              const text = typeof rec === 'string' ? rec : (rec.recommendation || rec.description || JSON.stringify(rec));
              return (
              <div key={idx} className="bg-cyan-500/10 border border-cyan-500/20 p-3 rounded-lg text-sm text-cyan-100">
                {text}
              </div>
            )})}
          </CardContent>
        </Card>
      </div>

      {/* Critical Path & Timeline */}
      <div className="flex flex-col gap-4">
        <h3 className="text-2xl font-bold flex items-center gap-2"><Info className="text-blue-400" /> Implementation Critical Path</h3>
        <div className="flex flex-wrap gap-2 mb-6">
          {state.execution_plan?.map((step: any, idx: number) => {
            const label = typeof step === 'string' ? step : (step.name || step.title || JSON.stringify(step));
            return (
            <Badge key={idx} variant="secondary" className="px-3 py-1 text-sm bg-blue-500/20 text-blue-200 border-blue-500/30">
              {idx + 1}. {label}
            </Badge>
          )})}
        </div>
        {state.gantt_tasks?.length > 0 ? (
          <FrappeGantt tasks={state.gantt_tasks} />
        ) : (
          <div className="p-8 text-center text-muted-foreground border rounded-md">No timeline tasks generated.</div>
        )}
      </div>

    </div>
  );
}
