#!/usr/bin/env node

import puppeteer from 'puppeteer-core';
import fs from 'fs';

// Read the portfolio data from research directory
const rawData = JSON.parse(fs.readFileSync('../research/portfolio_raw.json', 'utf8'));

// Remove duplicates
const seen = new Set();
const uniqueCompanies = rawData.filter(c => {
  if (seen.has(c.slug)) return false;
  seen.add(c.slug);
  return true;
});

console.log(`Found ${uniqueCompanies.length} unique companies to scrape`);

async function scrapeCompanyPage(page, company) {
  try {
    console.log(`\nScraping: ${company.name} (${company.href})`);

    await page.goto(company.href, {
      waitUntil: 'domcontentloaded',
      timeout: 30000
    });

    // Wait a bit for dynamic content to load
    await new Promise(r => setTimeout(r, 2000));

    // Extract company information
    const companyData = await page.evaluate(() => {
      const data = {
        website: '',
        details: '',
        founders: [],
        about: '',
        socialLinks: {},
        tags: [],
        status: ''
      };

      // Try to find the company website link
      const websiteLink = document.querySelector('a[href*="http"]:not([href*="firstmark.com"]):not([href*="linkedin.com"]):not([href*="twitter.com"])');
      if (websiteLink) {
        data.website = websiteLink.href;
      }

      // Extract about/description text
      const aboutSection = document.querySelector('p, .description, .about');
      if (aboutSection) {
        data.about = aboutSection.textContent.trim();
      }

      // Try to find all paragraphs as potential description
      const paragraphs = Array.from(document.querySelectorAll('p'));
      if (paragraphs.length > 0) {
        data.about = paragraphs
          .map(p => p.textContent.trim())
          .filter(text => text.length > 50)
          .join('\n\n');
      }

      // Extract founders information
      const founderElements = document.querySelectorAll('[class*="founder"], [class*="team"]');
      founderElements.forEach(el => {
        const founderName = el.textContent.trim();
        if (founderName && founderName.length < 100) {
          data.founders.push(founderName);
        }
      });

      // Extract tags/categories
      const tagElements = document.querySelectorAll('[class*="tag"], [class*="category"], [class*="label"]');
      tagElements.forEach(el => {
        const tag = el.textContent.trim();
        if (tag && tag.length < 50 && !data.tags.includes(tag)) {
          data.tags.push(tag);
        }
      });

      // Extract social media links
      const linkedinLink = document.querySelector('a[href*="linkedin.com"]');
      if (linkedinLink) {
        data.socialLinks.linkedin = linkedinLink.href;
      }

      const twitterLink = document.querySelector('a[href*="twitter.com"], a[href*="x.com"]');
      if (twitterLink) {
        data.socialLinks.twitter = twitterLink.href;
      }

      // Extract status (Active, Acquired, etc.)
      const statusElement = document.querySelector('[class*="status"]');
      if (statusElement) {
        data.status = statusElement.textContent.trim();
      }

      // Get all text content for details
      const mainContent = document.querySelector('main, article, .content');
      if (mainContent) {
        data.details = mainContent.textContent.trim().substring(0, 1000);
      }

      return data;
    });

    console.log(`  ✓ Scraped: ${companyData.website || 'No website found'}`);

    return {
      slug: company.slug,
      name: company.name,
      firstmarkUrl: company.href,
      ...companyData,
      scrapedAt: new Date().toISOString()
    };

  } catch (error) {
    console.error(`  ✗ Error scraping ${company.name}: ${error.message}`);
    return {
      slug: company.slug,
      name: company.name,
      firstmarkUrl: company.href,
      error: error.message,
      scrapedAt: new Date().toISOString()
    };
  }
}

async function main() {
  console.log('Connecting to Chrome on :9222...');

  const browser = await puppeteer.connect({
    browserURL: 'http://localhost:9222',
    defaultViewport: null
  });

  const pages = await browser.pages();
  const page = pages[0] || await browser.newPage();

  const results = [];

  // Process companies in batches to avoid overwhelming the server
  const batchSize = 5;
  for (let i = 0; i < uniqueCompanies.length; i += batchSize) {
    const batch = uniqueCompanies.slice(i, i + batchSize);
    console.log(`\n--- Processing batch ${Math.floor(i/batchSize) + 1}/${Math.ceil(uniqueCompanies.length/batchSize)} ---`);

    for (const company of batch) {
      const data = await scrapeCompanyPage(page, company);
      results.push(data);

      // Small delay between requests
      await new Promise(r => setTimeout(r, 1000));
    }

    // Save progress after each batch to research directory
    fs.writeFileSync('../research/portfolio_detailed.json', JSON.stringify(results, null, 2));
    console.log(`\nProgress saved: ${results.length}/${uniqueCompanies.length} companies`);
  }

  console.log('\n✓ Scraping complete!');
  console.log(`Results saved to: portfolio_detailed.json`);
  console.log(`Total companies scraped: ${results.length}`);
  console.log(`Successful: ${results.filter(r => !r.error).length}`);
  console.log(`Failed: ${results.filter(r => r.error).length}`);

  await browser.disconnect();
}

main().catch(console.error);
