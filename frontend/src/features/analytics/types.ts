
export type CategoryPerformance = {
  category: string;
  views: number;
  registrations: number;
  ad_spend: number;
  conversion_rate: number;
  cost_per_registration: number | null;
};

export type PerformanceReport = {
  period_start: string;
  period_end: string;
  total_views: number;
  total_registrations: number;
  total_ad_spend: number;
  overall_conversion_rate: number;
  categories: CategoryPerformance[];
};
