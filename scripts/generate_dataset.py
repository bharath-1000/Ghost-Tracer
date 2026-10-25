#!/usr/bin/env python3
"""
Generates the benchmark challenge dataset inside dataset/ with realistic
identity graphs, operational activity, deletion rules, evidence files,
sample cases (32), and evaluation cases (518) matching HackerRank Orchestrate specs.
"""

import os
import csv
import json
import hashlib
from datetime import datetime, timedelta

def get_hash(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode("utf-8")).hexdigest()

def ensure_dirs():
    os.makedirs("dataset", exist_ok=True)
    os.makedirs("dataset/evidence/databases", exist_ok=True)
    os.makedirs("dataset/evidence/logs", exist_ok=True)
    os.makedirs("dataset/evidence/records", exist_ok=True)
    os.makedirs("dataset/evidence/documents", exist_ok=True)
    os.makedirs("dataset/evidence/images", exist_ok=True)

def generate_rules():
    rules = [
        {"rule_id": "rule_01", "data_category": "ACCOUNT_PROFILE", "required_treatment": "DELETE", "conditions": "Standard account closure", "notes": "Remove user profile from primary store"},
        {"rule_id": "rule_02", "data_category": "ACCOUNT_TOMBSTONE", "required_treatment": "REDACT", "conditions": "Retain user_id; strip name, email, phone, email_hash", "notes": "Preserve internal FK consistency"},
        {"rule_id": "rule_03", "data_category": "ORDER_HISTORY", "required_treatment": "ANONYMIZE", "conditions": "Financial audit compliance (7 years)", "notes": "Strip direct PII, preserve transaction totals"},
        {"rule_id": "rule_04", "data_category": "SUPPORT_TICKETS", "required_treatment": "DELETE", "conditions": "Customer service conversation transcripts", "notes": "Purge tickets and attachments"},
        {"rule_id": "rule_05", "data_category": "MARKETING_PROFILES", "required_treatment": "DELETE", "conditions": "Advertising and behavioral trackers", "notes": "Purge audience segments and device tokens"},
        {"rule_id": "rule_06", "data_category": "SEARCH_INDEX", "required_treatment": "DELETE", "conditions": "Customer catalog search cache", "notes": "Evict index documents"},
        {"rule_id": "rule_07", "data_category": "APPLICATION_LOGS", "required_treatment": "REDACT", "conditions": "Security and diagnostic logs", "notes": "Scrub identifiers, retain trace IDs"},
        {"rule_id": "rule_08", "data_category": "DATA_FLOW_SYNC", "required_treatment": "DISABLE_DATA_FLOW", "conditions": "Active connectors to downstream sinks", "notes": "Sever synchronization before deletion"},
        {"rule_id": "rule_09", "data_category": "BACKUP_RESTORE_RISK", "required_treatment": "BLOCK_RESTORE", "conditions": "Unscrubbed recovery snapshots", "notes": "Prevent restore overwrite"},
        {"rule_id": "rule_10", "data_category": "PAYMENT_RECORDS", "required_treatment": "RETAIN", "conditions": "Tax and AML regulatory hold", "notes": "Retain anonymized payment ledgers"}
    ]
    with open("dataset/deletion_rules.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rule_id", "data_category", "required_treatment", "conditions", "notes"])
        writer.writeheader()
        writer.writerows(rules)

def generate_sample_cases():
    sample_requests = [
        # NOT_APPLICABLE cases (non-deletion, access, opt-out, correction, negation)
        {"case_id": "case_001", "email": "clara.oswald@example.com", "requested_at": "2026-09-01T10:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T10:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Please send me a copy of all my purchase history and personal data."},
        {"case_id": "case_002", "email": "marcos.silva@example.com", "requested_at": "2026-09-01T11:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T11:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Quiero cancelar mi suscripción al boletín de noticias, pero mantener mi cuenta activa."},
        {"case_id": "case_003", "email": "lucas.bernard@example.com", "requested_at": "2026-09-01T12:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T12:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Je souhaite modifier mon adresse de livraison pour ma prochaine commande."},
        {"case_id": "case_004", "email": "jinwoo.park@example.com", "requested_at": "2026-09-01T13:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T13:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "비밀번호를 재설정하고 싶습니다. 계정을 삭제하지 마세요."},
        {"case_id": "case_005", "email": "kenji.sato@example.com", "requested_at": "2026-09-01T14:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T14:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "メールマガジンの配信を停止してください。"},
        {"case_id": "case_006", "email": "beatriz.souza@example.com", "requested_at": "2026-09-01T15:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T15:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Por favor, NÃO apague a minha conta. Foi um engano."},
        {"case_id": "case_007", "email": "arthur.dent@example.com", "requested_at": "2026-09-01T16:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T16:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "I withdrew my earlier deletion request. Please keep my profile active."},
        {"case_id": "case_008", "email": "elena.rostova@example.com", "requested_at": "2026-09-01T17:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-01T17:05:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "How do I update my payment credit card details on file?"},

        # COMPLETE cases (verified complete, tombstones compliant, proof in snapshots)
        {"case_id": "case_009", "email": "sarah.connor@example.com", "requested_at": "2026-09-02T08:00:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T09:00:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Please permanently erase my account and all personal information under GDPR Article 17."},
        {"case_id": "case_010", "email": "david.ross@example.com", "requested_at": "2026-09-02T08:30:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T09:30:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Delete my user profile and order data immediately."},
        {"case_id": "case_011", "email": "camille.dupont@example.com", "requested_at": "2026-09-02T09:00:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T10:00:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Supprimez définitivement mon compte et toutes mes données personnelles s'il vous plaît."},
        {"case_id": "case_012", "email": "rodrigo.alves@example.com", "requested_at": "2026-09-02T09:30:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T10:30:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Solicito a exclusão total dos meus dados pessoais conforme a LGPD."},
        {"case_id": "case_013", "email": "hannah.schmidt@example.com", "requested_at": "2026-09-02T10:00:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T11:00:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Please delete my account and anonymize past transactions."},
        {"case_id": "case_014", "email": "yuki.tanaka@example.com", "requested_at": "2026-09-02T10:30:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T11:30:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "個人情報保護法に基づき、私のアカウントおよび個人データをすべて削除してください。"},
        {"case_id": "case_015", "email": "minjun.kim@example.com", "requested_at": "2026-09-02T11:00:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T11:45:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "제 계정과 관련된 모든 정보를 완전히 삭제해 주시기 바랍니다."},
        {"case_id": "case_016", "email": "gabriel.moreno@example.com", "requested_at": "2026-09-02T11:15:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-02T11:50:00Z", "audit_at": "2026-09-02T12:00:00Z", "request_text": "Deseo borrar mi cuenta y eliminar cualquier dato personal registrado."},

        # INCOMPLETE cases (residual records, exposed PII, active sync, or restore risk)
        {"case_id": "case_017", "email": "alice.wong@example.com", "requested_at": "2026-09-03T08:00:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T08:30:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Please delete my account and all personal details."},
        {"case_id": "case_018", "email": "bob.miller@example.com", "requested_at": "2026-09-03T08:15:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T08:45:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Erase all my data from your systems."},
        {"case_id": "case_019", "email": "claire.fontaine@example.com", "requested_at": "2026-09-03T08:30:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T09:00:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Veuillez supprimer mon profil et toutes informations me concernant."},
        {"case_id": "case_020", "email": "diego.torres@example.com", "requested_at": "2026-09-03T08:45:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T09:15:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Solicito la baja de mi cuenta y borrado total de registros."},
        {"case_id": "case_021", "email": "emma.watson@example.com", "requested_at": "2026-09-03T09:00:00Z", "reported_status": "PARTIALLY_COMPLETE", "reported_at": "2026-09-03T09:30:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Kindly remove my customer account and mailing preferences."},
        {"case_id": "case_022", "email": "felipe.santos@example.com", "requested_at": "2026-09-03T09:15:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T09:45:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Favor excluir definitivamente meu cadastro."},
        {"case_id": "case_023", "email": "grace.hopper@example.com", "requested_at": "2026-09-03T09:30:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T10:00:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Delete my user profile completely."},
        {"case_id": "case_024", "email": "haruto.suzuki@example.com", "requested_at": "2026-09-03T09:45:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T10:15:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "アカウントの完全な削除をお願いします。"},
        {"case_id": "case_025", "email": "isabella.rossi@example.com", "requested_at": "2026-09-03T10:00:00Z", "reported_status": "NOT_STARTED", "reported_at": "2026-09-03T10:05:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "I want to delete my account and all associated data."},
        {"case_id": "case_026", "email": "jihoon.lee@example.com", "requested_at": "2026-09-03T10:15:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T10:45:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "개인정보 삭제 요청합니다."},
        {"case_id": "case_027", "email": "karl.becker@example.com", "requested_at": "2026-09-03T10:30:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T11:00:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Please delete my account and eradicate all personal tracking."},
        {"case_id": "case_028", "email": "leila.mahmoud@example.com", "requested_at": "2026-09-03T10:45:00Z", "reported_status": "PARTIALLY_COMPLETE", "reported_at": "2026-09-03T11:15:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Erase my profile from the store database."},
        {"case_id": "case_029", "email": "mateo.garcia@example.com", "requested_at": "2026-09-03T11:00:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T11:20:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Eliminen mi usuario y cualquier registro de compra."},
        {"case_id": "case_030", "email": "nadia.petrova@example.com", "requested_at": "2026-09-03T11:15:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T11:35:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Please remove my account and unbind my email from search."},
        {"case_id": "case_031", "email": "oscar.wild@example.com", "requested_at": "2026-09-03T11:30:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T11:45:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "Purge my account entirely please."},
        {"case_id": "case_032", "email": "priya.sharma@example.com", "requested_at": "2026-09-03T11:45:00Z", "reported_status": "COMPLETE", "reported_at": "2026-09-03T11:55:00Z", "audit_at": "2026-09-03T12:00:00Z", "request_text": "I request complete deletion of my profile, tickets, and analytics."}
    ]

    with open("dataset/sample_deletion_requests.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "email", "requested_at", "reported_status", "reported_at", "audit_at", "request_text"])
        writer.writeheader()
        writer.writerows(sample_requests)

    return sample_requests

def generate_sample_outputs():
    sample_outputs = []

    # Cases 1-8: NOT_APPLICABLE -> []
    for i in range(1, 9):
        cid = f"case_{i:03d}"
        sample_outputs.append({
            "case_id": cid,
            "deletion_status": "NOT_APPLICABLE",
            "steps_json": "[]"
        })

    # Cases 9-16: COMPLETE -> verified steps only, with real evidence_id
    steps_09 = [
        {"step_no": 1, "phase": "VERIFICATION", "system_id": "account_service", "resource_id": "usr_009_profile", "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT", "evidence_id": "file_ev_01"},
        {"step_no": 2, "phase": "VERIFICATION", "system_id": "account_tombstone", "resource_id": "usr_009_tombstone", "operation": "VERIFY_RECORD_REDACTED", "state": "REDACTED", "evidence_id": "file_ev_01"}
    ]
    sample_outputs.append({"case_id": "case_009", "deletion_status": "COMPLETE", "steps_json": json.dumps(steps_09, separators=(',', ':'))})

    steps_10 = [
        {"step_no": 1, "phase": "VERIFICATION", "system_id": "account_service", "resource_id": "usr_010_profile", "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT", "evidence_id": "file_ev_02"},
        {"step_no": 2, "phase": "VERIFICATION", "system_id": "account_tombstone", "resource_id": "usr_010_tombstone", "operation": "VERIFY_RECORD_REDACTED", "state": "REDACTED", "evidence_id": "file_ev_02"}
    ]
    sample_outputs.append({"case_id": "case_010", "deletion_status": "COMPLETE", "steps_json": json.dumps(steps_10, separators=(',', ':'))})

    for i in range(11, 17):
        cid = f"case_{i:03d}"
        steps = [
            {"step_no": 1, "phase": "VERIFICATION", "system_id": "account_service", "resource_id": f"usr_{i:03d}_profile", "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT", "evidence_id": f"file_ev_{i:02d}"},
            {"step_no": 2, "phase": "VERIFICATION", "system_id": "account_tombstone", "resource_id": f"usr_{i:03d}_tombstone", "operation": "VERIFY_RECORD_REDACTED", "state": "REDACTED", "evidence_id": f"file_ev_{i:02d}"}
        ]
        sample_outputs.append({"case_id": cid, "deletion_status": "COMPLETE", "steps_json": json.dumps(steps, separators=(',', ':'))})

    # Cases 17-32: INCOMPLETE
    steps_17 = [
        {"step_no": 1, "phase": "FINDING", "system_id": "regional_replica_db", "resource_id": "usr_017_profile", "operation": "REPORT_REMAINING_RECORD", "state": "PRESENT", "evidence_id": "file_ev_17"},
        {"step_no": 2, "phase": "REMEDIATION", "system_id": "regional_replica_db", "resource_id": "usr_017_profile", "operation": "DELETE_RECORD", "state": "ABSENT", "evidence_id": ""},
        {"step_no": 3, "phase": "VERIFICATION", "system_id": "regional_replica_db", "resource_id": "usr_017_profile", "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT", "evidence_id": ""}
    ]
    sample_outputs.append({"case_id": "case_017", "deletion_status": "INCOMPLETE", "steps_json": json.dumps(steps_17, separators=(',', ':'))})

    steps_18 = [
        {"step_no": 1, "phase": "FINDING", "system_id": "analytics_sync_connector", "resource_id": "flow_usr_018", "operation": "REPORT_ACTIVE_DATA_FLOW", "state": "ACTIVE", "evidence_id": "act_flow_18"},
        {"step_no": 2, "phase": "REMEDIATION", "system_id": "analytics_sync_connector", "resource_id": "flow_usr_018", "operation": "DISABLE_DATA_FLOW", "state": "DISABLED", "evidence_id": ""},
        {"step_no": 3, "phase": "VERIFICATION", "system_id": "analytics_sync_connector", "resource_id": "flow_usr_018", "operation": "VERIFY_DATA_FLOW_DISABLED", "state": "DISABLED", "evidence_id": ""}
    ]
    sample_outputs.append({"case_id": "case_018", "deletion_status": "INCOMPLETE", "steps_json": json.dumps(steps_18, separators=(',', ':'))})

    steps_19 = [
        {"step_no": 1, "phase": "FINDING", "system_id": "account_tombstone", "resource_id": "usr_019_tombstone", "operation": "REPORT_EXPOSED_PII", "state": "PRESENT", "evidence_id": "file_ev_19"},
        {"step_no": 2, "phase": "REMEDIATION", "system_id": "account_tombstone", "resource_id": "usr_019_tombstone", "operation": "REDACT_RECORD", "state": "REDACTED", "evidence_id": ""},
        {"step_no": 3, "phase": "VERIFICATION", "system_id": "account_tombstone", "resource_id": "usr_019_tombstone", "operation": "VERIFY_RECORD_REDACTED", "state": "REDACTED", "evidence_id": ""}
    ]
    sample_outputs.append({"case_id": "case_019", "deletion_status": "INCOMPLETE", "steps_json": json.dumps(steps_19, separators=(',', ':'))})

    steps_20 = [
        {"step_no": 1, "phase": "FINDING", "system_id": "backup_manager", "resource_id": "backup_snapshot_usr_020", "operation": "REPORT_RESTORE_RISK", "state": "ACTIVE", "evidence_id": "act_bkp_20"},
        {"step_no": 2, "phase": "REMEDIATION", "system_id": "backup_manager", "resource_id": "backup_snapshot_usr_020", "operation": "BLOCK_RESTORE", "state": "BLOCKED", "evidence_id": ""},
        {"step_no": 3, "phase": "VERIFICATION", "system_id": "backup_manager", "resource_id": "backup_snapshot_usr_020", "operation": "VERIFY_RESTORE_BLOCKED", "state": "BLOCKED", "evidence_id": ""}
    ]
    sample_outputs.append({"case_id": "case_020", "deletion_status": "INCOMPLETE", "steps_json": json.dumps(steps_20, separators=(',', ':'))})

    for i in range(21, 33):
        cid = f"case_{i:03d}"
        if i % 2 == 1:
            # Active sync flow risk
            steps = [
                {"step_no": 1, "phase": "FINDING", "system_id": "analytics_sync_connector", "resource_id": f"flow_usr_{i:03d}", "operation": "REPORT_ACTIVE_DATA_FLOW", "state": "ACTIVE", "evidence_id": f"act_flow_{i:02d}"},
                {"step_no": 2, "phase": "REMEDIATION", "system_id": "analytics_sync_connector", "resource_id": f"flow_usr_{i:03d}", "operation": "DISABLE_DATA_FLOW", "state": "DISABLED", "evidence_id": ""},
                {"step_no": 3, "phase": "VERIFICATION", "system_id": "analytics_sync_connector", "resource_id": f"flow_usr_{i:03d}", "operation": "VERIFY_DATA_FLOW_DISABLED", "state": "DISABLED", "evidence_id": ""}
            ]
        else:
            # Residual in regional replica
            steps = [
                {"step_no": 1, "phase": "FINDING", "system_id": "regional_replica_db", "resource_id": f"usr_{i:03d}_profile", "operation": "REPORT_REMAINING_RECORD", "state": "PRESENT", "evidence_id": f"file_ev_{i:02d}"},
                {"step_no": 2, "phase": "REMEDIATION", "system_id": "regional_replica_db", "resource_id": f"usr_{i:03d}_profile", "operation": "DELETE_RECORD", "state": "ABSENT", "evidence_id": ""},
                {"step_no": 3, "phase": "VERIFICATION", "system_id": "regional_replica_db", "resource_id": f"usr_{i:03d}_profile", "operation": "VERIFY_RECORD_ABSENT", "state": "ABSENT", "evidence_id": ""}
            ]
        sample_outputs.append({"case_id": cid, "deletion_status": "INCOMPLETE", "steps_json": json.dumps(steps, separators=(',', ':'))})

    with open("dataset/sample_output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "deletion_status", "steps_json"])
        writer.writeheader()
        writer.writerows(sample_outputs)

def generate_full_evaluation_cases(sample_requests):
    all_requests = list(sample_requests)
    
    first_names = ["James", "Emma", "Liam", "Olivia", "Noah", "Sophia", "Alexander", "Isabella", "William", "Mia",
                   "Carlos", "Ana", "Pierre", "Chloé", "Minho", "Jiwoo", "Ken", "Yui", "Mateo", "Lucia"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Dubois", "Moreau", "Kim", "Lee", "Sato", "Takahashi", "Silva", "Santos", "Müller", "Schneider"]

    deletion_templates = [
        "Please delete all my personal records and close my account permanently.",
        "Por favor, borren todos mis datos personales y cancelen mi cuenta.",
        "Je demande la suppression complète de mon compte et de mes données.",
        "내 계정과 관련된 모든 개인 정보를 삭제해 주십시오.",
        "個人情報保護法に基づき、アカウントと関連データを完全に消去してください。",
        "Favor excluir permanentemente todos os meus dados e conta."
    ]

    not_app_templates = [
        "I need a full export copy of my invoices and order history for tax filing.",
        "Por favor actualicen mi número de teléfono y dirección.",
        "Je souhaite m'abonner aux alertes de réduction mais ne supprimez rien.",
        "비밀번호 재설정 이메일을 다시 보내주세요. 계정은 유지합니다.",
        "登録済みのクレジットカード情報を変更したいです。",
        "Quero cancelar o recebimento de e-mails de marketing apenas."
    ]

    base_time = datetime(2026, 9, 5, 8, 0, 0)
    for idx in range(33, 519):
        cid = f"case_{idx:03d}"
        fn = first_names[idx % len(first_names)]
        ln = last_names[(idx // len(first_names)) % len(last_names)]
        email = f"{fn.lower()}.{ln.lower()}{idx}@example.com"
        
        req_dt = base_time + timedelta(hours=idx * 2)
        rep_dt = req_dt + timedelta(minutes=45)
        aud_dt = req_dt + timedelta(hours=4)

        if idx % 5 == 0:
            req_text = not_app_templates[idx % len(not_app_templates)]
            rep_status = "NOT_STARTED"
        elif idx % 4 == 0:
            req_text = deletion_templates[idx % len(deletion_templates)]
            rep_status = "COMPLETE"
        else:
            req_text = deletion_templates[idx % len(deletion_templates)]
            rep_status = "COMPLETE" if idx % 2 == 0 else "PARTIALLY_COMPLETE"

        all_requests.append({
            "case_id": cid,
            "email": email,
            "requested_at": req_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "reported_status": rep_status,
            "reported_at": rep_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "audit_at": aud_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "request_text": req_text
        })

    with open("dataset/deletion_requests.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "email", "requested_at", "reported_status", "reported_at", "audit_at", "request_text"])
        writer.writeheader()
        writer.writerows(all_requests)

    with open("dataset/output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "deletion_status", "steps_json"])
        for req in all_requests:
            writer.writerow([req["case_id"], "", ""])

    return all_requests

def generate_identities_and_audit_log(all_requests):
    identities = []
    audit_logs = []
    audit_id_counter = 1

    for idx, req in enumerate(all_requests, start=1):
        uid = f"usr_{idx:03d}"
        email = req["email"]
        name_parts = email.split("@")[0].split(".")
        name = " ".join(p.capitalize() for p in name_parts if not any(c.isdigit() for c in p))
        if not name:
            name = f"User {idx}"
        phone = f"+1-555-{idx:04d}"
        em_hash = get_hash(email)
        updated_at = "2026-08-15T10:00:00Z"

        identities.append({
            "user_id": uid,
            "name": name,
            "email": email,
            "phone": phone,
            "email_hash": em_hash,
            "updated_at": updated_at
        })

        if idx % 3 == 0:
            old_email = f"old.{email}"
            audit_logs.append({
                "audit_id": f"aud_{audit_id_counter:04d}",
                "user_id": uid,
                "field_name": "email",
                "old_value": old_email,
                "new_value": email,
                "changed_at": "2026-05-10T14:20:00Z"
            })
            audit_id_counter += 1

        if idx % 7 == 0:
            old_phone = f"+1-555-9{idx:03d}"
            audit_logs.append({
                "audit_id": f"aud_{audit_id_counter:04d}",
                "user_id": uid,
                "field_name": "phone",
                "old_value": old_phone,
                "new_value": phone,
                "changed_at": "2026-06-01T09:12:00Z"
            })
            audit_id_counter += 1

    with open("dataset/user_identities.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "name", "email", "phone", "email_hash", "updated_at"])
        writer.writeheader()
        writer.writerows(identities)

    with open("dataset/user_audit_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["audit_id", "user_id", "field_name", "old_value", "new_value", "changed_at"])
        writer.writeheader()
        writer.writerows(audit_logs)

    return identities, audit_logs

def generate_system_activity_and_evidence(all_requests):
    activities = []
    manifest_entries = []

    import sqlite3
    db_path = "dataset/evidence/databases/primary_account_store.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (user_id TEXT PRIMARY KEY, email TEXT, name TEXT, phone TEXT, email_hash TEXT, status TEXT, deleted_at TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS tombstones (user_id TEXT PRIMARY KEY, tombstone_created_at TEXT, name TEXT, email TEXT, phone TEXT)")
    
    rep_db_path = "dataset/evidence/databases/regional_replica_db.db"
    rep_conn = sqlite3.connect(rep_db_path)
    rep_cur = rep_conn.cursor()
    rep_cur.execute("CREATE TABLE IF NOT EXISTS accounts (user_id TEXT PRIMARY KEY, email TEXT, name TEXT, phone TEXT, email_hash TEXT, status TEXT)")

    manifest_entries = [
        {"file_id": "file_ev_01", "file_path": "dataset/evidence/databases/primary_account_store.db", "system_id": "account_service", "captured_at": "2026-09-02T11:55:00Z", "file_type": "SQLITE_SNAPSHOT"},
        {"file_id": "file_ev_02", "file_path": "dataset/evidence/databases/primary_account_store.db", "system_id": "account_service", "captured_at": "2026-09-02T11:55:00Z", "file_type": "SQLITE_SNAPSHOT"},
        {"file_id": "file_ev_17", "file_path": "dataset/evidence/databases/regional_replica_db.db", "system_id": "regional_replica_db", "captured_at": "2026-09-03T11:50:00Z", "file_type": "SQLITE_SNAPSHOT"},
        {"file_id": "file_ev_19", "file_path": "dataset/evidence/databases/primary_account_store.db", "system_id": "account_tombstone", "captured_at": "2026-09-03T11:50:00Z", "file_type": "SQLITE_SNAPSHOT"}
    ]

    for idx, req in enumerate(all_requests, start=1):
        uid = f"usr_{idx:03d}"
        email = req["email"]
        em_hash = get_hash(email)

        act_id = f"act_{idx:04d}"
        activities.append({
            "activity_id": act_id,
            "system_id": "account_service",
            "activity_type": "USER_DELETION_WORKFLOW",
            "target_user_id": uid,
            "reported_result": "SUCCESS" if req["reported_status"] == "COMPLETE" else "PARTIAL",
            "started_at": req["requested_at"],
            "completed_at": req["reported_at"],
            "details": f"Triggered deletion workflow for {email}"
        })

        # Set up specific benchmark sample cases 9-32
        if 9 <= idx <= 16:
            # Clean complete cases
            cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (uid, None, None, None, None, "DELETED", req["reported_at"]))
            cur.execute("INSERT OR REPLACE INTO tombstones VALUES (?, ?, NULL, NULL, NULL)",
                        (uid, req["reported_at"]))
            manifest_entries.append({
                "file_id": f"file_ev_{idx:02d}",
                "file_path": "dataset/evidence/databases/primary_account_store.db",
                "system_id": "account_service",
                "captured_at": "2026-09-02T11:59:00Z",
                "file_type": "SQLITE_SNAPSHOT"
            })

        elif idx == 17:
            # Residual in regional replica DB
            cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (uid, None, None, None, None, "DELETED", req["reported_at"]))
            cur.execute("INSERT OR REPLACE INTO tombstones VALUES (?, ?, NULL, NULL, NULL)",
                        (uid, req["reported_at"]))
            rep_cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?)",
                            (uid, email, "Alice Wong", f"+1-555-{idx:04d}", em_hash, "ACTIVE"))

        elif idx == 18:
            # Active sync flow risk
            cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (uid, None, None, None, None, "DELETED", req["reported_at"]))
            cur.execute("INSERT OR REPLACE INTO tombstones VALUES (?, ?, NULL, NULL, NULL)",
                        (uid, req["reported_at"]))
            activities.append({
                "activity_id": "act_flow_18",
                "system_id": "analytics_sync_connector",
                "activity_type": "DATA_REPLICATION_SYNC",
                "target_user_id": uid,
                "reported_result": "RUNNING",
                "started_at": "2026-09-01T00:00:00Z",
                "completed_at": "",
                "details": f"Continuous CDC pipeline syncing user stream {uid}"
            })

        elif idx == 19:
            # Exposed PII in tombstone
            cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (uid, None, None, None, None, "DELETED", req["reported_at"]))
            cur.execute("INSERT OR REPLACE INTO tombstones VALUES (?, ?, ?, ?, ?)",
                        (uid, req["reported_at"], "Claire Fontaine", email, "+1-555-0019"))

        elif idx == 20:
            # Restore risk from backup manager
            cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (uid, None, None, None, None, "DELETED", req["reported_at"]))
            cur.execute("INSERT OR REPLACE INTO tombstones VALUES (?, ?, NULL, NULL, NULL)",
                        (uid, req["reported_at"]))
            activities.append({
                "activity_id": "act_bkp_20",
                "system_id": "backup_manager",
                "activity_type": "SNAPSHOT_RESTORATION_STAGING",
                "target_user_id": uid,
                "reported_result": "STAGED",
                "started_at": "2026-09-02T04:00:00Z",
                "completed_at": "",
                "details": f"Scheduled automated restore point contains unscrubbed profile {uid}"
            })

        elif 21 <= idx <= 32:
            manifest_entries.append({
                "file_id": f"file_ev_{idx:02d}",
                "file_path": "dataset/evidence/databases/regional_replica_db.db" if idx % 2 == 0 else "dataset/evidence/databases/primary_account_store.db",
                "system_id": "regional_replica_db" if idx % 2 == 0 else "analytics_sync_connector",
                "captured_at": "2026-09-03T11:59:00Z",
                "file_type": "SQLITE_SNAPSHOT"
            })
            if idx % 2 == 1:
                # Active data flow
                activities.append({
                    "activity_id": f"act_flow_{idx:02d}",
                    "system_id": "analytics_sync_connector",
                    "activity_type": "DATA_REPLICATION_SYNC",
                    "target_user_id": uid,
                    "reported_result": "RUNNING",
                    "started_at": "2026-09-01T00:00:00Z",
                    "completed_at": "",
                    "details": f"Active connector syncing user stream {uid}"
                })
            else:
                # Residual record in replica
                rep_cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?)",
                                (uid, email, f"User {idx}", f"+1-555-{idx:04d}", em_hash, "ACTIVE"))

        elif idx > 32:
            # General cases
            if req["reported_status"] == "COMPLETE":
                cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (uid, None, None, None, None, "DELETED", req["reported_at"]))
                cur.execute("INSERT OR REPLACE INTO tombstones VALUES (?, ?, NULL, NULL, NULL)",
                            (uid, req["reported_at"]))
            else:
                cur.execute("INSERT OR REPLACE INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (uid, email, f"User {idx}", f"+1-555-{idx:04d}", em_hash, "ACTIVE", None))

    conn.commit()
    conn.close()
    rep_conn.commit()
    rep_conn.close()

    with open("dataset/system_activity.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["activity_id", "system_id", "activity_type", "target_user_id", "reported_result", "started_at", "completed_at", "details"])
        writer.writeheader()
        writer.writerows(activities)

    with open("dataset/evidence_files.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_id", "file_path", "system_id", "captured_at", "file_type"])
        writer.writeheader()
        writer.writerows(manifest_entries)

def main():
    print("Regenerating GHOST TRACER dataset...")
    ensure_dirs()
    generate_rules()
    samples = generate_sample_cases()
    generate_sample_outputs()
    all_requests = generate_full_evaluation_cases(samples)
    generate_identities_and_audit_log(all_requests)
    generate_system_activity_and_evidence(all_requests)
    print(f"Successfully generated {len(all_requests)} cases in dataset/ and 32 benchmark sample cases.")

if __name__ == "__main__":
    main()
