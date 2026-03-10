import type { ReactNode } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Contribution, ContributionCategory } from "@/lib/types";
import {
  Heart,
  Building2,
  BookOpen,
  Activity,
  Leaf,
  Scale,
  Users,
  Star,
} from "lucide-react";

interface ContributionCardProps {
  contribution: Contribution;
}

const CATEGORY_CONFIG: Record<
  ContributionCategory,
  { color: string; bg: string; icon: ReactNode }
> = {
  "Social Work": {
    color: "text-green-700 dark:text-green-400",
    bg: "bg-green-100 dark:bg-green-900/30",
    icon: <Heart className="h-3.5 w-3.5" />,
  },
  Infrastructure: {
    color: "text-orange-700 dark:text-orange-400",
    bg: "bg-orange-100 dark:bg-orange-900/30",
    icon: <Building2 className="h-3.5 w-3.5" />,
  },
  Education: {
    color: "text-blue-700 dark:text-blue-400",
    bg: "bg-blue-100 dark:bg-blue-900/30",
    icon: <BookOpen className="h-3.5 w-3.5" />,
  },
  Healthcare: {
    color: "text-red-700 dark:text-red-400",
    bg: "bg-red-100 dark:bg-red-900/30",
    icon: <Activity className="h-3.5 w-3.5" />,
  },
  Environment: {
    color: "text-emerald-700 dark:text-emerald-400",
    bg: "bg-emerald-100 dark:bg-emerald-900/30",
    icon: <Leaf className="h-3.5 w-3.5" />,
  },
  Governance: {
    color: "text-slate-700 dark:text-slate-400",
    bg: "bg-slate-100 dark:bg-slate-900/30",
    icon: <Scale className="h-3.5 w-3.5" />,
  },
  Youth: {
    color: "text-purple-700 dark:text-purple-400",
    bg: "bg-purple-100 dark:bg-purple-900/30",
    icon: <Users className="h-3.5 w-3.5" />,
  },
  Other: {
    color: "text-muted-foreground",
    bg: "bg-muted",
    icon: <Star className="h-3.5 w-3.5" />,
  },
};

export default function ContributionCard({ contribution }: ContributionCardProps) {
  const config = CATEGORY_CONFIG[contribution.category];

  return (
    <Card size="sm" className="border-border/80 bg-[var(--surface-soft)]">
      <CardContent className="pt-3">
        <div className="flex flex-col gap-2">
          <span
            className={`inline-flex w-fit items-center gap-1 rounded-full px-2.5 py-1 text-xs font-medium ${config.color} ${config.bg}`}
          >
            {config.icon}
            {contribution.category}
          </span>

          <p className="text-sm font-semibold leading-snug text-foreground">
            {contribution.title}
          </p>

          {contribution.description && (
            <p className="text-sm leading-6 text-muted-foreground">
              {contribution.description}
            </p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
