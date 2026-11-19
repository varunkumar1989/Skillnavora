// Renders the handbook HTML to an A4 PDF with the browser that ships with this environment.
// Usage: node tools/aihandbook/render_pdf.js <input.html> <output.pdf>
const { chromium } = require('playwright');
const [, , input, output, mode, footerText] = process.argv;  // mode 'plain' = no header or footer; footerText optional
(async () => {
  const exe = '/opt/pw-browsers/chromium';
  const launch = require('fs').existsSync(exe) ? { executablePath: exe, args: ['--no-sandbox'] } : {};
  const b = await chromium.launch(launch);
  const p = await b.newPage();
  await p.goto('file://' + input, { waitUntil: 'load' });
  await p.emulateMedia({ media: 'print' });
  await p.pdf({
    path: output, format: 'A4', printBackground: true,
    margin: { top: '16mm', bottom: '18mm', left: '14mm', right: '14mm' },
    displayHeaderFooter: mode !== 'plain', headerTemplate: '<div></div>',
    footerTemplate: '<div style="font:8px Inter,sans-serif;color:#56607a;width:100%;text-align:center">' + (footerText || 'AI Master Course Handbook') + ' · SkillNavora · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
  });
  await b.close();
  console.log('pdf written', output);
})().catch(e => { console.error(e); process.exit(1); });
