# dbt-schema-gen

dbt-schema-gen is an LLM-powered tool that generates and maintains `schema.yml` files for dbt models. It reads SQL model files, infers column metadata, and produces rich documentation with descriptions, data types, and tests.

## Purpose

Maintaining `schema.yml` files manually is tedious and often neglected. dbt-schema-gen automates this by:

- Parsing SQL model files to extract column names, config blocks, and references
- Using an LLM to generate meaningful descriptions for models and columns
- Applying rule-based test generation for primary keys, timestamps, and composite keys
- Smart-merging generated content with existing manual edits

## LLM Providers

dbt-schema-gen supports three LLM providers:

| Provider | Environment Variable | Default Model |
|----------|---------------------|---------------|
| **OpenAI** | `OPENAI_API_KEY` | `gpt-4o-mini` |
| **Anthropic Claude** | `ANTHROPIC_API_KEY` | `claude-3-sonnet-20240229` |
| **Google Gemini** | `GEMINI_API_KEY` | `gemini-1.5-flash` |

Select the provider via the `LLM_PROVIDER` environment variable or the `dbt_schema_gen.yml` configuration file.

## Generation Modes

| Mode | What It Generates | Speed |
|------|-------------------|-------|
| `full` (default) | Descriptions + data types + tests | Standard |
| `descriptions` | Model and column descriptions only | Fastest |
| `types` | Data type inference only | Fast |
| `tests` | Test blocks only | Fast |

```bash
# Full generation
dbt-schema-gen --mode full /path/to/dbt/project

# Descriptions only (fastest for documentation)
dbt-schema-gen --mode descriptions /path/to/dbt/project
```

## Smart Merge

When `schema.yml` files already exist, dbt-schema-gen uses a smart merge strategy that distinguishes between three categories of fields:

### Fields Synced from SQL (Always Updated)

Config values from the SQL `{{ config() }}` block are always kept in sync:

- `config.materialized`
- `config.tags`

If you change tags in your SQL model, the schema file updates automatically on the next run.

### Preserved Fields (Your Manual Edits)

Fields you manually add to the YAML are preserved across regenerations:

- `meta.owner`
- `meta.authoritative`
- Any custom `meta` fields you define

### Regenerated Fields (LLM Output)

These fields are regenerated on each run:

- `description` (model-level and column-level)
- `columns.data_type` (inferred from SQL)

The tool tracks which fields it generated via `_generated_fields` metadata, so it knows the difference between your edits and its own previous output.

## Test Generation

Tests are generated using **rule-based pattern matching**, not by the LLM. This ensures only valid dbt tests are produced.

### Column-Level Tests

| Column Pattern | Tests Added |
|----------------|-------------|
| `*_id`, `*_pk`, `*_index` | `unique`, `not_null` |
| `*_timestamp`, `*_at`, `date` | `not_null` |
| `transaction_hash`, `block_hash` | `unique`, `not_null` |

### Model-Level Tests

| Pattern | Test Added |
|---------|------------|
| `date` + dimension column | `dbt_utils.unique_combination_of_columns` |

Invalid tests (ones that do not exist in dbt or dbt_utils) are automatically removed during validation.

## CLI Usage

```bash
# Generate schemas for all models in a project
dbt-schema-gen /path/to/dbt/project

# Generate for specific models
dbt-schema-gen -m fct_daily_sales,stg_transactions /path/to/project

# Generate from a subdirectory
dbt-schema-gen /path/to/dbt/project/models/staging

# Force regeneration (overwrite even if columns unchanged)
dbt-schema-gen -o /path/to/project

# Dry run (preview without writing)
dbt-schema-gen --dry-run -v /path/to/project

# Skip test generation
dbt-schema-gen --skip-tests /path/to/project

# Validate existing schemas without regenerating
dbt-schema-gen --validate-only /path/to/project
```

### CLI Options

| Option | Description |
|--------|-------------|
| `-m, --models TEXT` | Only process specific models (comma-separated) |
| `-o, --overwrite` | Force regeneration even if columns are unchanged |
| `--skip-tests` | Do not generate test blocks |
| `--mode` | Generation mode: `full`, `descriptions`, `types`, `tests` |
| `--dry-run` | Preview changes without writing files |
| `--preserve-config` | Preserve user-maintained fields (default: true) |
| `-v, --verbose` | Show detailed output and warnings |
| `--validate-only` | Validate existing schemas only |
| `--config PATH` | Path to custom configuration file |

## Configuration

### Environment Variables

```bash
# Provider selection
LLM_PROVIDER=openai                # openai | anthropic | gemini

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-sonnet-20240229
ANTHROPIC_TEMPERATURE=0.3

# Google Gemini
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.3

# Rate limiting
GLOBAL_MAX_RPM=10                  # Max requests per minute
```

### Project Configuration File

Create `dbt_schema_gen.yml` in the dbt project root for persistent settings:

```yaml
llm:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.3

generation:
  mode: full
  skip_tests: false

merge:
  preserve_user_fields:
    - meta.owner
    - meta.authoritative
  always_regenerate:
    - description
    - columns.description
    - columns.data_type
    - config.tags
    - config.materialized

tests:
  enabled: true
  packages:
    - dbt
    - dbt_utils
  auto_tests:
    primary_key: true
    not_null_timestamps: true
    relationships: false
  max_tests_per_column: 3

parsing:
  use_sqlglot: true
  fallback_to_regex: true
```

## Column Comments

You can add hints in your SQL files to improve the quality of LLM-generated descriptions:

```sql
-- @column date: The calendar date for this aggregation (UTC timezone)
-- @column total_value: Sum of all transaction values in wei

SELECT
    toStartOfDay(block_timestamp) AS date,
    SUM(value) AS total_value
FROM {{ ref('stg_execution__transactions') }}
GROUP BY 1
```

Jinja comment syntax is also supported:

```sql
{# @column date: Daily aggregation date in UTC #}
```

## How It Works

1. **Parse SQL** -- Uses sqlglot (with regex fallback) to extract column names, `{{ config() }}` blocks, and `{{ ref() }}` / `{{ source() }}` references
2. **Build context** -- Gathers upstream model schemas and source definitions for richer LLM prompts
3. **Call LLM** -- Sends focused prompts to generate model and column descriptions
4. **Generate tests** -- Applies rule-based pattern matching to produce valid tests
5. **Smart merge** -- Merges generated content with existing `schema.yml`, preserving manual edits
6. **Write files** -- Outputs `schema.yml` to each model's directory

## Integration with dbt-cerebro

dbt-schema-gen is used alongside dbt-cerebro to maintain documentation for the ~400 models in the project. A typical workflow:

```bash
# After adding or modifying models
dbt-schema-gen /path/to/dbt-cerebro

# Review changes
git diff models/

# Commit updated schemas
git add models/*/schema.yml
```

For CI/CD pipelines, use `--validate-only` to check that schemas are up to date without modifying files.
