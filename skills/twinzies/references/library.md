# The twin library

Twins are an asset that compounds. A twin built for one product (say, a physical media manager) should be found and reused when the builder makes a different product that the same kind of person would use, and it should get more accurate every time it is evaluated against real behavior. The library is what makes that work.

## Where it lives
A folder named `twinzies-library/` that persists between sessions. The cloud workspace is wiped when a session ends, so:
1. Look in the session's connected folders on the user's computer for an existing `twinzies-library/` (device tools: `get_device_info`, `device_list_dir`). Use it if found.
2. If none exists, create one inside a connected folder (ask which if several are connected, and don't put it inside an app's repo unless the user says so, so it isn't published by accident). If no folder is connected, work in the working directory and tell the user to add a folder, because otherwise the library is lost when the session ends.
3. Suggest putting it under git. Version history is what lets the user see how a twin changed and why.

```
twinzies-library/
├── README.md              # what this is, naming rules, status ladder
├── registry.md            # one row per twin: id, name, status, version, domains, needs, last validated, products tested
├── twins/<id>.md          # one file per twin (schema in persona-schema.md)
├── evidence/<domain>.md   # evidence logs, one per domain or source batch
├── products/<product>/    # per-product studies: tasks, findings.json, report.html, validation results
└── changelog.md           # every create / adapt / revise / retire, newest first
```

## Naming
Every twin gets a stable `id` (kebab-case, e.g. `barcode-blitz-cataloger`) and a display name: an invented first name plus a short nickname for what they do ("Marcus, the Barcode-Blitz Cataloger"). Pick names that are easy to say in a design review and that don't suggest a real poster. Never rename a twin once it is in the library; change `name` only if the user asks, and record it in the changelog. Fork variants get their own id and name and a `forked_from` field.

## Matching: find, adapt, or create
Run this whenever the user starts work on a new product, site or domain, before gathering any new evidence.

1. **Describe the product** in terms of the jobs it supports, the contexts of use (phone in a shop, desk, offline, shared device) and the audience.
2. **Search the library** by `domains` and `needs` tags, then read the candidates' goals, pain points and tasks. Judge fit by needs and behavior, not by topic label. A "bulk intake" twin from a cataloging app also fits an inventory tool for a small shop.
3. **Sort each candidate into one bucket:**
   - **Reuse**: the twin's needs cover the new product. Use it as is; add the product to its `products_tested`.
   - **Adapt**: the person is right but the context differs (different device, domain vocabulary, constraints). Fork a variant (`forked_from`, new id, version 0.1) and change only what the new evidence supports, so the parent stays clean. Use this instead of editing the parent when the change wouldn't hold for the parent's other products.
   - **Skip**: not relevant to this product.
4. **Find the gaps.** List the jobs, contexts or accessibility needs in the new product that no reused or adapted twin covers. Only those gaps need a fresh evidence pass (Build mode in SKILL.md), scoped to the gap, which keeps the work proportional.
5. **Show the user the plan** before spending effort: a short table of reused / adapted / new twins with one line of reasoning each. This is a good moment to offer options (for example, adapt vs. create new) since it changes how many twins they end up maintaining.
6. **Aim for a working set of 4-12 twins per product**, drawn from any mix of the three buckets. Don't let the library grow without pruning: merge near-duplicates and retire twins that no longer match any product.

## Status ladder
Each twin carries a `status`, and the report always shows it, so nobody mistakes a hypothesis for a finding.

| Status | Meaning | How it's earned |
|---|---|---|
| `hypothesis` | Built from public discourse or a few first-party signals | Created |
| `corroborated` | Its key traits show up in first-party data (feedback, support, analytics) from the builder's own users | At least 3 independent first-party signals per key trait |
| `validated` | Real users who match this twin confirmed or corrected the key predictions in research | At least 3 matched participants across a study, with the validation log filled in |
| `retired` | No longer matches real users or any product | User decision or two failed validations; keep the file and record why |

Evidence ages. If the newest evidence is more than about a year old, mark the twin `stale` in the registry and offer a refresh pass (a few fresh searches on the twin's top pain points) the next time it is used.

## The improvement loop
After every evaluation or study, close the loop before finishing:
1. **List mismatches** between what the twin predicted and what was observed (in the product, or from real users). Real-user evidence outranks forum evidence, which outranks the model's inference.
2. **Revise the twin file** where evidence supports it: update goals, pain points, vocabulary, tasks and evidence strength. Don't change a trait because a single observation contradicted it; mark it `contested` in the file and note what would settle it.
3. **Bump the version** (patch for wording or evidence additions, minor for changed goals or pain points, major for a changed archetype) and update `last_validated` and `status` if earned.
4. **Write the changelog entry**: date, twin id, what changed, which evidence (study, product, source) caused it. Never silently overwrite.
5. **Update the registry** and the product's study folder.
6. **Tell the user** what changed in the twins in two or three lines, since changed twins change what future reports say.

## Merging and splitting
If two twins keep producing the same findings across products, propose merging them; if one twin keeps splitting real users into groups with opposite reactions, propose splitting it. Both are changelog events and need the user's okay.
