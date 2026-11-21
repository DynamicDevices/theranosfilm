# Search and AI discovery

The release builder emits static, readable HTML, unique titles/descriptions,
canonical and Open Graph URLs, JSON-LD WebSite/Article metadata, a sitemap and
root robots.txt. `llms.txt` is an optional navigation aid, not an established
ranking signal or a promise that any model will cite this project.

Use `python3 build_site.py --base-url https://theranosfilm.com --output NEW_DIR`.
The output directory must not already exist. Only explicitly allowlisted files
are copied; never deploy the repository directory or its private parent.
Local source pages intentionally retain noindex until a reviewed release is
deployed. Do not submit a localhost URL or an unreviewed draft to search engines.

Indexability is not indexing. Search Console/Bing verification and sitemap
submission require the actual authenticated account and separate applicable
authority. No fake reviews, reputation scores, hidden keywords, invented author
credentials, automatic mass pages or guarantees of ranking/agency engagement.
Keep visible conclusions consistent with structured data. Do not label open
questions as verified facts or use official agency branding to attract attention.

Canonical address: https://theranosfilm.com/ after verified deployment. Redirect
HTTP and the chosen alternate hostname to that address when supported. Verify
robots, redirects, TLS, canonical URLs and asset loading on the actual host.
Changing canonical URLs does not itself migrate traffic or prove redirects.

Assisted-by: Briar.
