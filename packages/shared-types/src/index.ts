// Shared TS types for Studio + future SDKs. V1 auto-generates from
// Pydantic via datamodel-code-generator -> JSON Schema -> json-schema-to-typescript.

export type DebateMode = "research" | "publication";

export interface DebateRequest {
  topic: string;
  language?: string;
  n_agents?: number;
  cluster_size?: number;
  rounds?: number;
  mode?: DebateMode;
  persona_library_version?: string;
  weights_version?: string;
}

export interface DebateResponse {
  debate_id: string;
  topic: string;
  article: string;
  conclusive_remark: string;
  persona_library_version: string;
  weights_version: string;
  n_personas: number;
  minority_voice_fraction?: number;
  cost_usd?: number;
  latency_ms?: number;
}
