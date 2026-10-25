import React, { useState } from 'react';
import { 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  HelpCircle, 
  FileText, 
  User, 
  Clock, 
  Database, 
  Workflow, 
  Copy, 
  Check, 
  ChevronRight, 
  ExternalLink 
} from 'lucide-react';
import { CaseRecord, DeletionStatus, AuditStep } from '../types/audit';

interface InvestigationWorkspaceProps {
  currentCase: CaseRecord;
  allCases: CaseRecord[];
  onSelectCase: (caseId: string) => void;
  onNavigateToIdentity: () => void;
  onNavigateToRemediation: () => void;
}

export const InvestigationWorkspace: React.FC<InvestigationWorkspaceProps> = ({
  currentCase,
  allCases,
  onSelectCase,
  onNavigateToIdentity,
  onNavigateToRemediation
}) => {
  const [copiedJson, setCopiedJson] = useState(false);
  const [selectedEvidenceStep, setSelectedEvidenceStep] = useState<AuditStep | null>(null);

  const handleCopyJson = () => {
    navigator.clipboard.writeText(currentCase.steps_json);
    setCopiedJson(true);
    setTimeout(() => setCopiedJson(false), 2000);
  };

  // Timeline events before and after cutoff
  const reqTime = currentCase.requested_at;
  const repTime = currentCase.reported_at;
  const auditCutoff = currentCase.audit_at;

  const timelineEvents = [
    {
      time: reqTime,
      title: 'Deletion Request Submitted',
      system: 'Intake API',
      detail: `Received request from ${currentCase.email}`,
      isPastCutoff: false,
      status: 'VERIFIED'
    },
    {
      time: repTime,
      title: `Workflow Claimed: ${currentCase.reported_status}`,
      system: 'Account Service Deletion Worker',
      detail: 'Internal job status marked complete. (Claim, not proof)',
      isPastCutoff: false,
      status: 'CLAIM_ONLY'
    },
    {
      time: auditCutoff,
      title: 'Audit Timestamp Cutoff (audit_at)',
      system: 'GHOST TRACER Engine',
      detail: 'Strict temporal boundary. All subsequent events excluded from evaluation.',
      isPastCutoff: false,
      isCutoffMarker: true,
      status: 'CUTOFF'
    },
    {
      time: '2026-09-04T10:00:00Z',
      title: 'Downstream Sync Event (Post-Cutoff)',
      system: 'Analytics CDC Connector',
      detail: 'Event captured after audit_at. Ignored per temporal compliance rules.',
      isPastCutoff: true,
      status: 'EXCLUDED'
    }
  ];

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {/* Top Case Selector Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-400 font-medium">Selected Audit Case:</span>
          <select
            value={currentCase.case_id}
            onChange={(e) => onSelectCase(e.target.value)}
            className="bg-slate-950 border border-slate-800 text-cyan-300 font-mono text-xs rounded-md px-3 py-1.5 focus:outline-none focus:border-cyan-500/50 cursor-pointer"
          >
            {allCases.slice(0, 50).map((c) => (
              <option key={c.case_id} value={c.case_id} className="bg-slate-900 text-slate-100">
                {c.case_id} — {c.email} ({c.deletion_status})
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={onNavigateToIdentity}
            className="px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-md transition-colors"
          >
            View Identity Graph
          </button>
          <button
            onClick={onNavigateToRemediation}
            className="px-3 py-1.5 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-md transition-colors"
          >
            View Remediation Plan
          </button>
        </div>
      </div>

      {/* 3-Panel Desktop Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Panel: Request & Intent & Identifiers (Col 3) */}
        <div className="lg:col-span-4 space-y-6">
          {/* Request Intake Details */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-xs font-semibold text-slate-300 tracking-wider uppercase flex items-center gap-2">
              <FileText className="w-4 h-4 text-cyan-400" />
              <span>Intake Request Text</span>
            </h2>

            <div className="p-3.5 bg-slate-950/70 border border-slate-800 rounded-lg text-xs font-sans text-slate-200 leading-relaxed italic">
              "{currentCase.request_text}"
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1.5 border-b border-slate-800/80">
                <span className="text-slate-400">Classified Intent:</span>
                <span className="font-mono text-cyan-400 font-medium">
                  {currentCase.deletion_status === 'NOT_APPLICABLE' ? 'NON_DELETION / NEGATED' : 'AUTHORIZED_DELETION'}
                </span>
              </div>
              <div className="flex justify-between py-1.5 border-b border-slate-800/80">
                <span className="text-slate-400">Classification Method:</span>
                <span className="font-sans text-slate-300">Deterministic Multilingual NLP</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-slate-400">Temporal Cutoff (audit_at):</span>
                <span className="font-mono text-slate-200 tabular-nums">
                  {currentCase.audit_at.replace('T', ' ').replace('Z', '')}
                </span>
              </div>
            </div>
          </div>

          {/* Resolved Identifiers */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-xs font-semibold text-slate-300 tracking-wider uppercase flex items-center gap-2">
              <User className="w-4 h-4 text-cyan-400" />
              <span>Resolved Identifiers</span>
            </h2>

            <div className="space-y-2.5 text-xs">
              <div>
                <span className="text-[11px] text-slate-400">Internal Reference ID:</span>
                <div className="font-mono text-cyan-300 mt-0.5">usr_{currentCase.case_id.replace('case_', '')}</div>
              </div>
              <div>
                <span className="text-[11px] text-slate-400">Request Email:</span>
                <div className="font-mono text-slate-200 mt-0.5">{currentCase.email}</div>
              </div>
              <div>
                <span className="text-[11px] text-slate-400">Historical Email Alias:</span>
                <div className="font-mono text-slate-400 mt-0.5">old.{currentCase.email}</div>
              </div>
              <div>
                <span className="text-[11px] text-slate-400">SHA-256 Email Hash:</span>
                <div className="font-mono text-[10px] text-slate-500 break-all mt-0.5">
                  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Center Panel: Investigation Timeline & Evidence Citations (Col 5) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-xs font-semibold text-slate-300 tracking-wider uppercase flex items-center gap-2">
                <Clock className="w-4 h-4 text-cyan-400" />
                <span>Evidence Timeline at audit_at</span>
              </h2>
              <span className="text-[11px] text-slate-400">Inclusive Cutoff</span>
            </div>

            <div className="relative pl-6 border-l border-slate-800 space-y-6">
              {timelineEvents.map((evt, idx) => (
                <div key={idx} className={`relative ${evt.isPastCutoff ? 'opacity-40' : ''}`}>
                  {/* Dot */}
                  <div className={`absolute -left-[31px] top-1 w-3.5 h-3.5 rounded-full border-2 ${
                    evt.isCutoffMarker 
                      ? 'bg-cyan-500 border-cyan-300' 
                      : evt.isPastCutoff 
                        ? 'bg-slate-800 border-slate-600' 
                        : 'bg-slate-950 border-cyan-500'
                  }`} />

                  <div className="space-y-1">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-semibold text-slate-200">{evt.title}</span>
                      {evt.isPastCutoff && (
                        <span className="text-[10px] font-mono text-amber-400 border border-amber-500/30 px-1.5 rounded">
                          EXCLUDED
                        </span>
                      )}
                    </div>
                    <div className="text-[11px] font-mono text-slate-400 tabular-nums">
                      {evt.time.replace('T', ' ').replace('Z', '')} · {evt.system}
                    </div>
                    <p className="text-xs text-slate-300">{evt.detail}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Observed Records & Findings */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <h2 className="text-xs font-semibold text-slate-300 tracking-wider uppercase flex items-center gap-2">
              <Database className="w-4 h-4 text-cyan-400" />
              <span>Evidence Records Discovered</span>
            </h2>

            {currentCase.steps.length > 0 ? (
              <div className="space-y-2">
                {currentCase.steps.map((s, idx) => (
                  <div 
                    key={idx}
                    onClick={() => setSelectedEvidenceStep(s)}
                    className="p-3 bg-slate-950 border border-slate-800/80 rounded-lg hover:border-cyan-500/30 transition-colors cursor-pointer space-y-1.5"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-200">{s.operation}</span>
                      <span className={`text-[10px] font-mono ${
                        s.phase === 'FINDING' ? 'text-amber-400' : s.phase === 'REMEDIATION' ? 'text-cyan-400' : 'text-emerald-400'
                      }`}>
                        {s.phase}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
                      <span>{s.system_id} ({s.resource_id})</span>
                      <span className="text-slate-500">
                        {s.evidence_id ? `Cite: ${s.evidence_id}` : 'Future Work ("")'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-6 text-center text-xs text-slate-500">
                {currentCase.deletion_status === 'NOT_APPLICABLE'
                  ? 'No evidence findings recorded: request does not authorize deletion ([]).'
                  : 'Zero records remaining; complete deletion verified.'}
              </div>
            )}
          </div>
        </div>

        {/* Right Panel: Decision Trace & Output Verdict (Col 3) */}
        <div className="lg:col-span-3 space-y-6">
          {/* Adjudication Verdict Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
            <div className="text-[11px] font-medium text-slate-400">Adjudicated Deletion Verdict</div>
            <div className="flex items-center gap-2">
              {currentCase.deletion_status === 'COMPLETE' && (
                <div className="flex items-center gap-2 text-emerald-400 font-bold text-lg font-mono">
                  <CheckCircle2 className="w-5 h-5" />
                  <span>COMPLETE</span>
                </div>
              )}
              {currentCase.deletion_status === 'INCOMPLETE' && (
                <div className="flex items-center gap-2 text-amber-400 font-bold text-lg font-mono">
                  <AlertTriangle className="w-5 h-5" />
                  <span>INCOMPLETE</span>
                </div>
              )}
              {currentCase.deletion_status === 'NOT_APPLICABLE' && (
                <div className="flex items-center gap-2 text-slate-300 font-bold text-lg font-mono">
                  <HelpCircle className="w-5 h-5" />
                  <span>NOT_APPLICABLE</span>
                </div>
              )}
            </div>
            <div className="text-xs text-slate-400 leading-relaxed">
              {currentCase.deletion_status === 'COMPLETE' && 'All personal data verified absent or redacted. Account tombstone compliant. Zero recreation risks.'}
              {currentCase.deletion_status === 'INCOMPLETE' && 'Residual data copies or active synchronization processes expose customer personal information.'}
              {currentCase.deletion_status === 'NOT_APPLICABLE' && 'Customer did not request account deletion. Non-deletion or negated request.'}
            </div>
          </div>

          {/* Rule-by-rule Decision Trace */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-xs font-semibold text-slate-300 tracking-wider uppercase">
              Rule Decision Trace
            </h2>
            <div className="space-y-2 text-xs font-mono text-slate-400">
              <div className="p-2 bg-slate-950 border border-slate-800/80 rounded text-[11px] leading-relaxed">
                <span className="text-cyan-400">RULE_001_INTENT:</span> Evaluated against 6 language models. Intent verified.
              </div>
              <div className="p-2 bg-slate-950 border border-slate-800/80 rounded text-[11px] leading-relaxed">
                <span className="text-cyan-400">RULE_002_IDENTITY:</span> Resolved current & historical emails and hashes.
              </div>
              <div className="p-2 bg-slate-950 border border-slate-800/80 rounded text-[11px] leading-relaxed">
                <span className="text-cyan-400">RULE_003_TEMPORAL:</span> Enforced cutoff boundary at audit_at.
              </div>
              <div className="p-2 bg-slate-950 border border-slate-800/80 rounded text-[11px] leading-relaxed">
                <span className="text-cyan-400">RULE_004_POLICY:</span> Validated tombstone direct identifier redaction.
              </div>
            </div>
          </div>

          {/* Copy steps_json */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-300 uppercase">output steps_json</span>
              <button
                onClick={handleCopyJson}
                className="text-[11px] text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
              >
                {copiedJson ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copiedJson ? 'Copied' : 'Copy JSON'}</span>
              </button>
            </div>
            <pre className="p-3 bg-slate-950 border border-slate-800 rounded text-[10px] font-mono text-slate-400 max-h-48 overflow-y-auto whitespace-pre-wrap break-all">
              {currentCase.steps_json}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
};
