const puppeteer = require('puppeteer');
const path = require('path');

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Generate PDF 1: Roles, Goals, BIM (Portrait A4, max 4 pages)
    console.log('Generating PDF 1: Roles, Goals, BIM...');
    const html1Path = path.resolve(__dirname, 'Submission_Roles_Goals_BIM.html');
    await page.goto(`file://${html1Path}`, { waitUntil: 'networkidle0' });
    await delay(2000);

    await page.pdf({
        path: path.resolve(__dirname, 'Patni_553265_Exercise04_RolesGoalsBIM.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '12mm', right: '12mm', bottom: '12mm', left: '12mm' }
    });
    console.log('PDF 1 generated: Patni_553265_Exercise04_RolesGoalsBIM.pdf');

    // Generate PDF 2: Goal Model Diagram (Landscape A4)
    console.log('Generating PDF 2: Goal Model Diagram...');
    const html2Path = path.resolve(__dirname, 'Submission_Goal_Model.html');
    await page.goto(`file://${html2Path}`, { waitUntil: 'networkidle0' });
    await delay(2000);

    await page.pdf({
        path: path.resolve(__dirname, 'Patni_553265_Exercise04_GoalModel.pdf'),
        format: 'A4',
        landscape: true,
        printBackground: true,
        margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' }
    });
    console.log('PDF 2 generated: Patni_553265_Exercise04_GoalModel.pdf');

    await browser.close();
    console.log('\n✓ Both PDFs ready for Moodle submission!');
})();
