import React, { useState } from 'react';
import { ListOrdered, Copy, Check, Download, AlertOctagon, ShieldCheck } from 'lucide-react';
import { CaseRecord, AuditStep } from '../types/audit';

interface RemediationPlannerViewProps {
  currentCase: CaseRecord;
}

export const RemediationPlannerView: React.FC<RemediationPlannerViewProps> = ({ currentCase }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCase.steps_json);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="p-8 space-y-6 max-w-7xl mx-auto">
      {/* Non-Negotiable Boundary Banner */}
      <div className="bg-amber-950/40 border border-amber-500/30 rounded-xl p-4 flex items-start gap-3">
        <AlertOctagon className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
        <div className="space-y-0.5 text-xs">
          <span className="font-semibold text-amber-300">
            Recommendations Only — Zero Execution Boundary
          </span>
          <p className="text-amber-200/80 leading-relaxed">
            GHOST TRACER is strictly an audit system. It never executes deletions, redactions, or pipeline mutations. All remediation steps are prescriptive recommendations for Northstar Shop's engineering teams.
          </p>
        </div>
      </div>

      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <ListOrdered className="w-5 h-5 text-cyan-400" />
            <span>Ordered Remediation & Verification Plan: {currentCase.case_id}</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Official 7-key JSON representation sorted by Phase, Operation order, system_id, and resource_id.
          </p>
        </div>

        <button
          onClick={handleCopy}
          className="px-3.5 py-1.5 text-xs font-medium bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-200 rounded-md transition-colors flex items-center gap-2"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied Steps JSON' : 'Copy Steps JSON'}</span>
        </button>
      </div>

      {/* Step Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {currentCase.steps.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 bg-slate-950/40 font-medium">
                  <th className="py-3 px-4 w-16">Step #</th>
                  <th className="py-3 px-4 w-28">Phase</th>
                  <th className="py-3 px-4">System ID</th>
                  <th className="py-3 px-4">Resource ID</th>
                  <th className="py-3 px-4">Operation</th>
                  <th className="py-3 px-4">State</th>
                  <th className="py-3 px-4">Evidence Citation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-mono text-slate-300">
                {currentCase.steps.map((step) => (
                  <tr key={step.step_no} className="hover:bg-slate-800/40">
                    <td className="py-3 px-4 text-cyan-400 font-bold">{step.step_no}</td>
                    <td className="py-3 px-4 font-sans">
                      <span className={`text-[11px] font-semibold ${
                        step.phase === 'FINDING' ? 'text-amber-400' :
                        step.phase === 'REMEDIATION' ? 'text-cyan-400' : 'text-emerald-400'
                      }`}>
                        {step.phase}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-slate-200">{step.system_id}</td>
                    <td className="py-3 px-4 text-slate-400">{step.resource_id}</td>
                    <td className="py-3 px-4 font-semibold text-slate-200">{step.operation}</td>
                    <td className="py-3 px-4 text-slate-300">{step.state}</td>
                    <td className="py-3 px-4">
                      {step.evidence_id ? (
                        <span className="text-cyan-400 bg-cyan-950/60 border border-cyan-500/30 px-2 py-0.5 rounded text-[11px]">
                          {step.evidence_id}
                        </span>
                      ) : (
                        <span className="text-slate-600 italic">"" (Future Action)</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-12 text-center text-xs text-slate-500 font-sans space-y-2">
            <ShieldCheck className="w-8 h-8 text-slate-600 mx-auto" />
            <p className="font-medium text-slate-400">
              {currentCase.deletion_status === 'NOT_APPLICABLE'
                ? 'No remediation plan: Request does not authorize deletion ([]).'
                : 'Zero outstanding findings: Case verified complete.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
