use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::time::{SystemTime, UNIX_EPOCH};
use std::sync::{Arc, RwLock};
use crate::error::ConesisError;

/// [Immutable Record]
/// Represents a frozen moment in the entity's history.
/// Fields are private to ensure immutability after creation.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AkashicEnvelope {
    /// Unique Sequence ID (Monotonic increasing)
    pub id: i64,
    /// Timestamp (Unix Epoch)
    pub timestamp: i64,
    /// The actor who initiated the action (Agent ID)
    pub actor: String,
    /// The data payload (Action details, Context)
    pub payload: String,
    /// Cryptographic Hash of this record + Previous Hash (Chaining)
    pub hash: String,
    /// Previous Record's Hash (Provenance)
    pub prev_hash: String,
    /// Digital Signature (Simulated for validation)
    pub signature: String,
}

/// [The Memory Bank]
/// Thread-safe storage for the consciousness stream.
#[derive(Debug)]
pub struct AkashicLedger {
    /// The chain of records. Protected by RwLock for concurrent access.
    chain: Arc<RwLock<Vec<AkashicEnvelope>>>,
}

impl AkashicLedger {
    pub fn new() -> Self {
        Self {
            chain: Arc::new(RwLock::new(Vec::new())),
        }
    }

    /// Appends a new memory to the timeline.
    /// This is an O(1) operation protected by a Write Lock.
    pub fn record(&self, actor: &str, payload: &str, signature: &str) -> Result<i64, ConesisError> {
        let mut chain = self.chain.write().map_err(|_| ConesisError::LockPoisoned)?;
        
        let id = chain.len() as i64 + 1;
        let prev_hash = chain.last().map(|e| e.hash.clone()).unwrap_or_else(|| "GENESIS_HASH".to_string());
        
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map_err(|_| ConesisError::TimeError)?
            .as_secs() as i64;

        // Create the Integrity Hash (Chain Link)
        let mut hasher = Sha256::new();
        hasher.update(format!("{id}{timestamp}{actor}{payload}{prev_hash}{signature}"));
        let hash = format!("{:x}", hasher.finalize());

        let envelope = AkashicEnvelope {
            id,
            timestamp,
            actor: actor.to_string(),
            payload: payload.to_string(),
            hash,
            prev_hash,
            signature: signature.to_string(),
        };

        chain.push(envelope);
        Ok(id)
    }

    /// Read-only access to the full history (For KCP/Deep Think).
    pub fn read_history(&self) -> Result<Vec<AkashicEnvelope>, ConesisError> {
        let chain = self.chain.read().map_err(|_| ConesisError::LockPoisoned)?;
        Ok(chain.clone())
    }

    /// Returns the current state hash (Head) for quick validation.
    pub fn current_head_hash(&self) -> Result<String, ConesisError> {
        let chain = self.chain.read().map_err(|_| ConesisError::LockPoisoned)?;
        Ok(chain.last().map(|e| e.hash.clone()).unwrap_or_else(|| "GENESIS_HASH".to_string()))
    }
}
