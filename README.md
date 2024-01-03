# OpenProject Workflow Visualiser
This script parses a downloaded HTML of the Administration>Workflow page in OpenProject and extracts the default workflow of the previously selected role and type as a Mermaid stateDiagram-v2.

## Example
```mermaid
stateDiagram-v2
    1: New
    7: In progress
    12: Closed
    13: On hold
    14: Rejected
    1 --> 7
    1 --> 14
    7 --> 12
    7 --> 13
    13 --> 7
    13 --> 12
    13 --> 14
```
