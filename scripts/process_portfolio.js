import fs from 'fs';

const rawData = JSON.parse(fs.readFileSync('../research/portfolio_raw.json', 'utf8'));

// Function to extract company information
function extractCompanyInfo(nameStr, slug) {
  const info = {
    name: '',
    tagline: '',
    ticker: '',
    exchange: '',
    acquisition: '',
    acquirer: ''
  };

  let text = nameStr.trim();

  // Extract stock ticker information
  const tickerMatch = text.match(/(NYSE|NASDAQ|LSE AIM|NASDQA):\s*([A-Z]+)/);
  if (tickerMatch) {
    info.exchange = tickerMatch[1];
    info.ticker = tickerMatch[2];
    text = text.replace(/(NYSE|NASDAQ|LSE AIM|NASDQA):\s*[A-Z]+/g, '');
  }

  // Extract acquisition information
  const acquisitionMatch = text.match(/Acquired(?:\s+by\s+(.+?))?$/i);
  if (acquisitionMatch) {
    info.acquisition = 'Yes';
    info.acquirer = acquisitionMatch[1] ? acquisitionMatch[1].trim() : '';
    text = text.replace(/Acquired(?:\s+by\s+.+?)?$/i, '');
  }

  // Clean up the remaining text
  text = text.trim().replace(/\s+/g, ' ');

  // Extract company name (last capitalized word/phrase)
  const lastCapitalizedMatch = text.match(/\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*$/);
  if (lastCapitalizedMatch && lastCapitalizedMatch[1]) {
    info.name = lastCapitalizedMatch[1];
    // Everything before the name is the tagline
    info.tagline = text.substring(0, text.lastIndexOf(info.name)).trim();
  } else {
    info.name = text || slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  // If name is empty or too short, use slug
  if (!info.name || info.name.length < 2) {
    info.name = slug.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  }

  return info;
}

// Remove duplicates and extract info
const seen = new Set();
const uniqueCompanies = rawData
  .map(c => {
    const info = extractCompanyInfo(c.name, c.slug);
    return {
      ...info,
      slug: c.slug,
      website: c.href
    };
  })
  .filter(c => {
    if (seen.has(c.slug)) return false;
    seen.add(c.slug);
    return true;
  })
  .sort((a, b) => a.name.localeCompare(b.name));

// Generate markdown table
let markdown = '# FirstMark Portfolio Companies\n\n';
markdown += `| # | Company | Tagline | Ticker | Exchange | Status | Acquirer | Website |\n`;
markdown += `|---|---------|---------|--------|----------|--------|----------|----------|\n`;

uniqueCompanies.forEach((company, index) => {
  const ticker = company.ticker || '-';
  const exchange = company.exchange || '-';
  const status = company.acquisition ? 'Acquired' : 'Active';
  const acquirer = company.acquirer || '-';
  const tagline = company.tagline || '-';

  markdown += `| ${index + 1} | ${company.name} | ${tagline} | ${ticker} | ${exchange} | ${status} | ${acquirer} | ${company.website} |\n`;
});

markdown += `\n\n**Total Companies:** ${uniqueCompanies.length}\n`;
markdown += `**Active:** ${uniqueCompanies.filter(c => !c.acquisition).length}\n`;
markdown += `**Acquired:** ${uniqueCompanies.filter(c => c.acquisition).length}\n`;
markdown += `**Public (with ticker):** ${uniqueCompanies.filter(c => c.ticker).length}\n`;
markdown += `\n*Generated on: ${new Date().toISOString().split('T')[0]}*\n`;

fs.writeFileSync('../research/portfolio_table.md', markdown);
console.log(`Generated markdown table with ${uniqueCompanies.length} companies`);
