import type { MetadataRoute } from "next";
import { getCandidates } from "@/lib/getCandidates";

const BASE_URL = "https://knowrspcandidate.vercel.app";

export default function sitemap(): MetadataRoute.Sitemap {
  const candidates = getCandidates();

  const staticPages: MetadataRoute.Sitemap = [
    {
      url: BASE_URL,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1,
    },
    {
      url: `${BASE_URL}/analytics`,
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.7,
    },
    {
      url: `${BASE_URL}/about`,
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.5,
    },
  ];

  const candidatePages: MetadataRoute.Sitemap = candidates.map((candidate) => ({
    url: `${BASE_URL}/candidate/${candidate.id}`,
    lastModified: new Date(candidate.lastUpdated),
    changeFrequency: "weekly" as const,
    priority: 0.8,
  }));

  return [...staticPages, ...candidatePages];
}
