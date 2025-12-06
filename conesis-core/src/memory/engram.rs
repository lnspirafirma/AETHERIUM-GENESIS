use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

/// [Memory Engram]
/// The crystallized form of an intent after passing through the Consecrator.
/// Replaces the legacy 'ritual_document' dictionary.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Engram {
    /// Unique Ritual ID (UUID format for external correlation)
    pub ritual_id: String,
    
    /// The high-dimensional vector representing the thought.
    /// [Legacy: embedding]
    pub vector: Vec<f32>,
    
    /// Semantic Metadata
    pub meta: EngramMeta,
    
    /// The audit trail of how this thought was formed.
    /// [Legacy: protocol_log]
    pub trace: Vec<TraceStep>,

    /// Creation Timestamp
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EngramMeta {
    pub raw_text: String,
    pub symbol: String,
    pub emotion: String,
    pub theme: String,
    pub entities: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TraceStep {
    pub step_sequence: i32,
    pub protocol_name: String,
    pub output_summary: String,
    pub timestamp: u64,
}

/// [The High Priest]
/// Converts raw inputs into a Sacred Engram.
pub struct Consecrator;

impl Consecrator {
    /// Performs the ritual to crystalize a raw intent.
    pub fn consecrate(
        text: &str, 
        embedding: Vec<f32>, 
        symbol: &str,
        theme: &str
    ) -> Engram {
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default()
            .as_secs();

        // 1. Log the Parser Step
        let step1 = TraceStep {
            step_sequence: 1,
            protocol_name: "SymbolicParser".to_string(),
            output_summary: format!("Symbol identified: {}", symbol),
            timestamp: now,
        };

        // 2. Log the Ritual Step
        let step2 = TraceStep {
            step_sequence: 2,
            protocol_name: "Ritualizer".to_string(),
            output_summary: format!("Theme applied: {}", theme),
            timestamp: now,
        };

        // 3. Seal the Engram
        Engram {
            ritual_id: uuid::Uuid::new_v4().to_string(),
            vector: embedding,
            meta: EngramMeta {
                raw_text: text.to_string(),
                symbol: symbol.to_string(),
                emotion: "neutral".to_string(), // In real logic, this comes from Rexilon
                theme: theme.to_string(),
                entities: vec![], // Entity extraction logic here
            },
            trace: vec![step1, step2],
            timestamp: now,
        }
    }
}
