import fs from 'fs';

const detailedData = JSON.parse(fs.readFileSync('../research/portfolio_detailed.json', 'utf8'));

// Create CSV export
let csv = 'Company,Slug,Website,FirstMark Partner,Location,Founders,About,FirstMark URL\n';

detailedData.forEach(company => {
  // Extract partner and location from about section
  const partnerMatch = company.about.match(/Partner:\s*([^\n]+)/);
  const locationMatch = company.about.match(/Location:\s*([^\n]+)/);

  const partner = partnerMatch ? partnerMatch[1].trim() : '';
  const location = locationMatch ? locationMatch[1].trim() : '';

  // Clean about text - remove partner/location lines and get the description
  let cleanAbout = company.about
    .replace(/Partner:.*?\n/g, '')
    .replace(/Location:.*?\n/g, '')
    .replace(/Exit:.*?\n/g, '')
    .trim()
    .replace(/"/g, '""'); // Escape quotes for CSV

  // Extract founders from details/about
  let founders = '';
  const foundersMatch = company.details.match(/Founders?\s*\n\s*\n\s*([A-Z][^\n]+)/);
  if (foundersMatch) {
    founders = foundersMatch[1].replace(/"/g, '""');
  }

  const name = company.name.replace(/"/g, '""');

  csv += `"${name}","${company.slug}","${company.website}","${partner}","${location}","${founders}","${cleanAbout}","${company.firstmarkUrl}"\n`;
});

fs.writeFileSync('../research/portfolio_export.csv', csv);

// Create markdown summary
let markdown = '# FirstMark Portfolio Companies - Complete Export\n\n';
markdown += `**Total Companies:** ${detailedData.length}\n`;
markdown += `**Generated:** ${new Date().toISOString().split('T')[0]}\n\n`;

markdown += '## Summary Statistics\n\n';

// Count companies by partner
const partnerCounts = {};
detailedData.forEach(company => {
  const partnerMatch = company.about.match(/Partner:\s*([^\n]+)/);
  if (partnerMatch) {
    const partner = partnerMatch[1].trim();
    partnerCounts[partner] = (partnerCounts[partner] || 0) + 1;
  }
});

markdown += '### Companies by Partner\n\n';
Object.entries(partnerCounts)
  .sort((a, b) => b[1] - a[1])
  .forEach(([partner, count]) => {
    markdown += `- **${partner}**: ${count} companies\n`;
  });

// Sample companies
markdown += '\n## Sample Company Data\n\n';
detailedData.slice(0, 5).forEach(company => {
  markdown += `### ${company.name}\n\n`;
  markdown += `- **Website:** ${company.website}\n`;
  markdown += `- **FirstMark URL:** ${company.firstmarkUrl}\n`;

  const partnerMatch = company.about.match(/Partner:\s*([^\n]+)/);
  if (partnerMatch) {
    markdown += `- **Partner:** ${partnerMatch[1].trim()}\n`;
  }

  const locationMatch = company.about.match(/Location:\s*([^\n]+)/);
  if (locationMatch) {
    markdown += `- **Location:** ${locationMatch[1].trim()}\n`;
  }

  const cleanAbout = company.about
    .replace(/Partner:.*?\n/g, '')
    .replace(/Location:.*?\n/g, '')
    .replace(/Exit:.*?\n/g, '')
    .trim();

  if (cleanAbout) {
    markdown += `\n${cleanAbout}\n`;
  }

  markdown += '\n---\n\n';
});

markdown += '\n## All Companies List\n\n';
detailedData.forEach((company, index) => {
  markdown += `${index + 1}. **${company.name}** - ${company.website}\n`;
});

fs.writeFileSync('../research/portfolio_summary.md', markdown);

console.log('✓ CSV export created: portfolio_export.csv');
console.log('✓ Summary document created: portfolio_summary.md');
console.log(`\nProcessed ${detailedData.length} companies`);
