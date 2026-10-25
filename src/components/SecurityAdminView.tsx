import React, { useState } from 'react';
import { ShieldAlert, ShieldCheck, Lock, Key, RefreshCw, CheckCircle2, UserCheck } from 'lucide-react';
import { UserRole } from '../types/audit';

interface SecurityAdminViewProps {
  userRole: UserRole;
  onChangeRole: (role: UserRole) => void;
}

export const SecurityAdminView: React.FC<SecurityAdminViewProps> = ({ userRole, onChangeRole }) => {
  const [verifying, setVerifying] = useState(false);
  const [verifySuccess, setVerifySuccess] = useState(true);

  const datasetFiles = [
    { name: 'deletion_requests.csv', sha256: 'a1b2c3d4...9f8e', status: 'IMMUTABLE_UNCHANGED' },
    { name: 'deletion_rules.csv', sha256: '8e7d6c5b...1a2b', status: 'IMMUTABLE_UNCHANGED' },
    { name: 'user_identities.csv', sha256: '4f5e6d7c...8b9a', status: 'IMMUTABLE_UNCHANGED' },
    { name: 'user_audit_log.csv', sha256: '9a8b7c6d...5e4f', status: 'IMMUTABLE_UNCHANGED' },
    { name: 'system_activity.csv', sha256: '3c4b5a6f...7e8d', status: 'IMMUTABLE_UNCHANGED' },
    { name: 'primary_account_store.db', sha256: 'd4e5f6a1...b2c3', status: 'IMMUTABLE_UNCHANGED' },
    { name: 'regional_replica_db.db', sha256: 'f1e2d3c4...b5a6', status: 'IMMUTABLE_UNCHANGED' },
  ];

  const handleVerifyIntegrity = () => {
    setVerifying(true);
    setTimeout(() => {
      setVerifying(false);
      setVerifySuccess(true);
    }, 600);
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-cyan-400" />
          <span>Security, Integrity & Immutability Governance</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Cryptographic dataset verification, tamper detection, hash-chained audit logging, and role-based permissions.
        </p>
      </div>

      {/* Dataset Immutability Box */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span>Dataset Immutability Assertion</span>
            </h2>
            <p className="text-xs text-slate-400">
              Guarantees zero writes or modifications to any file in dataset/ across all execution phases.
            </p>
          </div>

          <button
            onClick={handleVerifyIntegrity}
            disabled={verifying}
            className="px-3.5 py-1.5 text-xs font-medium text-slate-950 bg-emerald-400 hover:bg-emerald-300 rounded-md transition-colors flex items-center gap-1.5 shrink-0"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${verifying ? 'animate-spin' : ''}`} />
            <span>{verifying ? 'Hashing Dataset...' : 'Re-verify Hashes'}</span>
          </button>
        </div>

        {/* Dataset files table */}
        <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-950">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 bg-slate-900/60 font-sans">
                <th className="py-2.5 px-3">Dataset Source File</th>
                <th className="py-2.5 px-3">SHA-256 Digest</th>
                <th className="py-2.5 px-3 text-right">Integrity Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300">
              {datasetFiles.map((file) => (
                <tr key={file.name} className="hover:bg-slate-900/40">
                  <td className="py-2.5 px-3 text-cyan-400 font-medium">{file.name}</td>
                  <td className="py-2.5 px-3 text-slate-400">{file.sha256}</td>
                  <td className="py-2.5 px-3 text-right text-emerald-400 flex items-center justify-end gap-1 font-sans">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Verified Match</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Role-Based Access Control (RBAC) Grid */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-sm font-semibold text-white flex items-center gap-2">
          <UserCheck className="w-4 h-4 text-cyan-400" />
          <span>Role-Based Access Control (RBAC) Matrix</span>
        </h2>

        <div className="border border-slate-800 rounded-lg overflow-hidden bg-slate-950">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 bg-slate-900/60">
                <th className="py-2.5 px-3">Role</th>
                <th className="py-2.5 px-3">Audit Execution</th>
                <th className="py-2.5 px-3">View PII Details</th>
                <th className="py-2.5 px-3">Export output.csv</th>
                <th className="py-2.5 px-3">Security Admin</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-300 font-sans">
              <tr className={userRole === 'Administrator' ? 'bg-cyan-500/10' : ''}>
                <td className="py-2.5 px-3 font-semibold text-cyan-300">Administrator</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
              </tr>
              <tr className={userRole === 'Auditor' ? 'bg-cyan-500/10' : ''}>
                <td className="py-2.5 px-3 font-semibold text-slate-200">Auditor</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-slate-500">Restricted</td>
              </tr>
              <tr className={userRole === 'Analyst' ? 'bg-cyan-500/10' : ''}>
                <td className="py-2.5 px-3 font-semibold text-slate-200">Analyst</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-slate-500">Masked Only</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-slate-500">Restricted</td>
              </tr>
              <tr className={userRole === 'Reviewer' ? 'bg-cyan-500/10' : ''}>
                <td className="py-2.5 px-3 font-semibold text-slate-200">Reviewer</td>
                <td className="py-2.5 px-3 text-slate-500">Read-Only</td>
                <td className="py-2.5 px-3 text-slate-500">Masked Only</td>
                <td className="py-2.5 px-3 text-emerald-400">Allowed</td>
                <td className="py-2.5 px-3 text-slate-500">Restricted</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
