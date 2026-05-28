# Architecture

```text
CLI -> input files or SSH collection -> parsers -> evaluator -> reporters
```

The project separates collection, parsing, evaluation and reporting so the validation logic can be tested offline before depending on live SSH access.
