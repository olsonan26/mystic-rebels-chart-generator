export type ObjectEntry = {
  id: string;
  name: string;
  glyph: string;
  group: string;
  available: boolean;
  reason?: string;
};
export type BirthInput = {
  name: string;
  local_date: string;
  local_time: string | null;
  timezone: string;
  fold: 0 | 1 | null;
  latitude: number;
  longitude: number;
  location_name: string;
  coordinate_provenance: string;
  time_accuracy:
    "recorded_second" | "nearest_minute" | "approximate" | "unknown";
  uncertainty_seconds: number | null;
  objects: string[];
  chart_type: "natal" | "dual";
};
export type Point = ObjectEntry & {
  longitude_deg: number | null;
  latitude_deg?: number;
  declination_deg?: number;
  speed_longitude_deg_per_day?: number;
  distance_au?: number;
  retrograde: boolean | null;
  // Optional research metadata. Never synthesize undocumented PRE/POST phases.
  motion_status?: "Direct" | "Retrograde" | "Stationary" | "Unknown";
  gradity_phase?: "Prograde" | "Pregrade" | "Retrograde" | "Postgrade" | null;
  gradity_source_status?: "EXPLICIT" | "VERIFIED_EXAMPLE" | "DERIVED" | "UNKNOWN";
  gradity?: {
    phase: "Prograde" | "Pregrade" | "Retrograde" | "Postgrade" | null;
    status: "VERIFIED" | "UNAVAILABLE" | "BOUNDARY" | "NOT_APPLICABLE";
    reason: string;
    events?: Record<string, unknown>[];
    verification_scope?: string;
    source?: {
      pdf_pages?: number[];
      reflow_pages?: number[];
      original_printed_pages?: number[];
      [key: string]: unknown;
    };
    [key: string]: unknown;
  };
  sign: string;
  sign_index: number;
  degree_in_sign: number;
  house: number | null;
  tone: string;
  pulse: string;
  field: string | null;
  display_dms: string;
  error?: { code: string; message: string };
  provenance: Record<string, unknown>;
};
export type Chart = {
  chart_id: string;
  input: BirthInput;
  points: Point[];
  angles: Record<string, number>;
  whole_sign_cusps: number[];
  warnings: { code: string; message: string }[];
  configuration: Record<string, unknown>;
  time: {
    birth_utc: string;
    iana_zone: string;
    uncertainty_seconds: number | null;
    time_is_reference_only: boolean;
    [key: string]: unknown;
  };
  rules: Record<string, unknown>;
  [key: string]: unknown;
};
export type Location = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  timezone: string;
  provenance: string;
};
