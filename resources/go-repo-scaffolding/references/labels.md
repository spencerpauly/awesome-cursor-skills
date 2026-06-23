# Repo Labels

Standard JumpCloud labels to create on new repos. New GitHub repos come with 9 default labels (bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix). Create the additional labels below.

Source: [jumpcloud-public-workflows labels](https://github.com/TheJumpCloud/jumpcloud-public-workflows/labels)

## Labels to create

```bash
REPO="TheJumpCloud/jumpcloud-{app_name}"

gh label create "DB Migration"                --repo "$REPO" --color "BB9A49" --description ""
gh label create "dependencies"                --repo "$REPO" --color "0366d6" --description "Pull requests that update a dependency file"
gh label create "Does Not Need Manual Testing" --repo "$REPO" --color "006B75" --description "PR can be deployed to production without any manual testing."
gh label create "go"                          --repo "$REPO" --color "16e2e2" --description "Pull requests that update Go code"
gh label create "minor"                       --repo "$REPO" --color "EFB993" --description ""
gh label create "Needs Manual Testing"        --repo "$REPO" --color "855A44" --description "PR needs manual testing in order to deploy to production."
gh label create "no version"                  --repo "$REPO" --color "AD194F" --description "PR does not add functional changes"
gh label create "origin"                      --repo "$REPO" --color "ededed" --description ""
gh label create "patch"                       --repo "$REPO" --color "E5859F" --description ""
gh label create "scaffold-release"            --repo "$REPO" --color "ededed" --description ""
gh label create "Terraform"                   --repo "$REPO" --color "3D69A9" --description ""
gh label create "auto-deploy-production"      --repo "$REPO" --color "F42DCD" --description "Automatically deploy to production after validating in staging"
gh label create "proto release"               --repo "$REPO" --color "66AC62" --description ""
gh label create "ai-full"                     --repo "$REPO" --color "c2e0c6" --description "AI usage for code and tests."
gh label create "ai-code"                     --repo "$REPO" --color "fef2c0" --description "AI usage for code."
gh label create "ai-tests"                    --repo "$REPO" --color "f9d0c4" --description "AI usage for tests."
gh label create "ai-none"                     --repo "$REPO" --color "BFA998" --description "No or limited AI usage."
gh label create "please-ai-review"            --repo "$REPO" --color "fa8b49" --description "Cursor Review"
```

Run all commands. Each should succeed. If a label already exists, `gh label create` will error — that's fine, skip it.
