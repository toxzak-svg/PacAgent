# Backpack VS Code Extension

This extension provides integration with the [Backpack Agent Container System](https://github.com/asdevllm/backpack).

## Features

- **Status View**: View the current `agent.lock` status, including defined credentials and personality.
- **Run with Backpack**: CodeLens to run Python agents with one click, automatically injecting credentials.
- **Cloud Ready**: Develop locally, deploy to Vercel/Railway with the same `agent.lock`.
- **Commands**:
  - `Backpack: Init`: Initialize a new agent in the current directory.
  - `Backpack: Run`: Run an agent script with JIT credential injection.
  - `Backpack: Refresh`: Refresh the status view.

## Requirements

- **Backpack CLI**: You must have the `backpack` CLI installed and available in your PATH or current environment.
  ```bash
  pip install backpack
  ```

## Usage

1. Open a folder containing a Backpack agent (or where you want to create one).
2. The "Backpack" view in the Activity Bar will show the status of `agent.lock`.
3. Open a Python file with a `if __name__ == "__main__":` block to see the "Run with Backpack" CodeLens.
