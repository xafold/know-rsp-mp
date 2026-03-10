import type { Candidate } from "@/lib/types";

/**
 * Safely loads candidate data from the JSON file.
 * Returns an empty array if the file doesn't exist or is malformed.
 */
export function getCandidates(): Candidate[] {
  try {
    // eslint-disable-next-line @typescript-eslint/no-require-imports
    const data = require("@/data/candidates.json");
    if (Array.isArray(data)) {
      return data as Candidate[];
    }
    return [];
  } catch {
    return [];
  }
}

export function getCandidateById(id: string): Candidate | undefined {
  return getCandidates().find((c) => c.id === id);
}
