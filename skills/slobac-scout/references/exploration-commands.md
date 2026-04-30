# Exploration Command Templates

Ready-made shell command patterns for efficient test-suite exploration. The scout loads this reference and adapts commands to the target suite's ecosystem.

## File discovery

Find all test files under a target directory, excluding common non-test directories.

### Python

```bash
rg --files -g 'test_*.py' -g '*_test.py' -g 'conftest.py' <target>
```

### JavaScript / TypeScript

```bash
rg --files -g '*.test.{js,ts,jsx,tsx}' -g '*.spec.{js,ts,jsx,tsx}' <target>
```

### Go

```bash
rg --files -g '*_test.go' <target>
```

### Ruby (rspec)

```bash
rg --files -g '*_spec.rb' -g 'spec_helper.rb' <target>
```

### Ruby (minitest)

```bash
rg --files -g 'test_*.rb' -g '*_test.rb' <target>
```

### JVM (Java / Kotlin)

```bash
rg --files -g '*Test.java' -g '*Test.kt' -g '*Tests.java' -g '*Tests.kt' <target>
```

### Rust

```bash
rg --files -g '*_test.rs' <target>
# Also check for tests/ directory convention
ls <target>/tests/*.rs 2>/dev/null
```

## Test counting per file

Approximate test count using pattern matching. These patterns are heuristic, not AST-based.

### Python

```bash
rg -c '^\s*(async )?def test_' <file>
```

### JavaScript / TypeScript

```bash
rg -c '^\s*(it|test|it\.each|test\.each)\(' <file>
```

### Go

```bash
rg -c '^func Test' <file>
```

### Ruby (rspec)

```bash
rg -c '^\s*(it|specify)\s' <file>
```

### Ruby (minitest)

```bash
rg -c '^\s*def test_' <file>
```

### JVM

```bash
rg -c '@Test' <file>
```

### Rust

```bash
rg -c '#\[test\]' <file>
```

## Size measurement

Line count and byte/character count per file.

```bash
wc -l <file>     # line count
wc -c <file>     # byte count (≈ char count for ASCII-dominant source)
```

For batch measurement of all discovered files:

```bash
wc -l -c <file1> <file2> ... <fileN>
```

## Tier convention detection

Detect directory-based tier conventions by listing immediate subdirectories of the suite root.

```bash
ls -d <target>/*/ 2>/dev/null
```

Common tier directory names: `unit`, `integration`, `e2e`, `end-to-end`, `smoke`, `contract`, `functional`, `acceptance`.
