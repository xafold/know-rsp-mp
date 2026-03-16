import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "Compare RSP MPs | Know RSP",
  description:
    "Compare RSP Members of Parliament side by side — education, vote share, win margin, constituency, and more from the 2026 Nepal election.",
  openGraph: {
    title: "Compare RSP MPs | Know RSP",
    description:
      "Compare RSP Members of Parliament side by side — education, vote share, win margin, constituency, and more from the 2026 Nepal election.",
    url: "/compare",
    images: [{ url: "/rsp-share-preview.jpg", width: 1024, height: 576, alt: "Know RSP share preview" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Compare RSP MPs | Know RSP",
    description:
      "Compare RSP Members of Parliament side by side — education, vote share, win margin, constituency, and more from the 2026 Nepal election.",
    images: ["/rsp-share-preview.jpg"],
  },
};

export default function CompareLayout({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
