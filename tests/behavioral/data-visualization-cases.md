# Behavioral Tests — Department of Data Visualization

**Persona:** reflective-architect (head of department)
**Grammar:** sci-data-visualization.ebnf
**Bootstrapped by:** /demerzel metabuild

## Test 1: Chart Type Selection

**Given:** A dataset showing quarterly revenue by product line over 3 years
**When:** The reflective-architect recommends a visualization
**Then:**
- Recommends line chart or small multiples (temporal trend + comparison)
- Does NOT recommend pie chart (temporal trends are not part-to-whole)
- References data_relationship = temporal_trend + comparison
- Explains why position encoding outperforms angle encoding for this task
- Cites Cleveland & McGill's perceptual ranking

## Test 2: Color Accessibility

**Given:** A categorical color palette using red and green for two categories
**When:** The department evaluates the palette
**Then:**
- Flags red-green combination as inaccessible (deuteranopia, protanopia)
- Recommends colorblind-safe alternatives (blue-orange, or use shape encoding)
- References perceptual_consideration = color_blindness
- Does NOT dismiss accessibility as optional
- Suggests testing with colorblind simulation tools

## Test 3: Misleading Visualization Detection

**Given:** A bar chart with a y-axis starting at 95% instead of 0%
**When:** The department assesses the chart
**Then:**
- Identifies truncated axis as a bias_awareness = truncated_axis issue
- Calculates the lie factor (visual difference / data difference)
- Recommends either starting at 0% or using a slope/change chart
- References Tufte's lie factor concept
- Produces C (contradictory) belief if the chart is presented as "showing dramatic growth"

## Test 4: Domain Boundaries

**Given:** A question about the mathematical proof that Poincaré disk preserves angles
**When:** The data-visualization department receives the question
**Then:**
- Recognizes overlap with mathematics department (conformal mapping)
- Can discuss the visualization implications (why angles matter for perception)
- Redirects the proof to mathematics
- May note that angle preservation is why hyperbolic layouts feel "natural"

## Test 5: Framework Selection

**Given:** A requirement for a real-time dashboard showing 100,000 data points updating every second
**When:** The department recommends a rendering approach
**Then:**
- Recommends Canvas or WebGL over SVG (performance at scale)
- References interaction_framework selection criteria
- Notes that SVG is better for < 5,000 elements with interaction
- Suggests deck.gl or WebGL for the geospatial/large-data case
- Does NOT recommend D3.js force layout for 100K nodes (performance)

## Test 6: Hyperbolic Layout Expertise

**Given:** A question about navigating a deep hierarchy with 5+ levels
**When:** The department investigates via hyperbolic_domain
**Then:**
- Recommends Poincaré disk or ball model for focus+context
- Explains that hyperbolic space naturally embeds trees with exponential branching
- References navigation_pattern = plunge_navigation + breadcrumb_path
- Contrasts with alternatives: sunburst (fixed depth), treemap (area-based), icicle (linear)
- Can cite Lamping & Rao (1994) hyperbolic browser

## Test 7: Research Cycle Integration

**Given:** A research cycle runs for data-visualization department
**When:** The cycle selects a question from research_areas
**Then:**
- Question is within the 8 defined research areas
- Hypothesis method weighted by weights (empirical 0.30, simulation 0.25 favored)
- Conclusion maps to tetravalent logic
- If confirm → course produced in courses/data-visualization/en/
- Weights updated per grammar-evolution-policy
