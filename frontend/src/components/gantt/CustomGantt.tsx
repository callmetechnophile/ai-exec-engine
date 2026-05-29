"use client";

import React, { useMemo } from "react";

interface Task {
  id: string;
  name: string;
  start: string;
  end: string;
  dependencies: string;
}

interface CustomGanttProps {
  tasks: Task[];
}

const COLORS = [
  "bg-sky-500",
  "bg-emerald-500",
  "bg-amber-500",
  "bg-fuchsia-400",
  "bg-indigo-500"
];

const TEAMS = ["Architecture & Layout", "Core Implementation", "Refinement & Delivery"];

const parseISO = (dateStr: string) => new Date(dateStr);
const addDays = (date: Date, days: number) => {
  const result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
};
const differenceInDays = (date2: Date, date1: Date) => {
  const diffTime = date2.getTime() - date1.getTime();
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};
const formatMonth = (d: Date) => d.toLocaleDateString("en-US", { month: "short" }).toUpperCase();
const formatDay = (d: Date) => d.toLocaleDateString("en-US", { day: "2-digit" });

export default function CustomGantt({ tasks }: CustomGanttProps) {
  const { minDate, totalDays, groupedTasks } = useMemo(() => {
    if (!tasks || tasks.length === 0) {
      return { minDate: new Date(), maxDate: new Date(), totalDays: 0, groupedTasks: [] };
    }

    const dates = tasks.flatMap((t) => [parseISO(t.start), parseISO(t.end)]);
    const minD = new Date(Math.min(...dates.map((d) => d.getTime())));
    const maxD = new Date(Math.max(...dates.map((d) => d.getTime())));
    
    // Add padding to timeline
    const paddedMin = addDays(minD, -2);
    const paddedMax = addDays(maxD, 2);
    const tDays = differenceInDays(paddedMax, paddedMin) + 1;

    // Group tasks into "Teams/Phases" for visual fidelity
    const groups = TEAMS.map(team => ({ name: team, tasks: [] as any[] }));
    
    tasks.forEach((task, idx) => {
      let startOffset = differenceInDays(parseISO(task.start), paddedMin);
      if (startOffset < 0) startOffset = 0;
      let duration = differenceInDays(parseISO(task.end), parseISO(task.start)) + 1;
      if (duration < 1) duration = 1;
      
      const groupIdx = Math.floor((idx / tasks.length) * TEAMS.length);
      const color = COLORS[idx % COLORS.length];
      
      groups[groupIdx].tasks.push({
        ...task,
        startOffset,
        duration,
        color
      });
    });

    return { minDate: paddedMin, maxDate: paddedMax, totalDays: tDays, groupedTasks: groups };
  }, [tasks]);

  if (!tasks || tasks.length === 0) return null;

  // Generate date headers
  const dateHeaders = [];
  for (let i = 0; i < totalDays; i++) {
    const d = addDays(minDate, i);
    dateHeaders.push(
      <div key={i} className="flex flex-col items-center justify-end pb-2 border-l border-border/40 text-[10px] text-muted-foreground w-12 min-w-[3rem]">
        <span className="font-bold tracking-widest opacity-60 mb-1">{formatMonth(d)}</span>
        <span className="text-xs">{formatDay(d)}</span>
      </div>
    );
  }

  return (
    <div className="w-full bg-card/80 backdrop-blur-sm rounded-xl border shadow-2xl overflow-hidden flex flex-col mb-12">
      <div className="p-6 border-b bg-muted/20">
        <h2 className="text-3xl font-light tracking-tight text-foreground">Product roadmap</h2>
        <p className="text-sm text-muted-foreground mt-1">Autonomous Execution Timeline</p>
      </div>

      <div className="overflow-x-auto p-6 custom-scrollbar">
        <div className="min-w-max">
          
          {/* Timeline Header */}
          <div className="flex ml-48 mb-4 border-b border-border/60">
            {dateHeaders}
          </div>

          {/* Grid Layout */}
          <div className="relative">
            {groupedTasks.map((group, gIdx) => (
              <div key={gIdx} className="mb-10 relative flex group/team">
                
                {/* Team Sidebar */}
                <div className="w-48 flex-shrink-0 pr-4 pt-1 z-20">
                  <div className="bg-muted/80 text-muted-foreground text-xs font-semibold px-4 py-2 rounded-full inline-flex items-center gap-2 shadow-sm border border-border/50">
                    <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                    {group.name}
                  </div>
                </div>

                {/* Tracks */}
                <div className="flex-1 relative pb-2 pt-2">
                  {/* Background Grid Lines */}
                  <div className="absolute inset-0 flex pointer-events-none z-0">
                    {Array.from({ length: totalDays }).map((_, i) => (
                      <div key={i} className="border-l border-border/20 h-full w-12 min-w-[3rem]"></div>
                    ))}
                  </div>

                  {/* Tasks */}
                  <div className="relative flex flex-col gap-4 z-10 pt-1">
                    {group.tasks.map((task) => (
                      <div 
                        key={task.id}
                        className={`h-11 ${task.color} rounded-sm shadow-md flex items-center px-4 cursor-pointer hover:brightness-110 hover:-translate-y-0.5 transition-all text-white overflow-hidden`}
                        style={{
                          marginLeft: `${task.startOffset * 3}rem`,
                          width: `${Math.max(task.duration * 3, 3)}rem`
                        }}
                        title={`${task.name} (${task.start} to ${task.end})`}
                      >
                        <span className="text-xs font-bold tracking-wide truncate drop-shadow-md">{task.name}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>

        </div>
      </div>
    </div>
  );
}
