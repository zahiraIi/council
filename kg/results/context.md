Context benchmark: 20 tasks, graph top-k=8, tokens = tiktoken cl100k (proxy)

| Setup | Avg tokens loaded | vs full KB | Gold-rule recall |
|---|---:|---:|---:|
| Full KB (all 33 files) | 27,288 | — | 100% |
| Hand-written bundles (index.yaml) | 4,199 | -85% | 100% |
| Graph retrieval (always + top-8) | 2,797 | -90% | 85% |
| Bundle + graph evidence (council design) | 4,761 | -83% | 100% |

Bundle + graph adds 2.5 out-of-bundle nodes per task on average (raw-source chunks and
cross-bundle rules the bundle can't reach).

Per task (bundle tokens / recall · graph tokens / recall):
- [media-buying] An ad set is at 1.3x break-even ROAS after 3 days. Should I scale it n — 5,268 / 100% · 3,610 / 100%
- [media-buying] CTR is 2%, CPC $1, but CVR is 0.4%. Kill the ad, iterate, or fix the p — 5,268 / 100% · 2,788 / 100%
- [media-buying] Plan the structure and daily budget for my next creative test batch. — 5,268 / 100% · 3,631 / 100%
- [script] Write 3 hooks for problem-aware dog owners scared of hurting their dog — 5,021 / 100% · 2,526 / 50%
- [script-check] Check this script's bridge and call to action. — 2,547 / 100% · 2,162 / 50%
- [deconstruct] Deconstruct this competitor's winning video ad transcript. — 5,570 / 100% · 2,485 / 100%
- [ad-copy] Write primary text and headlines for a static image ad. — 3,944 / 100% · 2,721 / 100%
- [mechanism] Build the unique mechanism for a quiet pet nail grinder. — 2,824 / 100% · 3,484 / 0%
- [angles] Generate 3 distinct ad angles for nervous dog owners. — 3,019 / 100% · 2,956 / 100%
- [desires] Extract the mass desires from these Reddit quotes about trimming pet n — 3,118 / 100% · 2,250 / 100%
- [page] Which landing page type should a problem-aware ad send traffic to? — 5,399 / 100% · 2,749 / 100%
- [page] Write the advertorial headline, hero image direction and lead copy. — 5,399 / 100% · 2,682 / 100%
- [offer] Design a bundle offer that raises AOV for a durable tool. — 4,111 / 100% · 2,982 / 100%
- [offer] Should I add a post-purchase upsell and shipping protection? — 4,111 / 100% · 2,523 / 100%
- [store-audit] Audit my product page for conversion problems. — 5,991 / 100% · 3,398 / 100%
- [research] Is a $40 nail grinder with $8 COGS worth testing? — 3,869 / 100% · 1,373 / 100%
- [validate] Is the 'senior dog owners' sub-avatar big and distinct enough to targe — 2,763 / 100% · 3,521 / 0%
- [avatar] Find sub-avatars for a pet nail grinder. — 3,909 / 100% · 2,858 / 100%
- [offer] Plan my Black Friday offer and timing. — 4,111 / 100% · 2,902 / 100%
- [ops] Set up an email popup and the core automated flows. — 2,465 / 100% · 2,332 / 100%
