# era-parser

The era-parser is a beacon chain archive file parser that extracts consensus layer data from era files and exports it to multiple formats including ClickHouse, Parquet, CSV, JSON, and JSONL.

## Purpose

Era files are compressed archives of beacon chain history, each containing 8192 consecutive slots. They provide an efficient way to bulk-load historical consensus data without querying a beacon node API slot by slot. The era-parser reads these files, applies fork-aware parsing, and outputs structured data.

## Era File Format

An era file is a binary archive format standardized for beacon chain data distribution:

- Each file contains exactly **8192 slots** of beacon chain data
- Files are named by network and era number: `gnosis-02607-fe3b60d1.era`
- The format includes block headers, block bodies, and state data
- Files are compressed for efficient storage and transfer
- Network is auto-detected from the filename prefix

## Data Types

era-parser can extract the following data types from era files:

| Data Type | Description | Fork Availability |
|-----------|-------------|-------------------|
| `blocks` | Block headers and metadata | Phase 0+ |
| `transactions` | Execution layer transactions | Bellatrix+ |
| `attestations` | Validator attestations | Phase 0+ |
| `deposits` | Validator deposits | Phase 0+ |
| `withdrawals` | Validator withdrawals | Capella+ |
| `voluntary-exits` | Voluntary validator exits | Phase 0+ |
| `proposer-slashings` | Proposer slashing events | Phase 0+ |
| `attester-slashings` | Attester slashing events | Phase 0+ |
| `sync-aggregates` | Sync committee participation | Altair+ |
| `bls-changes` | BLS-to-execution address changes | Capella+ |
| `execution-payloads` | Full execution layer payloads | Bellatrix+ |
| `blob-kzg-commitments` | Blob KZG commitments | Deneb+ |
| `deposit-requests` | Deposit execution requests | Electra+ |
| `withdrawal-requests` | Withdrawal execution requests | Electra+ |
| `consolidation-requests` | Consolidation execution requests | Electra+ |

Use `all-blocks` to extract all available data types in a single pass.

## Network Support

| Network | Phase 0 | Altair | Bellatrix | Capella | Deneb | Electra |
|---------|---------|--------|-----------|---------|-------|---------|
| **Mainnet** | Yes | Yes | Yes | Yes | Yes | Yes |
| **Gnosis** | Yes | Yes | Yes | Yes | Yes | Yes |
| **Sepolia** | Yes | Yes | Yes | Yes | Yes | Yes |

Network configuration is automatic based on the era filename.

## Output Formats

| Format | Extension | Best For |
|--------|-----------|----------|
| **JSON** | `.json` | API integration, small datasets |
| **JSON Lines** | `.jsonl` | Streaming, large datasets |
| **CSV** | `.csv` | Spreadsheet analysis, pandas |
| **Parquet** | `.parquet` | Big data analytics, ML pipelines |
| **ClickHouse** | `--export clickhouse` | Production analytics database |

## CLI Usage

### Local Era Files

```bash
# Show era file statistics
era-parser gnosis-02607-fe3b60d1.era stats

# Parse a single block
era-parser gnosis-02607-fe3b60d1.era block 21348352

# Export all data types to separate Parquet files
era-parser gnosis-02607-fe3b60d1.era all-blocks data.parquet --separate

# Export specific data type to JSON
era-parser gnosis-02607-fe3b60d1.era transactions txs.json

# Export directly to ClickHouse
era-parser gnosis-02607-fe3b60d1.era all-blocks --export clickhouse
```

### Remote Era Processing

era-parser can fetch era files from a remote URL and process them directly:

```bash
# Process a range of eras into ClickHouse
era-parser --remote gnosis 1082-1100 all-blocks --export clickhouse

# Force reprocess (cleans existing data first)
era-parser --remote gnosis 1082-1100 all-blocks --export clickhouse --force

# Download without processing
era-parser --remote gnosis 1082-1100 --download-only

# Open-ended range (from era 1082 to latest available)
era-parser --remote gnosis 1082+ all-blocks --export clickhouse
```

### State Management

```bash
# Check processing status for a network
era-parser --era-status gnosis

# View failed processing attempts
era-parser --era-failed gnosis

# Clean up stale entries older than 30 days
era-parser --era-cleanup 30
```

### Database Migrations

```bash
# Check migration status
era-parser --migrate status

# Run all pending migrations
era-parser --migrate run

# List available migrations
era-parser --migrate list
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLICKHOUSE_HOST` | -- | ClickHouse server hostname |
| `CLICKHOUSE_PASSWORD` | -- | Authentication password |
| `CLICKHOUSE_PORT` | `8443` | HTTP port |
| `CLICKHOUSE_USER` | `default` | Username |
| `CLICKHOUSE_DATABASE` | `beacon_chain` | Target database |
| `CLICKHOUSE_SECURE` | `true` | Use HTTPS |
| `ERA_BASE_URL` | -- | Base URL for remote era file downloads |
| `DOWNLOAD_TIMEOUT` | `300` | Download timeout in seconds |
| `MAX_RETRIES` | `3` | Maximum retry attempts |
| `DOWNLOAD_THREADS` | `4` | Concurrent download threads |

## Processing Modes

### Normal Mode (Default)

Processes all specified eras, automatically skipping those already completed:

```bash
era-parser --remote gnosis 1082-1100 all-blocks --export clickhouse
```

### Force Mode

Cleans existing data for the specified range before reprocessing:

```bash
era-parser --remote gnosis 1082-1100 all-blocks --export clickhouse --force
```

Force mode is useful for data recovery after corruption, reprocessing after schema changes, or ensuring a clean state for testing.

## Performance

- **Global batch size** -- 100,000 records per insert for optimal ClickHouse performance
- **Streaming inserts** -- Large datasets automatically use streaming mode
- **Constant memory** -- Memory usage remains constant per era regardless of data volume
- **Parallel downloads** -- Remote era files are fetched concurrently with retry logic
- **Atomic processing** -- Each era is either fully processed or marked as failed

## Docker Deployment

```bash
# Build
docker build -t era-parser:latest .

# Local file processing
docker-compose run --rm era-parser /app/era-files/your-file.era all-blocks --export clickhouse

# Remote processing
docker-compose run --rm era-parser --remote gnosis 1082-1100 all-blocks --export clickhouse
```
