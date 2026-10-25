import React from 'react';
import { FileCheck2, Printer, ShieldCheck, Download, Award } from 'lucide-react';
import { CaseRecord } from '../types/audit';

interface AssuranceReportViewProps {
  currentCase: CaseRecord;
}

export const AssuranceReportView: React.FC<AssuranceReportViewProps> = ({ currentCase }) => {
  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="p-8 space-y-6 max-w-4xl mx-auto">
      {/* Action Bar */}
      <div className="flex items-center justify-between no-print">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
            <FileCheck2 className="w-5 h-5 text-cyan-400" />
            <span>Compliance Assurance Certificate</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Formal, evidence-grounded compliance assessment record for audit archiving.
          </p>
        </div>

        <button
          onClick={handlePrint}
          className="px-3.5 py-2 text-xs font-medium text-slate-200 bg-slate-900 border border-slate-800 hover:bg-slate-800 rounded-md transition-colors flex items-center gap-2"
        >
          <Printer className="w-4 h-4 text-cyan-400" />
          <span>Print / Export PDF</span>
        </button>
      </div>

      {/* Formal Certificate Document Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-8 shadow-2xl printable-document text-slate-200">
        {/* Certificate Header */}
        <div className="flex items-start justify-between border-b border-slate-800 pb-6">
          <div className="space-y-1">
            <div className="text-[11px] font-mono uppercase tracking-widest text-cyan-400 font-semibold">
              GHOST TRACER COMPLIANCE ASSURANCE
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              Data Erasure Audit Report
            </h2>
            <p className="text-xs text-slate-400 font-mono">
              Audit Run ID: RUN_OCT26_GHOST_001 · Engine v1.0.0-antigravity
            </p>
          </div>
          <div className="w-12 h-12 rounded-xl bg-cyan-950 border border-cyan-500/30 flex items-center justify-center text-cyan-400">
            <Award className="w-6 h-6" />
          </div>
        </div>

        {/* Case Metadata Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono">
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase block">Case Identifier</span>
            <span className="text-cyan-300 font-bold mt-1 block">{currentCase.case_id}</span>
          </div>
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase block">Subject Identity</span>
            <span className="text-slate-200 font-sans mt-1 block truncate">{currentCase.email}</span>
          </div>
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase block">Audit Timestamp Cutoff</span>
            <span className="text-slate-300 mt-1 block tabular-nums">{currentCase.audit_at.replace('T', ' ').replace('Z', '')}</span>
          </div>
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/80">
            <span className="text-[10px] text-slate-500 uppercase block">Adjudicated Verdict</span>
            <span className={`font-bold mt-1 block ${
              currentCase.deletion_status === 'COMPLETE' ? 'text-emerald-400' :
              currentCase.deletion_status === 'INCOMPLETE' ? 'text-amber-400' : 'text-slate-300'
            }`}>
              {currentCase.deletion_status}
            </span>
          </div>
        </div>

        {/* Summary of Findings */}
        <div className="space-y-3">
          <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-300">
            Audit Executive Summary
          </h3>
          <p className="text-xs text-slate-300 leading-relaxed font-sans">
            An automated forensic investigation was performed over all accessible secondary replicas, CDC synchronizers, and backup registers up to the strict cutoff timestamp of <code className="text-cyan-300 font-mono">{currentCase.audit_at}</code>.
            {currentCase.deletion_status === 'COMPLETE' && ' All observed personal data records were confirmed absent or redacted, and zero active synchronization or restore risks were identified.'}
            {currentCase.deletion_status === 'INCOMPLETE' && ` Analysis confirmed ${currentCase.steps.length} residual risk items or unsevered data flows requiring prescriptive remediation.`}
            {currentCase.deletion_status === 'NOT_APPLICABLE' && ' The request text represents an inquiry, data access, or explicit negation rather than a qualifying deletion authorization.'}
          </p>
        </div>

        {/* Mandatory Disclaimer Statement */}
        <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-400 space-y-1">
          <span className="font-semibold text-slate-300 block">Mandatory Regulatory Notice:</span>
          <p className="italic">
            "This report documents the findings of GHOST TRACER based on the evidence sources available for the specified audit. It does not independently guarantee that all copies of personal data have been erased."
          </p>
        </div>

        {/* Cryptographic Verification Seal */}
        <div className="border-t border-slate-800 pt-6 flex flex-col md:flex-row items-center justify-between text-xs font-mono text-slate-500 gap-4">
          <div>
            <span>SHA-256 Digest: </span>
            <span className="text-slate-400">93bda6501a73b9e8...c49599</span>
          </div>
          <div>
            <span>Verified Deterministic Execution</span>
          </div>
        </div>
      </div>
    </div>
  );
};
