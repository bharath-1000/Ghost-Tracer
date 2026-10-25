export type DeletionStatus = 'COMPLETE' | 'INCOMPLETE' | 'NOT_APPLICABLE';
export type PhaseType = 'FINDING' | 'REMEDIATION' | 'VERIFICATION';
export type UserRole = 'Administrator' | 'Auditor' | 'Analyst' | 'Reviewer';

export interface AuditStep {
  step_no: number;
  phase: PhaseType;
  system_id: string;
  resource_id: string;
  operation: string;
  state: string;
  evidence_id: string;
}

export interface CaseRecord {
  case_id: string;
  email: string;
  requested_at: string;
  reported_status: string;
  reported_at: string;
  audit_at: string;
  request_text: string;
  deletion_status: DeletionStatus;
  steps_json: string;
  steps: AuditStep[];
}

export interface IdentityProfile {
  user_id: string;
  name: string;
  email: string;
  phone: string;
  email_hash: string;
  updated_at: string;
  historical_emails?: string[];
  historical_phones?: string[];
}

export interface EvidenceFile {
  file_id: string;
  file_path: string;
  system_id: string;
  captured_at: string;
  file_type: string;
  status: string;
}

export interface OverviewMetrics {
  total_cases: number;
  complete_count: number;
  incomplete_count: number;
  not_applicable_count: number;
  false_complete_count: number;
  status_accuracy: number;
  total_findings: number;
  total_lifecycle_risks: number;
  audit_coverage: number;
  avg_latency_ms: number;
}
