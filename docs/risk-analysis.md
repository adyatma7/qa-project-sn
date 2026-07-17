# Risk Analysis

| Feature          | Business Impact       | Risk Level | Reasoning                                     |
|-------------------|------------------------|------------|------------------------------------------------|
| Login             | Medium — gateway       | Medium     | Blocks every other flow if broken; no money moves directly through it |
| Fund Transfer     | High — moves money     | High       | Direct financial impact if broken — automated Phase 2 |
| Bill Pay          | High — moves money     | High       | Same class of risk as transfer — automated Phase 2 |
| Account Overview  | Low — read only        | Low        | No state change, low complexity — not automated yet |
| Contact Us        | Low                    | Low        | No business-critical data involved — out of scope |

This table is what justifies why Login gets 3 test cases (positive, invalid
credentials, empty-field edge case) while lower-risk pages get none yet —
effort follows risk, not alphabetical order through the site map.
