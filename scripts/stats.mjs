// Builds assets/stats card (dist/stats.svg) from the GitHub GraphQL API.
// Runs in .github/workflows/profile.yml every 12 hours. Locally: GITHUB_TOKEN=… node scripts/stats.mjs
// Add a repo secret STATS_TOKEN (classic PAT, scopes: read:user, repo) to include private repos.
import fs from 'node:fs';

const USER = process.env.GITHUB_USER ?? 'StanK1';
const TOKEN = process.env.STATS_TOKEN || process.env.GITHUB_TOKEN;
const OUT = process.env.OUT_DIR ?? 'dist';

const QUERY = `query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    contributionsCollection {
      totalCommitContributions restrictedContributionsCount totalPullRequestContributions totalIssueContributions
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } }
    }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes { stargazerCount languages(first: 8, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
  }
}`;

async function load() {
  if (process.env.STATS_FIXTURE) return JSON.parse(fs.readFileSync(process.env.STATS_FIXTURE, 'utf8'));
  const res = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: { Authorization: `bearer ${TOKEN}`, 'Content-Type': 'application/json', 'User-Agent': 'profile-stats' },
    body: JSON.stringify({ query: QUERY, variables: { login: USER } }),
  });
  const json = await res.json();
  if (json.errors) throw new Error(JSON.stringify(json.errors));
  return json.data.user;
}

const FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Ubuntu,Helvetica,Arial,sans-serif";
const MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace";
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const fmt = n => n >= 1000 ? `${(n / 1000).toFixed(n >= 10000 ? 0 : 1)}k` : String(n);

function streaks(days) {
  let longest = 0, run = 0;
  for (const d of days) { run = d.contributionCount ? run + 1 : 0; longest = Math.max(longest, run); }
  // current streak: count back from today (today may still be empty)
  let current = 0;
  for (let i = days.length - 1; i >= 0; i--) {
    if (days[i].contributionCount) current++;
    else if (i === days.length - 1) continue;
    else break;
  }
  return { current, longest };
}

function render(u) {
  const c = u.contributionsCollection;
  const days = c.contributionCalendar.weeks.flatMap(w => w.contributionDays);
  const { current, longest } = streaks(days);
  const stars = u.repositories.nodes.reduce((a, r) => a + r.stargazerCount, 0);
  const langs = new Map();
  for (const r of u.repositories.nodes) for (const e of r.languages.edges) {
    const l = langs.get(e.node.name) ?? { size: 0, color: e.node.color ?? '#8A97A8' };
    l.size += e.size; langs.set(e.node.name, l);
  }
  const top = [...langs.entries()].sort((a, b) => b[1].size - a[1].size).slice(0, 6);
  const total = top.reduce((a, [, l]) => a + l.size, 0) || 1;

  const tiles = [
    ['Contributions', c.contributionCalendar.totalContributions, 'last 12 months', '#3DC593'],
    ['Commits', c.totalCommitContributions + c.restrictedContributionsCount, 'incl. private', '#7C6CFF'],
    ['Current streak', current, `days · best ${longest}`, '#FF8A3D'],
    ['Repositories', u.repositories.totalCount, `${fmt(stars)} ★ · ${c.totalPullRequestContributions} PRs`, '#4FB3FF'],
  ];
  const tileSvg = tiles.map(([label, val, sub, col], i) => {
    const x = 32 + i * 196;
    return `<g transform="translate(${x} 70)">
      <rect width="180" height="112" rx="16" fill="#FFFFFF" fill-opacity=".04" stroke="#FFFFFF" stroke-opacity=".08"/>
      <rect x="18" y="20" width="6" height="26" rx="3" fill="${col}"/>
      <text x="34" y="40" font-family="${FONT}" font-size="34" font-weight="800" fill="#EEF2F6">${fmt(val)}</text>
      <text x="18" y="74" font-family="${FONT}" font-size="14" font-weight="600" fill="#C9D3DF">${esc(label)}</text>
      <text x="18" y="94" font-family="${FONT}" font-size="12" fill="#6E7B8C">${esc(sub)}</text>
    </g>`;
  }).join('');

  // languages: one stacked bar + legend
  let bx = 0;
  const bar = top.map(([, l]) => { const w = (l.size / total) * 336; const r = `<rect x="${bx.toFixed(1)}" y="0" width="${w.toFixed(1)}" height="12" fill="${l.color}"/>`; bx += w; return r; }).join('');
  const legend = top.map(([name, l], i) => {
    const x = (i % 2) * 150, y = 12 + Math.floor(i / 2) * 34;
    return `<circle cx="${x + 6}" cy="${y - 4}" r="5" fill="${l.color}"/><text x="${x + 18}" y="${y}" font-family="${FONT}" font-size="13" fill="#C9D3DF">${esc(name)} <tspan fill="#6E7B8C">${((l.size / total) * 100).toFixed(0)}%</tspan></text>`;
  }).join('');

  // heatmap: last 26 weeks, 7 rows
  const weeks = c.contributionCalendar.weeks.slice(-53);
  const max = Math.max(1, ...weeks.flatMap(w => w.contributionDays.map(d => d.contributionCount)));
  const ramp = ['#161E2E', '#0E4D3A', '#14805E', '#2BB07F', '#5BE3AE'];
  const cells = weeks.map((w, wi) => w.contributionDays.map((d, di) => {
    const lvl = d.contributionCount === 0 ? 0 : Math.min(4, 1 + Math.floor((d.contributionCount / max) * 3.999));
    return `<rect x="${(wi * 14.6).toFixed(1)}" y="${di * 13.4}" width="10.5" height="10.5" rx="2.5" fill="${ramp[lvl]}"><title>${d.date}: ${d.contributionCount}</title></rect>`;
  }).join('')).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="330" viewBox="0 0 1200 330" role="img" aria-label="GitHub stats for ${USER}">
  <defs>
    <linearGradient id="sg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B0F19"/><stop offset="1" stop-color="#121A2B"/></linearGradient>
    <linearGradient id="sline" x1="0" x2="1"><stop offset="0" stop-color="#3DC593"/><stop offset=".5" stop-color="#7C6CFF"/><stop offset="1" stop-color="#FF8A3D"/></linearGradient>
    <clipPath id="barclip"><rect width="336" height="12" rx="6"/></clipPath>
  </defs>
  <rect width="1200" height="330" rx="24" fill="url(#sg)"/>
  <rect x="32" y="0" width="1136" height="3" fill="url(#sline)"/>
  <text x="32" y="46" font-family="${FONT}" font-size="20" font-weight="800" fill="#EEF2F6">GitHub, in numbers</text>
  <text x="250" y="46" font-family="${MONO}" font-size="12" fill="#6E7B8C">updated ${new Date().toISOString().slice(0, 10)} · @${USER}</text>
  ${tileSvg}
  <g transform="translate(32 214)">
    <text x="0" y="0" font-family="${FONT}" font-size="14" font-weight="600" fill="#C9D3DF">Last 12 months</text>
    <g transform="translate(0 14)">${cells}</g>
  </g>
  <g transform="translate(832 70)">
    <rect width="336" height="230" rx="16" fill="#FFFFFF" fill-opacity=".04" stroke="#FFFFFF" stroke-opacity=".08"/>
    <text x="20" y="34" font-family="${FONT}" font-size="14" font-weight="600" fill="#C9D3DF">Languages I write most</text>
    <g transform="translate(20 52)"><g clip-path="url(#barclip)" transform="scale(${296 / 336} 1)">${bar}</g></g>
    <g transform="translate(20 92)">${legend}</g>
  </g>
</svg>`;
}

const u = await load();
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(`${OUT}/stats.svg`, render(u));
console.log(`wrote ${OUT}/stats.svg`);
