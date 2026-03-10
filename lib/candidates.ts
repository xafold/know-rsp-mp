import candidatesData from '@/data/candidates.json';
import { Candidate, CandidateFilters, SortKey, SortOrder } from '@/lib/types';

export const candidates: Candidate[] = candidatesData as Candidate[];

export function getCandidateById(id: string): Candidate | undefined {
  return candidates.find((c) => c.id === id);
}

export function getDefaultFilters(): CandidateFilters {
  return {
    query: '',
    provinces: [],
    educationLevels: [],
    ageMin: 0,
    ageMax: 120,
    gender: [],
    voteShareMin: 0,
    voteShareMax: 100,
    electionType: [],
    winMarginMin: 0,
  };
}

export function filterAndSortCandidates(
  candidateList: Candidate[],
  filters: CandidateFilters,
  sortKey: SortKey,
  sortOrder: SortOrder
): Candidate[] {
  let result = [...candidateList];

  // Text search
  if (filters.query.trim()) {
    const q = filters.query.toLowerCase();
    result = result.filter(
      (c) =>
        c.name.toLowerCase().includes(q) ||
        (c.nameNepali ?? '').toLowerCase().includes(q) ||
        c.constituency.name.toLowerCase().includes(q) ||
        c.constituency.district.toLowerCase().includes(q) ||
        (c.profession ?? '').toLowerCase().includes(q)
    );
  }

  // Province filter
  if (filters.provinces.length > 0) {
    result = result.filter((c) =>
      filters.provinces.includes(c.constituency.province)
    );
  }

  // Election type filter
  if (filters.electionType.length > 0) {
    result = result.filter((c) => filters.electionType.includes(c.electionType));
  }

  // Gender filter
  if (filters.gender.length > 0) {
    result = result.filter((c) => filters.gender.includes(c.gender));
  }

  // Education level filter
  if (filters.educationLevels.length > 0) {
    result = result.filter((c) =>
      c.education.some((e) => filters.educationLevels.includes(e.level))
    );
  }

  // Age range filter
  if (filters.ageMin > 0 || filters.ageMax < 120) {
    result = result.filter((c) => {
      if (c.age == null) return true;
      return c.age >= filters.ageMin && c.age <= filters.ageMax;
    });
  }

  // Vote share filter
  if (filters.voteShareMin > 0 || filters.voteShareMax < 100) {
    result = result.filter((c) => {
      if (c.voteSharePercent == null) return true;
      return (
        c.voteSharePercent >= filters.voteShareMin &&
        c.voteSharePercent <= filters.voteShareMax
      );
    });
  }

  // Win margin filter
  if (filters.winMarginMin > 0) {
    result = result.filter((c) => {
      if (c.winMargin == null) return true;
      return c.winMargin >= filters.winMarginMin;
    });
  }

  // Sorting
  result.sort((a, b) => {
    let aVal: string | number | undefined;
    let bVal: string | number | undefined;

    switch (sortKey) {
      case 'name':
        aVal = a.name;
        bVal = b.name;
        break;
      case 'age':
        aVal = a.age;
        bVal = b.age;
        break;
      case 'voteSharePercent':
        aVal = a.voteSharePercent;
        bVal = b.voteSharePercent;
        break;
      case 'winMargin':
        aVal = a.winMargin;
        bVal = b.winMargin;
        break;
      case 'constituency':
        aVal = a.constituency.name;
        bVal = b.constituency.name;
        break;
    }

    if (aVal == null && bVal == null) return 0;
    if (aVal == null) return 1;
    if (bVal == null) return -1;

    if (typeof aVal === 'string' && typeof bVal === 'string') {
      const cmp = aVal.localeCompare(bVal);
      return sortOrder === 'asc' ? cmp : -cmp;
    }

    const cmp = (aVal as number) - (bVal as number);
    return sortOrder === 'asc' ? cmp : -cmp;
  });

  return result;
}
