# OpenProject Workflow Visualiser
This script parses a downloaded HTML of the Administration>Workflow page in OpenProject and extracts the default workflow of the previously selected role and type as a Mermaid stateDiagram-v2. It's recommended to download the workflow page with the checkmark set for only showing states used by the type. 

In case you have mermaid-cli installed on your system and mmdc in your '$PATH', you can use the '-o' option to output a PNG rendering of your diagram. This option won't output a markdown representation.

## Example (role: Project Manager, type: Epic)
In this example the role is allowed to act on all states or the work package.

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
    12: Closed
    13: On hold
    14: Rejected
    22: Approved
    1 --> 2
    1 --> 14
    2 --> 3
    2 --> 14
    3 --> 2
    3 --> 14
    3 --> 22
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

## Example (role: Member, type: Epic)
In this example the role is not allowed to transfer to or from certain states. As "Rejected" is used in the work package type it is shown without any lines leaving or entering this state.

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

## Example (role: Reader, type: Epic)
The role in this example doesn't have any rights to adjust states.

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
    12: Closed
    13: On hold
    14: Rejected
    22: Approved
```
