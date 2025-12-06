use crate::error::ConesisResult;

/// [Governance Protocol]
/// Rules that must be satisfied before an action is materialized.
pub trait AuditProtocol {
    fn audit_intent(&self, actor: &str, intent: &str) -> ConesisResult<()>;
}

pub struct FirmaEnforcer {
    /// In a real implementation, this would load rules from `inspirafirma_ruleset.json`
    allowed_intents: Vec<String>,
}

impl FirmaEnforcer {
    pub fn new() -> Self {
        Self {
            // Hardcoded "Constitution" for prototype
            allowed_intents: vec![
                "generate_revenue".to_string(),
                "query_context".to_string(),
                "system_maintenance".to_string(),
                "alert_user".to_string(),
            ],
        }
    }
}

impl AuditProtocol for FirmaEnforcer {
    fn audit_intent(&self, actor: &str, intent: &str) -> ConesisResult<()> {
        // Rule 1: Unauthorized Actors check
        if actor == "UNIDENTIFIED_AGENT" {
             return Err(format!("[AUDIT FAIL] Actor '{actor}' is not authorized to act.").into());
        }

        // Rule 2: Allowed Intent Check
        if !self.allowed_intents.contains(&intent.to_string()) {
            return Err(format!("[AUDIT FAIL] Intent '{intent}' violates the Firma Constitution.").into());
        }

        // Logic passed
        Ok(())
    }
}
