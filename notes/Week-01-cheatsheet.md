# Week 1 Cheat Sheet

### The AI Map in Two Lines
Traditional code uses explicit **rules + data** to output explicit answers. 
Machine Learning reverses this: it uses **data + answers** to predict the underlying patterns and rules.

### Python vs Java: Five Differences
* **Typing**: Python uses dynamic typing (checked at runtime); Java uses rigid static typing (checked at compile time).
* **Syntax**: Python requires significant whitespace/indentation; Java uses explicit semicolons and curly braces `{}`.
* **Compilation**: Python is interpreted via bytecode (`.pyc`); Java explicitly compiles source to bytecode (`.class`).
* **Memory Management**: Python uses reference counting + a cycle-detecting GC; Java relies entirely on generational tracing GCs.
* **Objects**: Python types everything as a first-class object; Java splits systems into primitive types and object types.

### Pandas: The Five Calls I Use Most
* `pd.read_sql_query(query, conn)`: Extracts raw database tables directly into an operational DataFrame.
* `df.drop_duplicates()`: Drops redundant rows to enforce transactional data cleanliness.
* `df.copy()`: Duplicates structural states to prevent frustrating `SettingWithCopyWarning` errors.
* `df.groupby("col").size()`: Calculates rapid aggregations and frequencies across categorised keys.
* `df.sort_values(by="col", ascending=False)`: Rearranges matrices swiftly based on target variables.

### SQL: SELECT Order, WHERE vs HAVING, JOIN Types
* **Query Execution Order**: `FROM` ➔ `JOIN` ➔ `WHERE` ➔ `GROUP BY` ➔ `HAVING` ➔ `SELECT` ➔ `DISTINCT` ➔ `ORDER BY` ➔ `LIMIT`.
* **WHERE vs HAVING**: `WHERE` filters raw transactional rows *before* aggregation. `HAVING` filters generated groups *after* aggregation.
* **JOIN Varieties**:
  * `INNER`: Returns matching row intersections only.
  * `LEFT`: Retains all records from the left side, filling right-side gaps with `NULL`.
  * `RIGHT`: Retains all records from the right side, filling left-side gaps with `NULL`.
  * `FULL`: Retains the complete combination of both sides, matching where possible.

### LLM Basics: Token, Context Window, Temperature
* **Token**: The atomic text unit processed by an LLM (typically equalling roughly ~4 characters or 0.75 words).
* **Context Window**: The maximum threshold of input and output tokens a neural model can process inside a single query turn.
* **Temperature**: A randomisation factor between `0.0` (fully deterministic/analytical) and `1.0+` (highly creative/variable).
