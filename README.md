# OpenProject Workflow Visualiser
This script parses a downloaded HTML of the Administration>Workflow page in OpenProject and extracts the default workflow of the previously selected role and type as a Mermaid stateDiagram-v2. It's recommended to download the workflow page with the checkmark set for only showing states used by the type. 

## Example 1
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

## Example 2
In this example the role is not allowed to transfer to or from certain states. As "Rejected" and "Show and Tell" are used in the work package type they are shown without any lines leaving or entering this state.

```mermaid
stateDiagram-v2
    1: New
    2: In specification
    3: Specified
    7: In progress
    8: Developed
    9: In testing
    10: Tested
    11: Test failed
    15: Show and Tell
    12: Closed
    13: On hold
    14: Rejected
    22: Approved
    1 --> 2
    2 --> 3
    3 --> 2
    7 --> 8
    7 --> 12
    7 --> 13
    8 --> 9
    9 --> 10
    9 --> 11
    10 --> 12
    11 --> 7
    11 --> 9
    13 --> 7
    13 --> 12
    22 --> 7
```
