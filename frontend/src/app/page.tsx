"use client";

import { useState, useRef } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Mic, Search, Loader2, Download, ExternalLink, ChevronRight, History, Sun, Moon } from "lucide-react";
import FrappeGantt from "@/components/gantt/FrappeGantt";
import CodeBlock from "@/components/code/CodeBlock";
import ExecutionPackage from "@/components/ExecutionPackage";

const COMPLEXITY_LEVELS = ["Easy", "Medium", "Hard"];
const TIMEFRAMES = ["1 Hour", "1 Day", "1 Week", "1 Month", "6 Months"];

export default function Home() {
  const [query, setQuery] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<any>(null);
  const [budget, setBudget] = useState([1000]);
  const [errorMsg, setErrorMsg] = useState("");
  const [recentSearches, setRecentSearches] = useState<string[]>([]);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  // Deep Analysis State
  const [complexityIdx, setComplexityIdx] = useState([1]);
  const [timeframeIdx, setTimeframeIdx] = useState([2]);
  const [isAdvancing, setIsAdvancing] = useState(false);
  const [deepResults, setDeepResults] = useState<any>(null);

  // On-Demand Code Gen State
  const [selectedMcu, setSelectedMcu] = useState("arduino");
  const [generatedCode, setGeneratedCode] = useState("");
  const [isGeneratingCode, setIsGeneratingCode] = useState(false);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      const audioChunks: BlobPart[] = [];

      mediaRecorderRef.current.ondataavailable = (event) => audioChunks.push(event.data);

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
        await handleAudioUpload(audioBlob);
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      alert("Microphone access denied or error occurred.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleAudioUpload = async (audioBlob: Blob) => {
    setIsSearching(true);
    setErrorMsg("");
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.webm");

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/speech-to-text`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Audio transcription failed");
      
      if (data.text) {
        setQuery(data.text);
        handleSearch(data.text);
      }
    } catch (error: any) {
      console.error("Audio processing failed", error);
      setErrorMsg(error.message);
      setIsSearching(false);
    }
  };

  const handleSearch = async (searchQuery: string = query) => {
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    setErrorMsg("");
    setDeepResults(null); // Reset deep analysis
    try {
      if (!recentSearches.includes(searchQuery)) {
        setRecentSearches(prev => [searchQuery, ...prev].slice(0, 5));
      }
      
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/analyze-project`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: searchQuery }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Project analysis failed");
      setResults(data);
    } catch (error: any) {
      console.error("Search failed", error);
      setErrorMsg(error.message);
    } finally {
      setIsSearching(false);
    }
  };

  const filterComponents = (components: any[]) => {
    if (!components) return [];
    return components.filter((c) => c.estimated_price <= budget[0]);
  };

  const handleAdvanceFurther = async () => {
    setIsAdvancing(true);
    setErrorMsg("");
    try {
      // Gather all components to send
      let allComponents: any[] = [];
      if (results) {
        ["electronics", "structural", "mechanical", "pneumatic", "fluid_power"].forEach(cat => {
          if (results[cat]) allComponents = allComponents.concat(results[cat]);
        });
      }

      const payload = {
        query: query,
        components: allComponents,
        budget: budget[0],
        complexity: COMPLEXITY_LEVELS[complexityIdx[0]],
        time: TIMEFRAMES[timeframeIdx[0]]
      };

      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/advance-research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Deep analysis failed");
      setDeepResults(data);
    } catch (error: any) {
      console.error("Deep analysis failed", error);
      setErrorMsg(error.message);
    } finally {
      setIsAdvancing(false);
    }
  };

  const handleGenerateCode = async () => {
    setIsGeneratingCode(true);
    setErrorMsg("");
    try {
      let allComponents: any[] = [];
      if (results) {
        ["electronics", "structural", "mechanical", "pneumatic", "fluid_power"].forEach(cat => {
          if (results[cat]) allComponents = allComponents.concat(results[cat]);
        });
      }

      const payload = {
        query: query,
        components: allComponents,
        mcu_type: selectedMcu
      };

      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_URL}/api/generate-code`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Code generation failed");
      setGeneratedCode(data.code);
    } catch (error: any) {
      console.error("Code generation failed", error);
      setErrorMsg(error.message);
    } finally {
      setIsGeneratingCode(false);
    }
  };

  const downloadCSV = () => {
    if (!deepResults?.csv_export) return;
    const blob = new Blob([deepResults.csv_export], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'project_tasks.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <main className="min-h-screen text-foreground p-8 flex flex-col items-center relative">
      {/* Top Left Logo */}
      <div className="absolute top-4 left-4 sm:left-8 z-50">
        <a href="/" className="flex items-center hover:opacity-80 transition-opacity cursor-pointer">
          <img src="/logo.png" alt="WorkflowGuide Logo" className="h-12 w-auto object-contain drop-shadow-md rounded-md" />
        </a>
      </div>

      {/* Top Right Dark Mode Toggle */}
      <div className="absolute top-4 right-4 sm:right-8 z-50">
        <Button variant="outline" size="icon" className="rounded-full shadow-lg" onClick={() => document.documentElement.classList.toggle('dark')}>
          <Sun className="h-5 w-5 dark:hidden" />
          <Moon className="h-5 w-5 hidden dark:block" />
        </Button>
      </div>

      <div className="w-full max-w-5xl flex flex-col items-center gap-8 mt-12 mb-12 text-center">
        <h1 className="text-4xl sm:text-6xl md:text-8xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-br from-indigo-400 via-purple-400 to-emerald-400 drop-shadow-sm pb-2">
          WORKFLOWGUIDE.AI
        </h1>
        <div className="flex flex-col gap-2">
          <p className="text-lg sm:text-xl md:text-2xl font-bold tracking-widest text-muted-foreground uppercase opacity-80">
            IDEA → EXECUTION
          </p>
          <p className="text-white italic">
            Hey Builder, Wassup! , Wanna build something new
          </p>
        </div>

        <div className="relative w-full max-w-2xl flex items-center shadow-lg rounded-full overflow-hidden border border-border/50 bg-card/50 backdrop-blur-sm">
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder="I want to build a remote control car..."
            className="w-full border-0 bg-transparent h-14 pl-6 pr-24 text-lg focus-visible:ring-0"
          />
          <div className="absolute right-2 flex items-center gap-2">
            <Button
              variant={isRecording ? "destructive" : "secondary"}
              size="icon"
              className="rounded-full"
              onMouseDown={startRecording}
              onMouseUp={stopRecording}
              onTouchStart={startRecording}
              onTouchEnd={stopRecording}
            >
              <Mic className={isRecording ? "animate-pulse" : ""} />
            </Button>
            <Button
              variant="default"
              size="icon"
              className="rounded-full"
              onClick={() => handleSearch()}
              disabled={isSearching || isAdvancing}
            >
              {isSearching ? <Loader2 className="animate-spin" /> : <Search />}
            </Button>
          </div>
        </div>

        <div className="flex flex-col items-center gap-6 w-full max-w-2xl mt-4">
          <div className="flex flex-col items-center gap-3 w-full">
            <span className="text-xs text-muted-foreground uppercase tracking-widest">Suggestions</span>
            <div className="flex flex-wrap gap-2 justify-center w-full">
              {["esp32 smart weather station", "arduino automated plant waterer", "raspberry pi object tracking camera", "stm32 flight controller"].map(suggestion => (
                <Badge key={suggestion} variant="secondary" className="cursor-pointer hover:bg-primary/20 transition-colors" onClick={() => { setQuery(suggestion); handleSearch(suggestion); }}>
                  {suggestion}
                </Badge>
              ))}
            </div>
          </div>

          {recentSearches.length > 0 && (
            <div className="flex flex-col items-center gap-3 w-full border-t border-border/50 pt-4">
              <span className="text-xs text-muted-foreground uppercase tracking-widest flex items-center gap-1"><History className="h-3 w-3" /> Recent Searches</span>
              <div className="flex flex-wrap gap-2 justify-center w-full">
                {recentSearches.map(recent => (
                  <Badge key={recent} variant="outline" className="cursor-pointer hover:bg-primary/10 transition-colors" onClick={() => { setQuery(recent); handleSearch(recent); }}>
                    {recent}
                  </Badge>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {errorMsg && (
        <div className="mt-8 p-4 bg-destructive/10 border border-destructive rounded-lg text-destructive max-w-2xl text-center">
          <strong>Error:</strong> {errorMsg}
          <p className="text-sm mt-2">Check your backend terminal (FastAPI) for the exact error trace. It might be an issue with your API keys or models.</p>
        </div>
      )}

      {isSearching && !results && !errorMsg && (
        <div className="mt-20 flex flex-col items-center gap-4 text-muted-foreground animate-pulse">
          <Loader2 className="h-12 w-12 animate-spin text-primary" />
          <p>Autonomously researching projects and components...</p>
        </div>
      )}

      {results && !isSearching && (
        <div className="w-full max-w-6xl flex flex-col gap-12 animate-in fade-in slide-in-from-bottom-8 duration-700">
          
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Projects Column */}
            <div className="lg:col-span-8 flex flex-col gap-6">
              <div className="flex items-center gap-4">
                <h2 className="text-2xl font-bold">Discovered Implementations</h2>
                <Badge variant="outline" className="text-sm">Domain: {results.project_info?.domain}</Badge>
                <Badge variant="outline" className="text-sm">Difficulty: {results.project_info?.difficulty}</Badge>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {results.projects.map((proj: any, idx: number) => (
                  <Card key={idx} className="bg-card/50 backdrop-blur border-border/50 hover:border-primary/50 transition-colors cursor-pointer" onClick={() => window.open(proj.url, "_blank")}>
                    <CardHeader className="p-4 pb-2">
                      <CardTitle className="text-lg line-clamp-2">{proj.title}</CardTitle>
                      <CardDescription className="text-xs text-primary">{proj.source}</CardDescription>
                    </CardHeader>
                    <CardContent className="p-4 pt-0">
                      {proj.thumbnail && (
                        <div className="w-full h-32 mb-4 rounded-md bg-muted overflow-hidden">
                          <img src={proj.thumbnail} alt={proj.title} className="w-full h-full object-cover" />
                        </div>
                      )}
                      <p className="text-sm text-muted-foreground line-clamp-3">{proj.summary}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Components Column */}
            <div className="lg:col-span-4 flex flex-col gap-6">
              <h2 className="text-2xl font-bold">Required Components</h2>
              <Card className="bg-card/50 backdrop-blur border-border/50">
                <CardHeader className="pb-4">
                  <CardTitle className="text-lg">Budget Filter</CardTitle>
                  <CardDescription>Max price per component (₹)</CardDescription>
                  <div className="flex items-center gap-4 mt-2">
                    <Slider value={budget} onValueChange={(val) => setBudget(Array.isArray(val) ? val : [val as number])} max={50000} step={100} className="flex-1" />
                    <Input type="number" value={budget[0] ?? 0} onChange={(e) => setBudget([Number(e.target.value) || 0])} className="w-20 text-right h-8" />
                  </div>
                </CardHeader>
                <CardContent>
                  <ScrollArea className="h-[40vh] pr-4">
                    <div className="flex flex-col gap-6">
                      {["electronics", "structural", "mechanical", "pneumatic", "fluid_power"].map((category) => {
                        const filtered = filterComponents(results[category] || []);
                        if (filtered.length === 0) return null;
                        return (
                          <div key={category} className="flex flex-col gap-3">
                            <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground border-b pb-1">{category.replace("_", " ")}</h3>
                            {filtered.map((comp: any, idx: number) => (
                              <div key={idx} className="flex flex-col gap-1 bg-muted/30 p-3 rounded-lg border border-border/30">
                                <div className="flex justify-between items-start">
                                  <span className="font-medium text-sm">{comp.name}</span>
                                  <Badge variant="secondary" className="text-xs">₹{comp.estimated_price}</Badge>
                                </div>
                                <p className="text-xs text-muted-foreground">{comp.description}</p>
                              </div>
                            ))}
                          </div>
                        );
                      })}
                    </div>
                  </ScrollArea>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* ADVANCE FURTHER SECTION */}
          <div className="flex flex-col items-center border-t pt-12 mt-4">
            <h2 className="text-3xl font-bold mb-4">Deep Engineering Analysis</h2>
            <p className="text-muted-foreground mb-8 max-w-2xl text-center">
              Configure your project parameters and let the AI generate code templates, retrieve academic research, optimize your components, and build a Gantt roadmap.
            </p>
            
            <div className="flex flex-col md:flex-row gap-8 w-full max-w-3xl mb-8">
              <Card className="flex-1 bg-card/50">
                <CardHeader>
                  <CardTitle>Complexity</CardTitle>
                  <CardDescription>{COMPLEXITY_LEVELS[complexityIdx[0]]}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Slider value={complexityIdx} onValueChange={(val) => setComplexityIdx(Array.isArray(val) ? val : [val as number])} max={2} step={1} />
                </CardContent>
              </Card>
              <Card className="flex-1 bg-card/50">
                <CardHeader>
                  <CardTitle>Timeline</CardTitle>
                  <CardDescription>{TIMEFRAMES[timeframeIdx[0]]}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Slider value={timeframeIdx} onValueChange={(val) => setTimeframeIdx(Array.isArray(val) ? val : [val as number])} max={4} step={1} />
                </CardContent>
              </Card>
            </div>

            <Button 
              size="lg" 
              className="text-lg px-8 py-6 rounded-full shadow-lg hover:shadow-primary/25 transition-all"
              onClick={handleAdvanceFurther}
              disabled={isAdvancing}
            >
              {isAdvancing ? (
                <><Loader2 className="mr-2 h-5 w-5 animate-spin" /> Running Deep Analysis...</>
              ) : (
                <>Advance Further <ChevronRight className="ml-2 h-5 w-5" /></>
              )}
            </Button>
          </div>

          {/* DEEP RESULTS */}
          {deepResults && (
            <div className="flex flex-col gap-12 w-full animate-in slide-in-from-bottom-8 duration-700 pb-20">
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Academic Research */}
                <Card className="bg-card/50 border-border/50">
                  <CardHeader>
                    <CardTitle>Relevant Academic Research</CardTitle>
                    <CardDescription>Papers retrieved via Tavily and processed through local RAG</CardDescription>
                  </CardHeader>
                  <CardContent className="flex flex-col gap-4">
                    {deepResults.research_papers?.map((paper: any, idx: number) => (
                      <div key={idx} className="flex flex-col gap-2 p-4 bg-muted/30 rounded-lg border">
                        <div className="flex justify-between items-start gap-4">
                          <h4 className="font-bold text-primary">{paper.title}</h4>
                          <Button variant="outline" size="sm" onClick={() => window.open(paper.url, "_blank")}><ExternalLink className="h-4 w-4" /></Button>
                        </div>
                        <p className="text-xs text-muted-foreground line-clamp-3">{paper.abstract}</p>
                      </div>
                    ))}
                    {!deepResults.research_papers?.length && <p className="text-sm text-muted-foreground">No accessible papers found.</p>}
                  </CardContent>
                </Card>

                {/* Engineering Insights & Concept */}
                <div className="flex flex-col gap-8">
                  {deepResults.generated_image && (
                    <Card className="overflow-hidden bg-card/50 border-border/50">
                       <img src={deepResults.generated_image} alt="Concept Visualization" className="w-full h-48 object-cover" />
                       <div className="p-2 text-center text-xs text-muted-foreground bg-muted">AI Concept Visualization (fal.ai)</div>
                    </Card>
                  )}
                  
                  <Card className="bg-card/50 border-border/50 flex-1">
                    <CardHeader>
                      <CardTitle>RAG Engineering Insights</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="list-disc pl-4 flex flex-col gap-3">
                        {deepResults.engineering_insights?.map((insight: string, idx: number) => (
                          <li key={idx} className="text-sm">{insight}</li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                </div>
              </div>

              {/* Interactive Code Generation */}
              <Card className="bg-card/50 border-border/50">
                <CardHeader>
                  <CardTitle>Generate Code</CardTitle>
                  <CardDescription>Select your target microcontroller to generate custom starter code for your project components.</CardDescription>
                </CardHeader>
                <CardContent className="flex flex-col gap-6">
                  <div className="flex flex-wrap gap-4 items-center">
                    {["arduino", "esp32", "stm32", "raspberry_pi"].map(mcu => (
                      <Button 
                        key={mcu} 
                        variant={selectedMcu === mcu ? "default" : "outline"}
                        onClick={() => setSelectedMcu(mcu)}
                        className="capitalize"
                      >
                        {mcu.replace("_", " ")}
                      </Button>
                    ))}
                    <Button 
                      onClick={handleGenerateCode} 
                      disabled={isGeneratingCode}
                      className="ml-auto min-w-[150px]"
                    >
                      {isGeneratingCode ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Generating...</> : "Generate Code"}
                    </Button>
                  </div>
                  
                  {generatedCode && (
                    <div className="mt-4 border border-border/50 rounded-lg overflow-hidden">
                      <div className="bg-muted px-4 py-2 text-xs font-semibold uppercase tracking-wider border-b">
                        {selectedMcu.replace("_", " ")} Source Code
                      </div>
                      <CodeBlock code={generatedCode} />
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Optimized Components */}
              <Card className="bg-card/50 border-border/50">
                <CardHeader>
                  <CardTitle>Component Optimization</CardTitle>
                  <CardDescription>Upgraded alternatives fitting Complexity: {COMPLEXITY_LEVELS[complexityIdx[0]]}, Budget: ₹{budget[0]}, Time: {TIMEFRAMES[timeframeIdx[0]]}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {deepResults.optimized_components?.map((comp: any, idx: number) => (
                      <div key={idx} className="p-4 bg-muted/30 rounded-lg border border-primary/20">
                        <div className="font-bold text-primary mb-1">{comp.name}</div>
                        <p className="text-sm text-muted-foreground mb-2">{comp.description}</p>
                        <Badge variant="default">Estimated: ₹{comp.estimated_price}</Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Gantt Chart & Export */}
              <div className="flex flex-col gap-4">
                <div className="flex justify-between items-end">
                  <h2 className="text-2xl font-bold">Project Timeline</h2>
                  <Button variant="outline" onClick={downloadCSV}>
                    <Download className="mr-2 h-4 w-4" /> Export CSV (Notion)
                  </Button>
                </div>
                {deepResults.gantt_tasks?.length > 0 ? (
                  <FrappeGantt tasks={deepResults.gantt_tasks} />
                ) : (
                  <div className="p-8 text-center text-muted-foreground border rounded-md">No timeline tasks generated.</div>
                )}
              </div>

              {/* PHASE 3: EXECUTION PACKAGE */}
              <ExecutionPackage 
                query={query} 
                components={(() => {
                  let allComponents: any[] = [];
                  ["electronics", "structural", "mechanical", "pneumatic", "fluid_power"].forEach(cat => {
                    if (results[cat]) allComponents = allComponents.concat(results[cat]);
                  });
                  return allComponents;
                })()} 
                budget={budget[0]} 
                complexity={COMPLEXITY_LEVELS[complexityIdx[0]]} 
                time={TIMEFRAMES[timeframeIdx[0]]} 
              />
            </div>
          )}
        </div>
      )}
    </main>
  );
}
