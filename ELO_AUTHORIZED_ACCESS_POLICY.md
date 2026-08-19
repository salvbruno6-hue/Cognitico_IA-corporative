# ELO Authorized Access Policy — Identity & Operation Restrictions

**Status**: NORMATIVE  
**Authority**: Security & Governance  
**Effective**: 2026-08-19  
**Purpose**: Control repository access based on Git user email identity

---

## Executive Summary

This policy enforces **identity-based access control** where:

- ✅ **Authorized users** (company email domains) → Full read/write/governance
- 🔒 **Unauthorized users** (external/guest email) → READ-ONLY mode (search, view, consult)
- 🚫 **Blocked operations** → No commits, no PRs, no modifications

---

## 1. User Classification

### 1.1 Authorized Users

**Definition**: Users with **approved company email domains**

```yaml
authorized_domains:
  - "@cognitico.com"        # Primary company domain
  - "@elo-ecosystem.io"     # ELO operational domain
  - "@salvbruno6.dev"       # Architect domain (if applicable)
```

**Capabilities**:
- ✅ Clone repository
- ✅ Read all content (public/private)
- ✅ Create branches
- ✅ Commit changes
- ✅ Create pull requests
- ✅ Merge approved PRs
- ✅ Modify architecture/governance documents
- ✅ Execute admin operations

**Example Authorized Emails**:
```
john.doe@cognitico.com
architect@elo-ecosystem.io
salvbruno@cognitico.com
```

### 1.2 Unauthorized Users

**Definition**: Users with **external email domains** or **no company identity**

```yaml
unauthorized_domains:
  - "@gmail.com"
  - "@outlook.com"
  - "@yahoo.com"
  - "@protonmail.com"
  - Any domain not in authorized_domains list
```

**Capabilities** (READ-ONLY):
- ✅ View repository content
- ✅ Read all documents
- ✅ Search and query information
- ✅ Review architectural decisions (ADRs)
- ✅ Access knowledge base
- ✅ View governance rules
- ✅ Run analysis (no execution)
- ✅ Submit consultation requests
- 🚫 **NO** commit access
- 🚫 **NO** branch creation
- 🚫 **NO** PR submission
- 🚫 **NO** modifications
- 🚫 **NO** admin access

**Example Unauthorized Emails**:
```
external.contractor@gmail.com
guest@partner-company.com
consultant@freelance-provider.com
```

---

## 2. Access Control Rules

### 2.1 Read Operations (ALLOWED for all)

| Operation | Authorized | Unauthorized | Notes |
|-----------|:-----------:|:------------:|-------|
| Clone repo | ✅ | ✅ | Read-only clone for unauthorized |
| View files | ✅ | ✅ | Full access to documentation |
| View commits | ✅ | ✅ | History visible |
| View branches | ✅ | ✅ | Branch list visible |
| View PRs | ✅ | ✅ | PR discussion visible |
| Search code | ✅ | ✅ | Full semantic search |
| View issues | ✅ | ✅ | Issue tracking visible |
| Read ADRs | ✅ | ✅ | Architecture history visible |
| Access governance | ✅ | ✅ | Policies readable |
| Run read-only queries | ✅ | ✅ | Analysis tools allowed |

### 2.2 Write Operations (BLOCKED for unauthorized)

| Operation | Authorized | Unauthorized | Consequences |
|-----------|:-----------:|:------------:|-------|
| Create branch | ✅ | 🚫 | **BLOCKED** — permission denied |
| Commit code | ✅ | 🚫 | **BLOCKED** — push rejected |
| Create PR | ✅ | 🚫 | **BLOCKED** — PR submission blocked |
| Merge PR | ✅ | 🚫 | **BLOCKED** — merge blocked |
| Modify document | ✅ | 🚫 | **BLOCKED** — file modification rejected |
| Delete branch | ✅ | 🚫 | **BLOCKED** — deletion rejected |
| Update issue | ✅ | 🚫 | **BLOCKED** — edit rejected |
| Create tag | ✅ | 🚫 | **BLOCKED** — tag creation rejected |
| Admin operations | ✅ | 🚫 | **BLOCKED** — admin access denied |

### 2.3 Consultation Mode (Allowed for unauthorized)

Unauthorized users can **submit consultation requests** without modifying repository:

- ✅ Ask questions via GitHub Discussions
- ✅ Request analysis
- ✅ Propose features in Discussions (not code)
- ✅ Review consulting responses
- 🚫 Cannot merge proposals into code
- 🚫 Cannot execute decisions
- 🚫 Cannot commit changes

---

## 3. Identity Verification

### 3.1 Git User Configuration

**Authorized users MUST configure Git with company email**:

```bash
git config user.email "yourname@cognitico.com"
git config --global user.email "yourname@cognitico.com"
```

### 3.2 Commit Validation

Every commit is validated:

```yaml
validation_rules:
  - Check author email in commit
  - Check committer email in commit
  - Reject if not in authorized_domains
  - Log attempt with timestamp
  - Notify security team of unauthorized attempt
```

### 3.3 Allowed Commit Patterns

```
✅ ALLOWED
Author: John Doe <john.doe@cognitico.com>
Committer: John Doe <john.doe@cognitico.com>

❌ BLOCKED
Author: John Doe <john.doe@gmail.com>
Committer: John Doe <john.doe@gmail.com>

⚠️ MIXED (Suspicious - requires review)
Author: John Doe <john.doe@cognitico.com>
Committer: John Doe <john.doe@gmail.com>
```

---

## 4. Pre-commit Hook Implementation

### 4.1 Local Hook (`.git/hooks/pre-commit`)

Place in `scripts/git-hooks/pre-commit`:

```bash
#!/bin/bash

# ELO Authorized Access Policy - Pre-commit Hook

AUTHORIZED_DOMAINS=(
  "cognitico.com"
  "elo-ecosystem.io"
  "salvbruno6.dev"
)

# Get committer email
COMMITTER_EMAIL=$(git config user.email)
AUTHOR_EMAIL=$(git var GIT_AUTHOR_IDENT | cut -d '<' -f 2 | cut -d '>' -f 1)

echo "Validating commit identity..."
echo "  Author: $AUTHOR_EMAIL"
echo "  Committer: $COMMITTER_EMAIL"

# Check if email is authorized
AUTHORIZED=false
for domain in "${AUTHORIZED_DOMAINS[@]}"; do
  if [[ "$COMMITTER_EMAIL" == *"@$domain" ]]; then
    AUTHORIZED=true
    break
  fi
done

if [ "$AUTHORIZED" = false ]; then
  echo ""
  echo "❌ COMMIT REJECTED"
  echo ""
  echo "Your Git email is NOT authorized for this repository:"
  echo "  Email: $COMMITTER_EMAIL"
  echo ""
  echo "Authorized domains:"
  for domain in "${AUTHORIZED_DOMAINS[@]}"; do
    echo "  - @$domain"
  done
  echo ""
  echo "To fix this, run:"
  echo "  git config user.email 'yourname@cognitico.com'"
  echo ""
  echo "If you need write access, contact: security@cognitico.com"
  echo ""
  exit 1
fi

echo "✅ Identity verified"
exit 0
```

### 4.2 Install Hook

```bash
cp scripts/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## 5. Push Protection Rules

### 5.1 Server-side Validation (GitHub Branch Protection)

Configure in **Settings → Branches → Branch Protection Rules**:

```yaml
branch_protection:
  pattern: "main"
  
  require_status_checks: true
  checks:
    - "ELO-Auth-Verification"
    - "Email-Domain-Validation"
  
  require_code_review: true
  dismiss_stale_reviews: false
  require_review_from_code_owners: true
  
  restrict_who_can_push_to_matching_branches: true
  allow_only:
    - "authorized_users_role"
```

### 5.2 GitHub Actions Workflow — Email Validation

Create `.github/workflows/elo-auth-check.yml`:

```yaml
name: "ELO Auth Verification"

on:
  pull_request:
  push:
    branches:
      - main
      - dev

jobs:
  verify_author:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Extract author email
        id: author
        run: |
          AUTHOR_EMAIL=$(git log -1 --pretty=format:'%ae')
          echo "email=$AUTHOR_EMAIL" >> $GITHUB_OUTPUT
          echo "Detected author: $AUTHOR_EMAIL"

      - name: Validate email domain
        id: validate
        run: |
          AUTHOR_EMAIL="${{ steps.author.outputs.email }}"
          AUTHORIZED_DOMAINS="cognitico.com|elo-ecosystem.io|salvbruno6.dev"
          
          if echo "$AUTHOR_EMAIL" | grep -E "@($AUTHORIZED_DOMAINS)$" > /dev/null; then
            echo "✅ Author authorized"
            echo "result=success" >> $GITHUB_OUTPUT
            exit 0
          else
            echo "❌ Author NOT authorized: $AUTHOR_EMAIL"
            echo "result=blocked" >> $GITHUB_OUTPUT
            exit 1
          fi

      - name: Post failure message
        if: failure()
        run: |
          echo "# ❌ Access Denied"
          echo ""
          echo "Your Git email is not authorized for this repository."
          echo "Author detected: ${{ steps.author.outputs.email }}"
          echo ""
          echo "## Authorized domains:"
          echo "- @cognitico.com"
          echo "- @elo-ecosystem.io"
          echo "- @salvbruno6.dev"
          echo ""
          echo "## To resolve:"
          echo "1. Configure Git with authorized email:"
          echo "   \`\`\`bash"
          echo "   git config user.email 'yourname@cognitico.com'"
          echo "   \`\`\`"
          echo ""
          echo "2. Amend your commit:"
          echo "   \`\`\`bash"
          echo "   git commit --amend --no-edit"
          echo "   git push --force-with-lease"
          echo "   \`\`\`"
          echo ""
          echo "3. For access requests: security@cognitico.com"
```

---

## 6. Unauthorized User Workflow

### 6.1 What Unauthorized Users CAN Do

```mermaid
Unauthorized User (external@gmail.com)
  ↓
  ├─→ Clone repository (read-only)
  ├─→ View all documents
  ├─→ Read ADRs and governance
  ├─→ Search codebase
  ├─→ Review discussions
  ├─→ Submit consultation request
  └─→ View architectural decisions
  
  ✅ These operations allowed
```

### 6.2 What Unauthorized Users CANNOT Do

```mermaid
Unauthorized User (external@gmail.com)
  ↓
  ├─X→ Create branch
  ├─X→ Commit code
  ├─X→ Create pull request
  ├─X→ Modify files
  ├─X→ Update issues
  ├─X→ Delete branches
  └─X→ Admin operations
  
  ❌ These operations BLOCKED
```

### 6.3 Consultation Request Path

```yaml
workflow:
  1. Unauthorized user reviews documentation
  2. User submits question via GitHub Discussions
  3. System logs consultation request
  4. Authorized user reviews and responds
  5. Response sent via Discussions (read-only for user)
  6. User can implement based on consultation
  7. User submits for authorized team member to commit
```

---

## 7. Error Messages

### 7.1 Pre-commit Hook Error

```
❌ COMMIT REJECTED

Your Git email is NOT authorized for this repository:
  Email: external@gmail.com

Authorized domains:
  - @cognitico.com
  - @elo-ecosystem.io
  - @salvbruno6.dev

To fix this, run:
  git config user.email 'yourname@cognitico.com'

If you need write access, contact: security@cognitico.com

For READ-ONLY access:
  ✅ You can clone and review code
  ✅ You can search and analyze
  ✅ You can submit consultation requests
  ✅ You can participate in Discussions
```

### 7.2 GitHub Actions Error

```
❌ Access Denied

Your Git email is not authorized for this repository.
Author detected: external@gmail.com

Authorized domains:
  - @cognitico.com
  - @elo-ecosystem.io
  - @salvbruno6.dev

To resolve:
1. Configure Git with authorized email:
   git config user.email 'yourname@cognitico.com'

2. Amend your commit:
   git commit --amend --no-edit
   git push --force-with-lease

3. For access requests: security@cognitico.com
```

---

## 8. Audit and Logging

### 8.1 Log Unauthorized Attempts

Every unauthorized operation attempt is logged:

```yaml
log_entry:
  timestamp: "2026-08-19T12:30:45Z"
  email: "external@gmail.com"
  operation: "commit"
  branch: "main"
  result: "BLOCKED"
  reason: "Unauthorized domain"
  action: "Rejected push"
```

### 8.2 Security Team Notifications

```yaml
notification:
  severity: "INFO"
  recipients: ["security@cognitico.com"]
  message: "Unauthorized commit attempt from external@gmail.com"
  details:
    - Timestamp
    - Email
    - Operation
    - Branch
    - Commit message (first 100 chars)
```

---

## 9. Access Request Process

### 9.1 For Permanent Access

**If external user needs write access**:

1. **Request submission**:
   ```
   Email: security@cognitico.com
   Subject: "Access Request - [Name] - [Company]"
   Body:
     - Full name
     - Company/organization
     - Purpose
     - Start date
     - End date
     - Requested email domain
   ```

2. **Approval process**:
   - [ ] Security team reviews
   - [ ] Manager approval
   - [ ] Adds email domain to authorized_domains
   - [ ] User updates Git config
   - [ ] Access granted

3. **After approval**:
   ```bash
   git config user.email 'contractor@partner-company.com'
   # Update authorized_domains in this policy
   ```

### 9.2 Temporary Contractors

For short-term consultants:

```yaml
temporary_access:
  duration: "30 days"
  email_domain: "@contractor-agency.com"
  expires: "2026-09-19"
  scope: "Review and consultation only"
  auto_revoke: true
```

---

## 10. Configuration

### 10.1 Authorized Domains List

```yaml
# Update this section to add/remove domains
authorized_domains:
  - "cognitico.com"        # Primary company
  - "elo-ecosystem.io"     # ELO ecosystem
  - "salvbruno6.dev"       # Architect domain

# Contractors (temporary)
temporary_authorized:
  - email: "contractor@partner-agency.com"
    expires: "2026-09-19"
    reason: "30-day engagement"
```

### 10.2 How to Update Authorized Domains

1. **Modify this file**:
   - Edit `authorized_domains` section
   - Commit with authorized email

2. **Update pre-commit hook**:
   - Update `scripts/git-hooks/pre-commit`
   - Commit changes

3. **Update GitHub Actions workflow**:
   - Update `.github/workflows/elo-auth-check.yml`
   - Commit changes

4. **Announce changes**:
   - Email security@cognitico.com
   - Update team documentation

---

## 11. Emergency Access

### 11.1 If Authorized User Loses Access

```bash
# If pre-commit hook blocks you:
# 1. Verify Git config
git config user.email

# 2. Should show authorized email
# Expected: yourname@cognitico.com

# 3. If wrong, fix it:
git config user.email 'yourname@cognitico.com'

# 4. Amend previous commit:
git commit --amend --no-edit

# 5. Push
git push --force-with-lease
```

### 11.2 Contact Security

If you believe this is an error:

```
Email: security@cognitico.com
Subject: "Emergency Access Request"
Include:
  - Your Git email
  - Your company email
  - Reason for access
  - Manager approval (if new employee)
```

---

## 12. Implementation Checklist

- [ ] Authorized domains list created
- [ ] Pre-commit hook written and placed
- [ ] GitHub Actions workflow created
- [ ] Branch protection rules enabled
- [ ] Error messages documented
- [ ] Audit logging configured
- [ ] Access request process defined
- [ ] All team members notified
- [ ] Security team trained
- [ ] Contingency plan created

---

## 13. Status and Review

| Property | Value |
|----------|-------|
| **Status** | NORMATIVE |
| **Authority** | Security & Governance |
| **Effective** | 2026-08-19 |
| **Owner** | Security Team |
| **Last Review** | 2026-08-19 |
| **Next Review** | 2026-09-19 (or when domains change) |

---

**This policy ensures that only authorized company users can modify the ELO repository, while external users retain full read and consultation access.**
