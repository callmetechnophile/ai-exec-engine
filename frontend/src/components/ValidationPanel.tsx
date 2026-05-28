import { AlertTriangle, Info } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function ValidationPanel({ warnings }: { warnings: string[] }) {
  if (!warnings || warnings.length === 0) {
    return (
      <Card className="bg-emerald-500/10 border-emerald-500/20">
        <CardHeader>
          <CardTitle className="text-emerald-400 flex items-center gap-2">
            <Info className="h-5 w-5" /> Engineering Validation Passed
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-emerald-200">The Validation Agent found no contradictions or feasibility issues in this architecture.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-destructive/10 border-destructive/20">
      <CardHeader>
        <CardTitle className="text-destructive flex items-center gap-2">
          <AlertTriangle className="h-5 w-5" /> Validation Agent Warnings
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {warnings.map((warn, i) => (
          <div key={i} className="bg-destructive/20 border border-destructive/30 p-3 rounded-lg text-sm text-red-200">
            {warn}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
