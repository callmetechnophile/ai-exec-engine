"use client";

import React, { useEffect, useRef } from "react";
// @ts-ignore
import Gantt from "frappe-gantt";
import "@/app/gantt.css";

interface Task {
  id: string;
  name: string;
  start: string;
  end: string;
  progress: number;
  dependencies: string;
}

interface FrappeGanttProps {
  tasks: Task[];
}

export default function FrappeGantt({ tasks }: FrappeGanttProps) {
  const ganttRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ganttRef.current && tasks.length > 0) {
      // Clear previous instance
      ganttRef.current.innerHTML = '<svg id="gantt-svg"></svg>';
      
      try {
        new Gantt("#gantt-svg", tasks, {
          header_height: 50,
          column_width: 30,
          step: 24,
          view_modes: ['Quarter Day', 'Half Day', 'Day', 'Week', 'Month'],
          bar_height: 20,
          bar_corner_radius: 3,
          arrow_curve: 5,
          padding: 18,
          view_mode: 'Day',
          date_format: 'YYYY-MM-DD'
        });
      } catch (error) {
        console.error("Error initializing Frappe Gantt:", error);
      }
    }
  }, [tasks]);

  if (!tasks || tasks.length === 0) return null;

  return (
    <div className="w-full overflow-x-auto bg-card rounded-md border p-4">
      <div ref={ganttRef}>
        <svg id="gantt-svg"></svg>
      </div>
    </div>
  );
}
