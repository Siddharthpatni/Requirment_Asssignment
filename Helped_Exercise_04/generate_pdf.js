const puppeteer = require('puppeteer');
const path = require('path');

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Generate main solution PDF
    const htmlPath1 = path.resolve(__dirname, 'Solution_Exercise_04.html');
    await page.goto(`file://${htmlPath1}`, { waitUntil: 'networkidle0' });
    await delay(2000);
    await page.pdf({
        path: path.resolve(__dirname, 'Nikunj_Exercise_04_Solution.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' }
    });
    console.log('PDF 1 generated: Nikunj_Exercise_04_Solution.pdf');

    // Generate Goal Model PDF
    const htmlPath2 = path.resolve(__dirname, 'Goal_Model.html');
    await page.goto(`file://${htmlPath2}`, { waitUntil: 'networkidle0' });
    await delay(2000);
    await page.pdf({
        path: path.resolve(__dirname, 'Nikunj_Exercise_04_Goal_Model.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' }
    });
    console.log('PDF 2 generated: Nikunj_Exercise_04_Goal_Model.pdf');

    await browser.close();
    console.log('All PDFs generated successfully!');
})();
