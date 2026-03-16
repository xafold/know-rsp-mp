import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Election Analytics \u2013 RSP Vote Performance & Demographics",
  description:
    "Detailed election analytics for RSP Members of Parliament. Vote share leaderboards, win margins, province-level performance, age and education demographics, and race competitiveness data from Nepal's 2026 General Election.",
  alternates: {
    canonical: "/analytics",
  },
  openGraph: {
    title: "RSP Election Analytics \u2013 Vote Performance & Demographics",
    description:
      "Explore RSP election performance: vote share rankings, win margins, province summaries, and demographic breakdowns from Nepal's 2026 General Election.",
    url: "/analytics",
    images: [{ url: "/rsp-share-preview.jpg", width: 1024, height: 576, alt: "Know RSP share preview" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "RSP Election Analytics \u2013 Vote Performance & Demographics",
    description:
      "Explore RSP election performance: vote share rankings, win margins, province summaries, and demographic breakdowns.",
    images: ["/rsp-share-preview.jpg"],
  },
};

export default function AnalyticsLayout({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
