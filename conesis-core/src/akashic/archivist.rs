use super::ledger::AkashicLedger;
use crate::error::ConesisResult;
use std::fs::File;
use std::io::Write;

/// [Memory Management Agent]
/// Responsible for Pruning and Snapshotting the Akashic Ledger.
pub struct Archivist;

impl Archivist {
    /// Creates a snapshot of the current ledger state to a secure file.
    pub fn create_snapshot(ledger: &AkashicLedger, path: &str) -> ConesisResult<String> {
        let history = ledger.read_history()?;
        let json = serde_json::to_string_pretty(&history)
            .map_err(|e| format!("Serialization failed: {}", e))?;

        let mut file = File::create(path).map_err(|e| format!("File IO failed: {}", e))?;
        file.write_all(json.as_bytes()).map_err(|e| format!("Write failed: {}", e))?;

        Ok(format!("Snapshot secured at {} with {} records.", path, history.len()))
    }

    /// [Pruning Protocol]
    /// In Rust (Memory Safe), we enforce that pruning maintains the Hash Chain integrity.
    /// This function would theoretically archive old records and keep only the 'Head' + N records.
    pub fn prune_memory(ledger: &AkashicLedger, keep_count: usize) -> ConesisResult<()> {
        // Note: For actual pruning in RwLock<Vec>, we need write access to truncate logic.
        // This is a placeholder for the logic:
        // 1. Calculate the 'Anchor Hash' of the oldest record to be kept.
        // 2. Archive everything before it.
        // 3. Update the in-memory chain.
        
        let current_count = ledger.read_history()?.len();
        
        if current_count > keep_count {
             // Logic to truncate would go here (requires extending Ledger API)
             return Ok(());
        }
        
        Ok(())
    }
}
