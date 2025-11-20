# Talent Signal Agent: User Guide

## What is the Talent Signal Agent?

The Talent Signal Agent is an AI-powered tool that helps you match executive candidates with open roles at FirstMark portfolio companies. Instead of manually researching each candidate, the system automatically gathers information from public sources, evaluates candidates against your role requirements, and provides structured assessments to help you make faster, more informed hiring decisions.

## How It Works

### Overview

The system operates through Airtable, which you're already familiar with. When you're ready to screen candidates for a role, you simply:

1. Create a Screen record in Airtable
2. Link candidates you want to evaluate
3. Link the role specification (evaluation criteria)
4. Change the Screen status to "Ready to Screen"

The AI agent then automatically:
- Researches each candidate using public data sources
- Evaluates them against your role requirements
- Generates detailed assessments with scores and evidence
- Updates Airtable with the results

### The 4-Step Process

Behind the scenes, the system follows a systematic workflow for each candidate:

**Step 1: Deep Research**
- Gathers comprehensive information about the candidate
- Sources include LinkedIn, company websites, news articles, funding databases
- Identifies career history, achievements, and relevant experience
- Collects evidence with citations (links to sources)

**Step 2: Quality Check**
- Verifies the research has sufficient evidence (at least 3 citations)
- Ensures the profile is complete enough for accurate assessment
- If gaps exist, triggers additional research (Step 3)
- If quality is good, proceeds directly to assessment (Step 4)

**Step 3: Incremental Search (only when needed)**
- Runs only if the initial research had gaps
- Performs targeted additional searches to fill specific information gaps
- Merges new findings with existing research

**Step 4: Assessment**
- Evaluates the candidate against your role specification
- Scores each evaluation dimension (e.g., Fundraising Experience, Team Building)
- Identifies strengths, concerns, and key evidence
- Generates an overall match score

## Working with Airtable

### Setting Up a Screen

**What You Need:**
- **Candidates:** Executives you want to evaluate (from the People table)
- **Role Spec:** The evaluation criteria for the position (from the Role_Specs table)
- **Search:** The portfolio company role (from the Searches table)

**Step-by-Step:**

1. **Create a Screen Record**
   - Go to the Platform-Screens table in Airtable
   - Create a new record

2. **Link the Search**
   - In the "Search" field, link to the relevant Search record
   - This connects the Screen to both the role and the portfolio company

3. **Link Candidates**
   - In the "Candidates" field, link all executives you want to evaluate
   - You can add 1-50 candidates (though 5-15 is typically optimal)

4. **Select Role Specification**
   - The role spec is automatically pulled from the linked Search
   - OR you can use "Custom Spec" mode for one-off evaluations (see below)

5. **Trigger the Screen**
   - Change the "Status" field to "Ready to Screen"
   - The AI agent will automatically start processing
   - Status will change to "Processing" while running
   - Status will change to "Complete" when finished

### Choosing Your Evaluation Criteria

The system offers two ways to specify what you're evaluating candidates against:

**Option 1: Search Spec (Recommended for Standard Evaluations)**
- Uses the reusable Role_Spec linked to your Search
- Best for consistent evaluations across multiple screening batches
- Example: You have a "CFO - Series B SaaS" spec you use regularly

**How to Use:**
1. Ensure your Search is linked to a Role_Spec record
2. Set "Role Spec Selection" to "Search Spec" (this is the default)
3. The system will use the linked Role_Spec

**Option 2: Custom Spec (For Testing or One-Off Evaluations)**
- Write evaluation criteria directly in the Screen record
- Best for experimental criteria or A/B testing different approaches
- Example: Testing "growth-stage CFO" vs "pre-IPO CFO" criteria

**How to Use:**
1. Set "Role Spec Selection" to "Custom Spec"
2. Paste your custom evaluation criteria into the "Custom Role Spec Content" field
3. The system will use your custom text instead of the linked spec

**Audit Trail:**
The system automatically creates a snapshot of whichever spec you used when the Screen starts processing. This ensures you can always trace back which criteria were applied, even if specs are later edited or deleted.

### Understanding the Results

Once a Screen completes, you'll find Assessment records created in the Platform-Assessments table.

**Each Assessment Contains:**

**Overall Match Score (0-100)**
- A composite score reflecting how well the candidate matches the role
- Based on averaging scored evaluation dimensions
- `None` if there's insufficient evidence to evaluate

**Confidence Level (High/Medium/Low)**
- How confident the AI is in its assessment
- Based on evidence quality and completeness
- Higher confidence = more robust public information available

**Topline Summary**
- 2-3 sentence overview of the candidate's fit
- Highlights key strengths and concerns
- Written in plain language for quick review

**Dimension Scores**
- Individual scores (1-5) for each evaluation criterion
- Examples: "Fundraising Experience", "Team Building", "Technical Leadership"
- Each dimension includes reasoning and evidence quotes
- Scores can be `None` if evidence is insufficient for that specific dimension

**Must-Have Requirements**
- Binary check (Met/Not Met) for critical requirements
- Example: "10+ years finance leadership" → Met: Yes
- Includes evidence for each requirement

**Green Flags & Red Flags**
- **Green Flags:** Positive signals (e.g., "Led $100M Series C", "Built team from 5 to 50")
- **Red Flags:** Potential concerns (e.g., "Frequent job changes", "Limited B2B experience")
- Based on evidence from research

**Counterfactuals**
- "Why this candidate might NOT be ideal"
- Helps identify potential blind spots
- Encourages balanced consideration

**Citations**
- Links to all sources used in the assessment
- Typically includes LinkedIn, company sites, news articles
- Allows you to verify evidence independently

### Example Assessment Output

Here's what an actual assessment looks like for a CFO candidate:

```
Candidate: Sarah Chen
Role: CFO - Series B SaaS (Pigment)
Overall Score: 84/100
Confidence: High

TOPLINE SUMMARY
Sarah Chen is a strong match for the Pigment CFO role. She brings 12+ years
of finance leadership in B2B SaaS (Zendesk, Atlassian), led two successful
Series B→C fundraises ($50M+), and scaled finance teams from 3 to 25. Limited
exposure to international expansion may be a gap for Pigment's European growth.

DIMENSION SCORES
• Fundraising Experience: 5/5
  - Led Series C ($75M) at Zendesk, Series B ($50M) at Atlassian
  - Evidence: "Closed oversubscribed Series C with Sequoia, Index" (LinkedIn)

• Team Building: 4/5
  - Scaled finance from 3 to 25 people across FP&A, accounting, tax
  - Evidence: "Built finance org supporting 400% revenue growth" (News article)

• SaaS Metrics Expertise: 5/5
  - Deep ARR, CAC, LTV experience in B2B subscription businesses
  - Evidence: Multiple mentions of SaaS metrics in talks, blog posts

• International Finance: None
  - No public evidence of multi-currency or international operations experience
  - This dimension cannot be scored due to insufficient data

MUST-HAVE REQUIREMENTS
✓ 10+ years finance leadership: Met (12 years confirmed)
✓ Series B+ fundraising experience: Met (2 rounds, $125M total)
✓ B2B SaaS background: Met (100% of career in B2B SaaS)

GREEN FLAGS
• Oversubscribed fundraises (investor demand signal)
• Quick progression: Controller → VP Finance → CFO in 6 years
• Public speaking on SaaS metrics (thought leadership)

RED FLAGS
• Average tenure 2.5 years per company (potential retention risk)
• No international expansion experience (Pigment needs EU expertise)

COUNTERFACTUALS (Why Sarah Might NOT Be Ideal)
While Sarah has strong fundraising credentials, her companies were US-centric.
Pigment's European expansion may require multi-currency, VAT, and cross-border
finance expertise that isn't evident in her background. Her 2-3 year tenures
could indicate restlessness or external recruiting pressure.

KEY ASSUMPTIONS
• LinkedIn profile is current (last updated 3 months ago)
• News articles accurately represent her role scope
• Company size data from Crunchbase/Pitchbook is reliable

CITATIONS
• https://linkedin.com/in/sarahchen
• https://techcrunch.com/2021/zendesk-series-c
• https://saasmetrics.co/author/sarah-chen
• https://www.crunchbase.com/person/sarah-chen
```

**Key Takeaways from This Example:**
- **Overall score (84)** suggests strong fit, but not perfect
- **None score** for International Finance shows evidence-aware assessment (unknown ≠ poor)
- **Citations** allow you to verify claims (e.g., check LinkedIn for fundraising details)
- **Counterfactuals** encourage balanced evaluation despite high score
- **Red flags** surface even for high-scoring candidates

### Interpreting Scores

**Overall Score:**
- **80-100:** Strong match - candidate aligns well with requirements
- **60-79:** Moderate match - some alignment, but gaps exist
- **40-59:** Weak match - significant gaps or misalignment
- **0-39:** Poor match - candidate doesn't meet key criteria
- **None:** Insufficient evidence - need more public information

**Dimension Scores (1-5 scale):**
- **5:** Exceptional - exceeds requirements significantly
- **4:** Strong - clearly meets requirements
- **3:** Adequate - meets basic requirements
- **2:** Limited - some relevant experience, but gaps
- **1:** Minimal - little to no relevant experience
- **None:** Unknown - insufficient evidence to score

**Confidence Levels:**
- **High:** Robust public profile with multiple high-quality sources
- **Medium:** Adequate information, but some gaps
- **Low:** Limited public information - may need manual research

## Best Practices

### What Good Looks Like: Success Metrics

Understanding what to expect helps you evaluate system performance and identify issues early.

**Typical Results Distribution (10-candidate screen):**
- **High Confidence assessments:** 6-8 candidates (60-80%)
- **Medium Confidence:** 2-3 candidates (20-30%)
- **Low Confidence:** 0-1 candidates (0-10%)

**Citation Quality:**
- **Target:** 5-8 citations per candidate
- **Minimum:** 3 citations (quality gate threshold)
- **Sources:** LinkedIn (100%), news articles (40-60%), company sites (30-50%), funding databases (20-40%)

**Dimension Coverage:**
- **Expected:** 70-90% of dimensions scored (not "None")
- **Red flag:** <50% scored (indicates spec mismatch or insufficient public data)

**Score Distribution:**
- **Well-calibrated spec:** Scores range 40-90 with clear differentiation
- **Too easy spec:** Most candidates score 80+ (consider adding harder criteria)
- **Too hard spec:** Most candidates score <50 (may need to adjust expectations)

**Processing Performance:**
- **Per-candidate time:** 3-5 minutes average
- **Quality research (Step 1):** ~2-3 minutes
- **Incremental search (Step 3, when triggered):** ~1-2 minutes additional
- **Assessment (Step 4):** ~1-2 minutes

### Getting Quality Results

**1. Ensure Candidates Have Public Profiles**
- The system relies on publicly available information
- LinkedIn profiles are the most valuable source (strongly recommend 100% coverage)
- News articles, company sites, and funding databases also help
- Candidates with minimal online presence will have lower confidence scores
- **Pre-screen check:** Search candidate name + company on Google - if <5 results, expect Low confidence

**2. Write Clear Role Specifications**
- Be specific about requirements (e.g., "10+ years" vs "extensive experience")
- Include both must-haves and nice-to-haves
- Define evaluation dimensions clearly (3-6 dimensions is optimal)
- Provide context about the company stage and challenges
- **Example good dimension:** "Fundraising Experience: Has led or participated in Series B+ fundraises ($30M+) in B2B SaaS"
- **Example poor dimension:** "Good at finance" (too vague)

**3. Use Consistent Specs for Comparable Results**
- If comparing candidates, use the same role spec
- Save reusable specs in the Role_Specs table
- Use "Custom Spec" only for one-off evaluations or A/B testing
- **Tip:** Version your specs (e.g., "CFO - Series B v1", "CFO - Series B v2") to track iterations

**4. Review Multiple Candidates Together**
- Screen 5-15 candidates at once for better comparison
- Use Airtable views to sort by score or specific dimensions
- Look for patterns across assessments (e.g., if all candidates score low on one dimension, spec might be too strict)
- **Comparative review trick:** Create filtered view showing only High confidence + score >70 for quick shortlisting

**5. Verify Key Evidence**
- Check citations for critical claims (especially high-impact dimensions like fundraising, team size)
- Use assessments as a starting point, not the final decision
- Supplement with interviews and reference checks
- **Red flag check:** If a claim seems too good to be true, click the citation to verify

### A/B Testing Evaluation Criteria

Want to test different evaluation approaches? Use Custom Specs:

**Example Scenario:** Test "growth-stage CFO" vs "pre-IPO CFO" criteria

**Setup:**
1. Create Screen 1:
   - Set "Role Spec Selection" = "Custom Spec"
   - Paste growth-stage CFO criteria in "Custom Role Spec Content"
   - Link candidates: Alex, Jordan, Sam

2. Create Screen 2:
   - Set "Role Spec Selection" = "Custom Spec"
   - Paste pre-IPO CFO criteria in "Custom Role Spec Content"
   - Link the same candidates: Alex, Jordan, Sam

3. Run both Screens and compare results side-by-side

**Benefits:**
- Same candidates, different evaluation lenses
- Easy to compare scores and reasoning
- Helps refine your evaluation criteria
- Full audit trail preserved in Assessments

### Monitoring Progress

**While a Screen is Running:**
- Status shows "Processing"
- You can view real-time progress in the AgentOS control plane (ask your technical team for access)
- Typical processing time: 3-5 minutes per candidate

**Expected Timeline:**
- **Small screens (1-3 candidates):** 5-15 minutes total
- **Medium screens (5-10 candidates):** 20-50 minutes total
- **Large screens (15-20 candidates):** 60-90 minutes total

If a Screen takes significantly longer than expected, check the troubleshooting guide below.

### Troubleshooting

**Screen Status Stuck on "Processing"**

*Symptoms:* Screen has been "Processing" for >2 hours, no new assessments appearing

*Common Causes:*
1. **API rate limits reached** - OpenAI has usage caps that may delay processing
2. **Webhook timeout** - Initial automation call may have failed
3. **Invalid data** - Malformed candidate data (e.g., broken LinkedIn URLs)

*How to Diagnose:*
1. Check **Operations-Automation_Log** table for error messages
2. Look for entries matching your Screen ID
3. Check timestamp - errors usually appear within 5 minutes of triggering

*How to Fix:*
- **If no log entry exists:** Webhook never fired. Re-trigger by changing status to "Draft" then back to "Ready to Screen"
- **If API error in logs:** Wait 1 hour and re-trigger (rate limits reset hourly)
- **If data validation error:** Fix the candidate data (LinkedIn URL, bio field, etc.) and re-trigger

**Assessment Fields Are Empty**

*Symptoms:* Assessment record created but overall_score, summary, or dimension_scores are blank

*Common Causes:*
1. **Insufficient public data** - Candidate has minimal online presence
2. **Research quality gate failed** - System couldn't find 3+ citations
3. **Workflow interruption** - Process stopped mid-execution

*How to Diagnose:*
1. Check the Assessment record's "citations" field - is it empty or <3 URLs?
2. Check Operations-Automation_Log for workflow completion messages
3. Search for the candidate on LinkedIn/Google yourself to validate data availability

*How to Fix:*
- **If citations < 3:** Candidate likely needs manual research (insufficient public data)
- **If citations = 0:** Workflow failed. Check logs and re-trigger Screen
- **Prevention:** Before screening, verify candidates have LinkedIn profiles with work history

**Scores Seem Wrong or Inconsistent**

*Symptoms:* Dimension scores don't align with evidence, or overall score seems off

*Common Causes:*
1. **Spec mismatch** - Wrong Role_Spec was used (check spec_snapshot field)
2. **Evidence misinterpretation** - AI misread source material
3. **Outdated public data** - LinkedIn/sources haven't been updated by candidate

*How to Diagnose:*
1. Review **citations** - do they support the claims?
2. Check **spec_snapshot** field - is this the spec you intended?
3. Review **dimension reasoning** - does the logic make sense?

*How to Fix:*
- **If wrong spec:** Create new Screen with correct spec
- **If evidence misread:** Verify citations yourself, use assessment as one input (not sole decision)
- **If scores valid but unexpected:** Spec might be surfacing legitimate gaps - consider if criteria should be adjusted

**Common Edge Cases**

**Candidate Has No LinkedIn Profile**
- System will search other sources (news, company sites, Crunchbase)
- Confidence will likely be "Low"
- Many dimensions may score "None" (insufficient evidence)
- **Recommendation:** Flag for manual research or phone screen

**Candidate Changed Jobs Recently**
- Public sources may be outdated (LinkedIn lag, old news articles)
- Assessment will reflect publicly available data, not current reality
- **Recommendation:** Check "Last Updated" dates in citations, supplement with direct outreach

**Candidate Works at Stealth Startup**
- Limited public information available (by design)
- Many dimensions will score "None"
- **Recommendation:** Use Custom Spec focused on verifiable experience (e.g., prior roles), not current company

**Multiple Candidates with Similar Names**
- System may pull information from wrong person
- **How to Detect:** Check citations - do they match the candidate's actual LinkedIn?
- **How to Fix:** Ensure candidate_linkedin field has correct URL before screening

## Common Use Cases

### Use Case 1: Screening for a New Role

**Scenario:** Pigment needs a CFO. You have 10 candidates from your network.

**Steps:**
1. Create a Search record for "Pigment - CFO"
2. Link it to your "CFO - Series B SaaS" Role_Spec
3. Create a Screen record
4. Link the Search and all 10 candidates
5. Set Status to "Ready to Screen"
6. Review assessments when complete
7. Shortlist top 3-4 candidates based on scores and evidence

### Use Case 2: Comparing Candidates Across Multiple Roles

**Scenario:** You're filling 3 roles (CFO, CTO, VP Sales) and have overlapping candidate pools.

**Steps:**
1. Create 3 separate Screens (one per role)
2. Each Screen links to its own role spec
3. Link relevant candidates to each Screen (some may appear in multiple)
4. Run all Screens
5. Use Airtable filters to see how each candidate scored across different roles
6. Identify candidates who might fit multiple positions

### Use Case 3: Refining Your Evaluation Criteria

**Scenario:** Your current CFO spec isn't surfacing the right candidates.

**Steps:**
1. Create a Screen using your current spec (Search Spec mode)
2. Create a second Screen with modified criteria (Custom Spec mode)
3. Use the same candidate pool for both
4. Compare results to see which criteria better identify strong candidates
5. Update your reusable Role_Spec based on learnings

## Understanding the Evidence-Aware System

The Talent Signal Agent uses "evidence-aware assessment," which means it explicitly tracks what it knows and doesn't know about each candidate.

### Key Principles

**1. Unknown ≠ Zero**
- If evidence is missing for a dimension, the score is `None` (not 0)
- Example: If LinkedIn doesn't mention fundraising, "Fundraising Experience" score = None
- This prevents penalizing candidates for incomplete public profiles

**2. Citations Required**
- Every claim is backed by a source
- Minimum 3 citations for quality assessment
- You can verify evidence independently

**3. Confidence Self-Assessment**
- The AI evaluates its own confidence per dimension
- Helps you know which scores are robust vs tentative

**4. Counterfactuals for Balance**
- Every assessment includes "why NOT" reasoning
- Encourages considering both sides
- Helps avoid overconfidence in high scores

## Frequently Asked Questions

**Q: How long does screening take?**
A: Typically 3-5 minutes per candidate. A Screen with 10 candidates takes about 30-50 minutes total.

**Q: What if a candidate has no LinkedIn profile?**
A: The system will still search other sources (news, company sites), but confidence will likely be lower. Consider manual research for these candidates.

**Q: Can I re-screen a candidate with different criteria?**
A: Yes! Create a new Screen with different role spec settings and link the same candidate. Both assessments will be preserved.

**Q: Why is a dimension score `None`?**
A: The system found insufficient public evidence to score that dimension. This is different from a low score—it means "unknown," not "bad."

**Q: Can I edit an assessment after it's created?**
A: Assessments are read-only to maintain audit trails. If you need to re-evaluate, create a new Screen.

**Q: How do I access the AgentOS control plane?**
A: Ask your technical team for access. The control plane shows real-time workflow progress, which is especially useful for demos and debugging.

**Q: What happens if the system makes a mistake?**
A: The system is a tool to augment your judgment, not replace it. Always verify key evidence via citations and use assessments as one input among many (interviews, references, etc.).

**Q: Can I screen candidates who aren't in Airtable yet?**
A: No, candidates must first be added to the Platform-People table. This ensures all candidate data is centralized.

**Q: How many candidates can I screen at once?**
A: Technically up to 50, but 5-15 is optimal for manageable review and comparison.

## Getting Help

**For Airtable Questions:**
- Check field descriptions in Airtable (hover over field names)
- Review example Screen records in the "Demo Screens" view

**For Technical Issues:**
- Contact your technical team
- Check the Operations-Automation_Log table for error messages
- Provide the Screen ID when reporting issues

**For Evaluation Strategy:**
- Review successful past screens to see what worked
- Experiment with Custom Specs to refine criteria
- Compare high-confidence assessments to actual hire outcomes

## Tips for Success

1. **Start Small:** Screen 2-3 candidates first to understand the output format
2. **Review Citations:** Check sources for key claims before making decisions
3. **Use Filters:** Create Airtable views to surface top candidates by score or specific dimensions
4. **Iterate Specs:** Refine your evaluation criteria based on which assessments correlate with successful hires
5. **Combine with Human Judgment:** Use assessments as one data point, not the sole decision factor
6. **Track Outcomes:** Note which high-scoring candidates performed well in interviews to validate the system

## Summary

The Talent Signal Agent automates the time-consuming research phase of executive screening, allowing you to:
- Evaluate more candidates faster
- Make evidence-based decisions
- Focus your time on high-potential matches
- Maintain consistent evaluation standards

Remember: The system is designed to augment your expertise, not replace it. Use it to surface insights and save time, then apply your judgment and experience to make final hiring decisions.
