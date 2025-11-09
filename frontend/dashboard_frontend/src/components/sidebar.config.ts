import {
  LayoutDashboard,
  CheckCircle,
  CalendarCheck,
  ShieldCheck,
  Building2,
  ListChecks,
  BarChart3,
  PieChart,
  Building,
  Globe,
  UserCircle2,
  Network,
  Link as LinkIcon,
  KeyRound,
  KeySquare,
} from "lucide-react";

export const sidebarPages = [
  { label: "Overview", route: "/dashboard", icon: LayoutDashboard },
  { label: "Active vs Expired", route: "/dashboard/active-vs-expired", icon: CheckCircle },
  { label: "Validity Analytics", route: "/dashboard/validity-analytics", icon: CalendarCheck },
  { label: "Signature & Hash", route: "/dashboard/signature-hash", icon: ShieldCheck },
  { label: "CA Analytics", route: "/dashboard/ca-analytics", icon: Building2 },
  { label: "SAN Analytics", route: "/dashboard/san-analytics", icon: ListChecks },
  { label: "Trends", route: "/dashboard/trends", icon: BarChart3 },
  { label: "Type Distribution", route: "/dashboard/type-distribution", icon: PieChart },
  { label: "Issuer Organizations", route: "/dashboard/issuer-organizations", icon: Building },
  { label: "Issuer Countries", route: "/dashboard/issuer-countries", icon: Globe },
  { label: "Subject Names", route: "/dashboard/subject-names", icon: UserCircle2 },
  { label: "CAs vs Domains", route: "/dashboard/cas-vs-domains", icon: Network },
  { label: "CAs vs URLs", route: "/dashboard/cas-vs-urls", icon: LinkIcon },
  { label: "CAs vs Public Keys", route: "/dashboard/cas-vs-public-keys", icon: KeyRound },
  { label: "Shared Public Keys", route: "/dashboard/shared-public-keys", icon: KeySquare },
];


















































// // src/app/dashboard/sidebar.config.ts
// export const sidebarPages = [
//   { label: 'Overview', route: '/dashboard' },
//   { label: 'Active vs Expired', route: '/dashboard/active-vs-expired' },
//   { label: 'Validity Analytics', route: '/dashboard/validity-analytics' },
//   { label: 'Signature & Hash', route: '/dashboard/signature-hash' },
//   { label: 'CA Analytics', route: '/dashboard/ca-analytics' },
//   { label: 'SAN Analytics', route: '/dashboard/san-analytics' },
//   { label: 'Trend', route: '/dashboard/signature-hash1' },
//   { label: 'Type Distribution', route: '/dashboard/ca-analytics1' },
//   { label: 'Issuer Orgainzations', route: '/dashboard/san-analytics1' },
//   { label: 'Issuer Countries', route: '/dashboard/signature-hash2' },
//   { label: 'Subject Names', route: '/dashboard/ca-analytics2' },
//   { label: 'CAs vs Domains', route: '/dashboard/san-analytics2' },
//   { label: 'CAs vs URLs', route: '/signature-hash3' },
//   { label: 'CAs vs Public Keys', route: '/ca-analytics3' },
//   { label: 'Shared Public Keys', route: '/san-analytics3' },
  
//   // ...more items
// ];
