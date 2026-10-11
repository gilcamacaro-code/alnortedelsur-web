// Uso: NODE_PATH=$(npm root -g) node render.cjs <archivo.html> <carpeta_salida>
// Hace una captura JPG de 1080x1350 de cada <section class="s ..."> en orden: 1.jpg, 2.jpg...
const {chromium}=require('playwright');const path=require('path');(async()=>{
const [file,out]=process.argv.slice(2);require('fs').mkdirSync(out,{recursive:true});
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'}).catch(()=>chromium.launch());
const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+path.resolve(file));await p.waitForTimeout(800);
const secs=await p.$$('section.s');let i=0;
for(const s of secs){i++;await s.screenshot({path:path.join(out,i+'.jpg'),type:'jpeg',quality:92});}
console.log('imagenes:',i);await b.close();})();
