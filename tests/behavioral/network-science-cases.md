# Behavioral Tests — Department of Network Science

**Persona:** reflective-architect (head of department)
**Grammar:** sci-network-science.ebnf
**Bootstrapped by:** /demerzel metabuild

## Test 1: Centrality Ranking

**Given:** A directed network of 8 nodes where node A has degree 2 but lies on 90% of all shortest paths
**When:** The reflective-architect ranks nodes by centrality
**Then:**
- Ranks node A highest on betweenness_centrality despite low degree_centrality
- Explains that degree_centrality and betweenness_centrality measure different structural roles
- Identifies node A as a broker / gatekeeper (centrality_interpretation = identifies_broker)
- Does NOT conflate high degree with high betweenness — they are orthogonal measures
- References betweenness_centrality ::= sum_sigma_paths / total_sigma_paths from grammar
- Notes that removing node A would maximally fragment the network

## Test 2: Community Detection

**Given:** A social network graph is provided; Louvain detects 3 communities but they seem too coarse (two dense cliques merged into one)
**When:** The department investigates the partition quality
**Then:**
- Identifies the resolution limit: Louvain may merge small communities that are individually dense
- Recommends switching to Leiden algorithm or tuning the gamma resolution parameter
- Evaluates partition using modularity_Q and notes that higher Q does not always mean better partition
- References the resolution_limit production in grammar
- Does NOT accept Louvain output uncritically when dense sub-structures are visually apparent
- Produces U (Unknown) belief if gamma calibration data is unavailable

## Test 3: Resilience Assessment

**Given:** A scale-free infrastructure network (power-law exponent gamma ≈ 2.5) undergoes random node failure at 20% removal
**When:** The department performs resilience analysis
**Then:**
- Predicts the network is robust to random failure (scale-free networks tolerate random removal well due to sparse low-degree nodes)
- Warns that the same network is highly vulnerable to targeted attack on hubs (degree-based or betweenness-based attack strategy)
- Computes or estimates the critical fraction f_c using the Molloy-Reed criterion
- References kappa = <k^2>/<k> — high kappa (heterogeneous) means lower f_c under targeted attack
- References robustness_measure = R_index (area under giant component curve)
- Produces T belief if empirical removal matches theoretical prediction; U if gamma is uncertain

## Test 4: MCP Federation Mapping

**Given:** The Demerzel MCP ecosystem has repos: Demerzel, ix, tars, ga, and tools: read_file, edit_file, bash, mcp_search, discord_reply
**When:** The department maps this as an mcp_network
**Then:**
- Models repos as mcp_node_set (Demerzel, ix, tars, ga)
- Models tool invocations as directed weighted edges in mcp_edge_set
- Applies centrality_analysis_on_mcp_network: identifies which repo is most central (likely Demerzel by governance_directive out-degree)
- Identifies governance_directive edges as directed (Demerzel → consumer repos)
- Identifies compliance_report edges as directed (consumer repos → Demerzel)
- Detects that tools with high betweenness (e.g., bash, read_file) are single points of federation failure
- Does NOT treat the MCP network as undirected — governance directives have explicit direction

## Test 5: Cross-Repo Dependency Analysis

**Given:** ix depends on 4 Demerzel personas, tars depends on 6 policies, ga depends on 3 constitutions and 2 personas
**When:** The department builds and analyzes the dependency graph
**Then:**
- Constructs a bipartite_graph: repos on one side, governance artifacts on the other
- Computes degree_centrality for artifacts to find which are most widely depended upon
- Identifies any artifact depended upon by all 3 repos as a critical shared dependency
- Flags removal or breaking change to such artifacts as high-resilience risk
- References bipartite_graph in graph_type production
- Produces C (contradictory) belief if a policy is both depended upon and slated for deprecation simultaneously

## Test 6: Critical Node Identification

**Given:** A network analyst asks which nodes to protect to maximize network resilience under budget constraint (protect at most 3 nodes)
**When:** The department applies resilience_domain analysis
**Then:**
- Ranks candidates by combined score: betweenness_centrality + degree_centrality + percolation_centrality
- Notes that protecting the top-3 betweenness nodes typically maximizes giant component retention under targeted attack
- References attack_strategy = betweenness_based_attack to model the adversary
- References robustness_measure = giant_component_fraction as the objective
- Does NOT recommend protecting purely high-degree nodes without betweenness check — hubs and bridges are distinct structural roles
- Recommends simulation to validate: generate temporal networks, remove unprotected nodes, measure R_index

## Test 7: Small-World Property Detection

**Given:** A collaboration network of 500 researchers; clustering coefficient C = 0.48, average path length L = 3.2; equivalent random graph has C_rand = 0.012, L_rand = 3.0
**When:** The department evaluates whether small-world topology is present
**Then:**
- Computes sigma = (C / C_rand) / (L / L_rand) = (0.48 / 0.012) / (3.2 / 3.0) = 40 / 1.067 ≈ 37.5
- Concludes sigma >> 1: strong small-world topology confirmed
- Confirms that high clustering (C >> C_rand) with short paths (L ~ L_rand) is the defining criterion
- References small_world_index ::= "sigma = (C/C_rand) / (L/L_rand)" from grammar
- Notes that Watts-Strogatz WS(500, k, beta) with small beta would reproduce these statistics
- Produces T belief for small-world property

## Test 8: Network Growth Model Selection

**Given:** A new platform is being designed; the team expects organic growth where established nodes attract more connections (rich-get-richer dynamics)
**When:** The department recommends a generative network model
**Then:**
- Recommends Barabasi-Albert model (BA(n, m)) as the appropriate generative model — preferential attachment produces the expected rich-get-richer topology
- Predicts the resulting network will exhibit power-law degree distribution P(k) ~ k^(-gamma) with gamma ≈ 3
- Warns that scale-free topology implies vulnerability to targeted hub attack — recommend resilience planning
- Does NOT recommend Erdos-Renyi (no preferential attachment) or Watts-Strogatz (models rewiring, not growth) for this scenario
- References preferential_attachment_test as a validation step: measure attachment kernel on real growth data once platform is live
- References network_model selection grammar section
- Recommends community_detection_on_repos once network reaches sufficient scale to identify emergent clusters
