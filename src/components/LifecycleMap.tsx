import React from 'react';
import { Workflow, Database, RefreshCw, Archive, AlertTriangle, ShieldCheck, ArrowRight } from 'lucide-react';

export const LifecycleMap: React.FC = () => {
  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <Workflow className="w-5 h-5 text-cyan-400" />
          <span>Data Lifecycle & Recreation Risk Topology</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Tracking how personal data flows across primary datastores, asynchronous CDC pipelines, replicas, and backup restore points.
        </p>
      </div>

      {/* Visual Topology Diagram */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-center">
          {/* Node 1: Primary Account Service */}
          <div className="p-5 bg-slate-950 border border-cyan-500/30 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono text-cyan-400 font-semibold tracking-wider uppercase">Origin Store</span>
              <Database className="w-4 h-4 text-cyan-400" />
            </div>
            <h3 className="text-sm font-semibold text-white">Primary Account DB</h3>
            <p className="text-[11px] text-slate-400">
              User profile erased; compliant tombstone maintained with user_id.
            </p>
            <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-emerald-400">
              STATUS: ERASED_COMPLIANT
            </div>
          </div>

          {/* Node 2: CDC Sync Connector (Recreation Risk) */}
          <div className="p-5 bg-slate-950 border border-amber-500/40 rounded-xl space-y-3 relative">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono text-amber-400 font-semibold tracking-wider uppercase">CDC Sync Flow</span>
              <RefreshCw className="w-4 h-4 text-amber-400 animate-spin" />
            </div>
            <h3 className="text-sm font-semibold text-white">Analytics Sync Connector</h3>
            <p className="text-[11px] text-slate-400">
              Asynchronous pipeline still listening to user CDC stream at audit_at.
            </p>
            <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-amber-400 font-bold flex items-center gap-1">
              <AlertTriangle className="w-3 h-3" />
              <span>RECREATION RISK ACTIVE</span>
            </div>
          </div>

          {/* Node 3: Regional Replicas (Replication Drift) */}
          <div className="p-5 bg-slate-950 border border-amber-500/40 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono text-amber-400 font-semibold tracking-wider uppercase">Secondary Replica</span>
              <Database className="w-4 h-4 text-amber-400" />
            </div>
            <h3 className="text-sm font-semibold text-white">Regional Replica DB</h3>
            <p className="text-[11px] text-slate-400">
              Replication lag caused user record to remain in read-only node.
            </p>
            <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-amber-400">
              REPLICATION DRIFT DETECTED
            </div>
          </div>

          {/* Node 4: Backup Restore Manager */}
          <div className="p-5 bg-slate-950 border border-slate-800 rounded-xl space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono text-slate-400 font-semibold tracking-wider uppercase">Disaster Recovery</span>
              <Archive className="w-4 h-4 text-slate-400" />
            </div>
            <h3 className="text-sm font-semibold text-white">Automated Backups</h3>
            <p className="text-[11px] text-slate-400">
              Recovery snapshots staged for restore testing without exclusion filter.
            </p>
            <div className="pt-2 border-t border-slate-800 text-[10px] font-mono text-slate-400">
              RESTORE BLOCK REQUIRED
            </div>
          </div>
        </div>

        {/* Remediation Sequencing Guidance */}
        <div className="p-4 bg-slate-950/60 border border-slate-800 rounded-lg text-xs text-slate-400 space-y-2">
          <span className="font-semibold text-slate-200">Enforced Remediation Dependency Order:</span>
          <p className="leading-relaxed">
            Per the challenge rules, active recreation pipelines must be severed (<code className="text-cyan-300">DISABLE_DATA_FLOW</code>) and recovery overwrites quarantined (<code className="text-cyan-300">BLOCK_RESTORE</code>) BEFORE secondary record deletions are executed. Otherwise, active connectors will immediately regenerate ghost data upon deletion.
          </p>
        </div>
      </div>
    </div>
  );
};
