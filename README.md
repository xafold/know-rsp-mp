# Know Your RSP Candidate

> **Civic transparency website** for Nepal's Rastriya Swatantra Party (RSP) elected Members of Parliament from the **2026 General Election (March 5, 2026)**.

## 🎯 Project Objective

A public, searchable directory of all RSP MPs elected in the 2026 Nepalese General Election. Enables citizens to explore, filter, and learn about their elected RSP representatives — backgrounds, education, contributions, and electoral performance.

**This is a civic transparency tool** — not affiliated with RSP or any political party.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | Next.js 15 (App Router, SSG) |
| Language | TypeScript (strict, no `any`) |
| Styling | Tailwind CSS v4 |
| UI Components | shadcn/ui |
| Charts | Recharts |
| Icons | Lucide React |
| Dark Mode | next-themes |
| Deploy | Vercel (Free Tier) |

---

## 📁 Project Structure

```
know_rsp_candidate/
├── app/
│   ├── layout.tsx                    # Root layout with nav, footer, theme
│   ├── page.tsx                      # Home / directory page with search + filters
│   ├── analytics/
│   │   └── page.tsx                  # Analytics dashboard (charts)
│   ├── about/
│   │   └── page.tsx                  # About / methodology page
│   └── candidate/
│       └── [id]/
│           └── page.tsx              # Individual MP profile (SSG)
├── components/
│   ├── ui/                           # shadcn/ui components
│   ├── CandidateCard.tsx             # Card in directory grid
│   ├── CandidateGrid.tsx             # Grid with filter state
│   ├── FilterPanel.tsx               # Sidebar/bottom-sheet filters
│   ├── SearchBar.tsx                 # Real-time search input
│   ├── StatsBar.tsx                  # Live stats (count, avg age, etc.)
│   ├── VoteChart.tsx                 # Vote bar/donut charts
│   ├── EducationTimeline.tsx         # Education history timeline
│   ├── ContributionCard.tsx          # Contribution cards by category
│   ├── SourceLinks.tsx               # Prominent source links section
│   └── Navbar.tsx                    # Top navigation with theme toggle
├── data/
│   └── candidates.json               # ALL candidate data (static, no DB)
├── lib/
│   ├── types.ts                      # TypeScript interfaces
│   ├── candidates.ts                 # Data loading & filtering utilities
│   └── utils.ts                      # Helper functions
├── public/
│   ├── candidates/                   # MP photos (or placeholder silhouettes)
│   └── rsp-share-preview.jpg         # Default OG image for social sharing
├── vercel.json
└── tailwind.config.ts
```

---

## 📊 Data Model (`lib/types.ts`)

```typescript
interface Candidate {
  id: string;                          // slug: "rabi-lamichhane"
  name: string;
  nameNepali?: string;                 // Devanagari
  photo?: string;
  dateOfBirth?: string;                // ISO: "1985-10-25"
  age?: number;
  gender: "Male" | "Female" | "Other";
  education: {
    level: "SLC" | "Intermediate" | "+2" | "Bachelors" | "Masters" | "PhD" | "Other";
    degree?: string;
    institution?: string;
    country?: string;
  }[];
  constituency: {
    name: string;                      // "Chitwan-2"
    district: string;
    province: string;
    provinceNumber: number;            // 1-7
  };
  electionType: "FPTP" | "PR";
  votesReceived?: number;
  totalValidVotes?: number;
  voteSharePercent?: number;
  runnerUp?: { name: string; party: string; votes: number; };
  winMargin?: number;
  winMarginPercent?: number;
  profession?: string;
  biography?: string;
  majorContributions: {
    title: string;
    description: string;
    category: "Social Work" | "Infrastructure" | "Education" | "Healthcare" | "Environment" | "Governance" | "Youth" | "Other";
  }[];
  previousPositions?: string[];
  sources: {
    platform: "Wikipedia" | "LinkedIn" | "Twitter/X" | "Facebook" | "Nepal Election Commission" | "Parliament Website" | "News Article" | "Official Website" | "Other";
    url: string;
    label?: string;
  }[];
  lastUpdated: string;                 // ISO date of last data verification
}
```

---

## 🖥️ Pages

| Page | Route | Description |
|---|---|---|
| Home/Directory | `/` | Search + filter grid of all RSP MPs |
| Candidate Profile | `/candidate/[id]` | Full profile with bio, education, contributions, vote data, sources |
| Analytics | `/analytics` | Charts: education distribution, age histogram, gender ratio, province seats |
| About | `/about` | Project purpose, methodology, disclaimer |

---

## 🔍 Key Features

- **Real-time search** by name, constituency, district
- **Filter panel**: Province, Education Level, Age Range, Gender, Vote Share, Election Type, Win Margin
- **Sort**: By name, age, vote share, win margin, constituency
- **Stats bar**: Live summary stats based on active filters
- **SSG**: All pages pre-rendered at build time — Vercel free tier compatible
- **Dark mode**: via next-themes
- **SEO**: Dynamic meta/OG tags, sitemap.xml, robots.txt, JSON-LD Person schema

---

## 🚀 Getting Started

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # Production build
```

---

## ⚠️ Data Notes

- The 2026 Nepal General Election occurred **March 5, 2026** (3 days before project start)
- Final results may still be incoming — UI handles missing/pending data gracefully
- **Priority candidates**: Rabi Lamichhane (RSP President), Sobita Gautam, Balen Shah, Swarnim Wagle
- Data sourced from: Nepal Election Commission (`election.gov.np`), Parliament website, Wikipedia, news outlets
- **Never fabricate data** — leave fields null if unverifiable. This is a civic transparency tool.
- All sources must be cited in the `sources[]` array

---

## 🎨 Design

- Aesthetic: Clean civic/institutional — government transparency portal meets modern web
- RSP accent colors (party uses bell symbol — blue/green branding)
- Font: Outfit or Plus Jakarta Sans (headings), Source Sans 3 (body) — both render Devanagari
- Lucide React icons
- Subtle animations: staggered card reveals, smooth filter transitions
- WCAG 2.1 AA accessibility

---

## 📝 Claude Code Context

This file exists to preserve project context across sessions. If you are resuming work:

1. Check `data/candidates.json` for current data state
2. Check `lib/types.ts` for the canonical TypeScript interfaces
3. The project uses **Tailwind CSS v4** (imported via `@import "tailwindcss"` in globals.css, NOT via tailwind.config.js plugin)
4. shadcn/ui is configured with the `new-york` style
5. All pages are SSG — no server-side API routes needed at runtime
6. Run `npm run build` to verify build health before committing

### Pending Work Checklist
- [ ] Install: shadcn/ui, recharts, lucide-react, next-themes
- [ ] Create `lib/types.ts`
- [ ] Create `data/candidates.json` with researched RSP 2026 MPs
- [ ] Build components: Navbar, CandidateCard, CandidateGrid, FilterPanel, SearchBar, StatsBar
- [ ] Build profile components: VoteChart, EducationTimeline, ContributionCard, SourceLinks
- [ ] Build pages: Home, Candidate Profile, Analytics, About
- [ ] Configure vercel.json
- [ ] SEO: sitemap.xml, robots.txt, JSON-LD
- [ ] Test `npm run build`
- [ ] Deploy to Vercel
