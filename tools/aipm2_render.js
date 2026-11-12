// Renders the HTML jobs from aipm2_build.py to PDFs in the site folder. Usage: node aipm2_render.js JOBS_JSON PDF_DIR
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [jobsFile, outDir] = process.argv.slice(2);
  const jobs = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
  fs.mkdirSync(outDir, {recursive: true});
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const j of jobs) {
    await p.goto('file://' + j.src, {waitUntil: 'load'});
    await p.pdf({path: path.join(outDir, j.pdf), format: 'A4', printBackground: true,
      margin: {top: '16mm', bottom: '16mm', left: '15mm', right: '15mm'},
      displayHeaderFooter: true, headerTemplate: '<span></span>',
      footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888">SkillNavora · AI Product Management 2 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>'});
    console.log('pdf', j.pdf);
  }
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
