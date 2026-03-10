import { GraduationCap, Globe } from "lucide-react";
import { Education, EducationLevel } from "@/lib/types";

interface EducationTimelineProps {
  education: Education[];
}

const LEVEL_ORDER: Record<EducationLevel, number> = {
  SLC: 1,
  Intermediate: 2,
  "+2": 3,
  Bachelors: 4,
  Masters: 5,
  PhD: 6,
  Other: 7,
};

const LEVEL_COLORS: Record<EducationLevel, string> = {
  SLC: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
  Intermediate:
    "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
  "+2": "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
  Bachelors:
    "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
  Masters:
    "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300",
  PhD: "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300",
  Other: "bg-muted text-muted-foreground",
};

export default function EducationTimeline({ education }: EducationTimelineProps) {
  if (!education || education.length === 0) {
    return (
      <p className="text-sm text-muted-foreground italic">
        Education details not available.
      </p>
    );
  }

  const sorted = [...education].sort(
    (a, b) => (LEVEL_ORDER[a.level] ?? 99) - (LEVEL_ORDER[b.level] ?? 99)
  );

  return (
    <ol className="relative flex flex-col gap-0">
      {sorted.map((edu, idx) => (
        <li key={idx} className="group flex gap-4">
          <div className="flex flex-col items-center">
            <div
              className="mt-1 h-3.5 w-3.5 shrink-0 rounded-full border-2 border-background"
              style={{ backgroundColor: "var(--rsp-blue)" }}
            />
            {idx < sorted.length - 1 && (
              <div className="my-1 w-px flex-1 bg-border/90" />
            )}
          </div>

          <div className="min-w-0 flex-1 pb-5">
            <div className="rounded-[1.3rem] border border-border/80 bg-[var(--surface-soft)] p-4">
              <div className="mb-2 flex flex-wrap items-center gap-2">
              <span
                className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${LEVEL_COLORS[edu.level]}`}
              >
                <GraduationCap className="h-3 w-3 mr-1" />
                {edu.level}
              </span>
              {edu.country && edu.country !== "Nepal" && (
                <span className="inline-flex items-center gap-1 text-xs text-muted-foreground">
                  <Globe className="h-3 w-3" />
                  {edu.country}
                </span>
              )}
              </div>
              {edu.degree && (
                <p className="text-sm font-semibold leading-snug text-foreground">
                  {edu.degree}
                </p>
              )}
              {edu.institution && (
                <p className="mt-1 text-sm text-muted-foreground">
                  {edu.institution}
                  {edu.country === "Nepal" || !edu.country ? "" : `, ${edu.country}`}
                </p>
              )}
            </div>
          </div>
        </li>
      ))}
    </ol>
  );
}
