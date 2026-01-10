const puppeteer = require('puppeteer');
const path = require('path');

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Goal Model PDF (Landscape)
    console.log('Generating AOM_Goal_Model.pdf...');
    await page.goto(`file://${path.resolve(__dirname, 'AOM_Goal_Model.html')}`, { waitUntil: 'networkidle0' });
    await delay(2000);
    await page.pdf({
        path: path.resolve(__dirname, 'AOM_Goal_Model.pdf'),
        format: 'A4',
        landscape: true,
        printBackground: true,
        margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' }
    });

    // BIM PDF (Portrait)
    console.log('Generating AOM_BIM.pdf...');
    await page.goto(`file://${path.resolve(__dirname, 'AOM_BIM.html')}`, { waitUntil: 'networkidle0' });
    await delay(2000);
    await page.pdf({
        path: path.resolve(__dirname, 'AOM_BIM.pdf'),
        format: 'A4',
        printBackground: true,
        margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' }
    });

    await browser.close();
    console.log('✓ Both AOM PDFs generated!');
})();
