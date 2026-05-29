import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Download, CheckCircle2, Info, AlertTriangle, Cpu, Server, History, Activity, MessageSquare, Bot, X, Send, Loader2, Image as ImageIcon } from "lucide-react";
import AgentActivityTimeline from "./AgentActivityTimeline";
import ValidationPanel from "./ValidationPanel";

export default function ExecutionPackage({ query, budget, complexity, time, imageUrl }: any) {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [state, setState] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState("");
  
  // Chat Recommendation State
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<{role: string, content: string}[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);

  // Prototype Image State
  const [prototypeImage, setPrototypeImage] = useState<string | null>(null);
  const [isGeneratingImage, setIsGeneratingImage] = useState(false);

  const handleGenerateImage = async () => {
    setIsGeneratingImage(true);
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/generate-image`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      if (data.base64_image) {
        setPrototypeImage(data.base64_image);
      }
    } catch (e) {
      console.error("Image gen failed", e);
    } finally {
      setIsGeneratingImage(false);
    }
  };

  const downloadImage = () => {
    if (!prototypeImage) return;
    const a = document.createElement("a");
    a.href = prototypeImage;
    a.download = "prototype-rendering.png";
    a.click();
  };

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (taskId && state?.status !== "DONE" && state?.status !== "ERROR") {
      interval = setInterval(async () => {
        try {
          const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
          const res = await fetch(`${API_URL}/api/orchestrator-status/${taskId}`);
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
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/start-orchestrator`, {
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
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    window.open(`${API_URL}/api/export/${type}/${filename}`, "_blank");
  };

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim()) return;

    const userMessage = chatInput;
    setChatMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setChatInput("");
    setIsChatLoading(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const payload = {
        message: userMessage,
        context: state
      };
      const res = await fetch(`${API_URL}/api/chat-recommendation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setChatMessages(prev => [...prev, { role: "assistant", content: data.response }]);
    } catch (err) {
      setChatMessages(prev => [...prev, { role: "assistant", content: "Error connecting to AI consultant." }]);
    } finally {
      setIsChatLoading(false);
    }
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

        <Card className="bg-card/50 border-border/50 relative overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="flex items-center gap-2"><CheckCircle2 className="text-emerald-400" /> Engineering Recommendations</CardTitle>
            <Button variant="ghost" size="icon" onClick={() => setChatOpen(!chatOpen)} className="rounded-full text-indigo-400 hover:text-indigo-300 hover:bg-indigo-500/20">
              <MessageSquare className="h-5 w-5" />
            </Button>
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

          {/* Chat Panel Inline Overlay */}
          {chatOpen && (
            <div className="absolute inset-0 bg-card/95 backdrop-blur-md z-30 flex flex-col animate-in fade-in zoom-in-95 border-t border-indigo-500/30">
              <div className="p-3 border-b border-border/50 flex justify-between items-center bg-indigo-500/10">
                <h3 className="font-semibold flex items-center gap-2 text-sm"><Bot className="h-4 w-4 text-indigo-400"/> AI Consultant</h3>
                <Button variant="ghost" size="icon" className="h-6 w-6" onClick={() => setChatOpen(false)}><X className="h-4 w-4" /></Button>
              </div>
              <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3 custom-scrollbar">
                {chatMessages.length === 0 && (
                   <p className="text-xs text-muted-foreground text-center mt-4">Ask me to verify any component alternative or technical choice probabilistically.</p>
                )}
                {chatMessages.map((m, idx) => (
                  <div key={idx} className={`p-3 rounded-lg text-sm max-w-[90%] ${m.role === 'user' ? 'bg-indigo-600/20 text-indigo-100 self-end ml-auto' : 'bg-muted text-foreground self-start'}`}>
                    <p className="whitespace-pre-wrap">{m.content}</p>
                  </div>
                ))}
                {isChatLoading && <Loader2 className="animate-spin text-indigo-400 h-5 w-5 mx-auto mt-2" />}
              </div>
              <div className="p-3 border-t border-border/50 bg-background/50">
                <form onSubmit={handleChatSubmit} className="flex gap-2">
                  <input 
                    type="text"
                    value={chatInput} 
                    onChange={(e) => setChatInput(e.target.value)} 
                    placeholder="Ask about an alternative..." 
                    className="flex-1 bg-muted/50 border border-border/50 rounded-md px-3 text-sm focus:outline-none focus:border-indigo-500"
                  />
                  <Button type="submit" size="sm" disabled={isChatLoading || !chatInput.trim()} className="bg-indigo-600 hover:bg-indigo-700 text-white px-3"><Send className="h-4 w-4"/></Button>
                </form>
              </div>
            </div>
          )}
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

      {/* Prototype Rendering Generation */}
      <div className="flex flex-col gap-4">
        <h3 className="text-2xl font-bold flex items-center gap-2"><ImageIcon className="text-pink-400" /> Prototype Rendering</h3>
        
        <Card className="overflow-hidden bg-card/50 border-border/50 mb-6 w-full mx-auto shadow-xl flex flex-col items-center justify-center p-8 min-h-[400px] relative group">
          {prototypeImage ? (
            <>
              <img src={prototypeImage} alt="Prototype Rendering" className="w-full h-full object-contain rounded-md absolute inset-0 z-0 p-4" />
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity z-10 flex items-center justify-center backdrop-blur-sm">
                <Button onClick={downloadImage} size="lg" className="bg-pink-600 hover:bg-pink-700 text-white shadow-2xl flex items-center gap-2">
                  <Download className="h-5 w-5" /> Download Concept Image
                </Button>
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center gap-4 z-10 text-center">
              <div className="bg-pink-500/10 p-6 rounded-full border border-pink-500/20 mb-2">
                <ImageIcon className="h-12 w-12 text-pink-400" />
              </div>
              <h4 className="text-xl font-bold text-white tracking-wide">Visualize Your Prototype</h4>
              <p className="text-muted-foreground text-sm max-w-sm mb-4">Click below to generate a high-fidelity, 3D CAD style conceptual rendering of your architecture using Fal.ai.</p>
              <Button 
                onClick={handleGenerateImage} 
                disabled={isGeneratingImage} 
                size="lg" 
                className="bg-pink-600/90 hover:bg-pink-600 text-white font-bold tracking-wider rounded-md border border-pink-500 shadow-lg shadow-pink-900/20 w-64 h-14"
              >
                {isGeneratingImage ? <><Loader2 className="mr-2 h-5 w-5 animate-spin"/> Rendering Engine...</> : "IMAGE GENERATION +"}
              </Button>
            </div>
          )}
        </Card>
      </div>

    </div>
  );
}
