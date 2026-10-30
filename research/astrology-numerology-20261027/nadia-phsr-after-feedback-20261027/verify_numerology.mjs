// Research verification only. Imports the existing compiled asset without building it.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'../../..');
const staff=path.join(root,'work/staffprofiler-recreation/repository');
const engine=await import(pathToFileURL(path.join(staff,'assets/chart-engine.js')));
const indicators=await import(pathToFileURL(path.join(staff,'pattern-indicators.js')));
const frozen=JSON.parse(fs.readFileSync(path.join(here,'../nadia-sanchez-blind-trial/numerology.json'),'utf8'));
const failures=[];let months=0;
for(const record of frozen.records){
  const fresh=engine.buildPersonChart({FullName:'Nadia Sanchez',txtBirthdate:'17-07-1992'},record.calendar_year,0).years[0];
  for(const field of ['ess','py','com']){
    if(JSON.stringify(fresh[field])!==JSON.stringify(record[field]))failures.push({year:record.calendar_year,field});
    if(JSON.stringify(indicators.compoundAlert(fresh[field]))!==JSON.stringify(record.annual_alerts[field]))failures.push({year:record.calendar_year,field:field+'_alert'});
  }
  if(JSON.stringify(fresh.activeLetterOrdinals)!==JSON.stringify(record.active_letters))failures.push({year:record.calendar_year,field:'active_letters'});
  for(const month of record.months){
    const current=fresh.months.find(m=>m.monthIndex===month.month);months++;
    for(const field of ['pm','pme','mcom']){
      if(JSON.stringify(current[field])!==JSON.stringify(month[field]))failures.push({year:record.calendar_year,month:month.month,field});
    }
    if(JSON.stringify(indicators.patternIndicator(fresh,current,7,month.month-1))!==JSON.stringify(month.indicator))failures.push({year:record.calendar_year,month:month.month,field:'indicator'});
  }
}
const out={annual_states:frozen.records.length,monthly_states:months,full_compounds_formulas_and_letters_match:failures.length===0,failures,
  indicators_and_annual_alerts_match:failures.length===0,
  note:'No application build/test hooks executed. Frozen JSON was read only. Existing compiled arithmetic, annual alerts and monthly indicator functions re-executed without modification.'};
fs.writeFileSync(path.join(here,'numerology-reexecution-verification.json'),JSON.stringify(out,null,2)+'\n');
process.stdout.write(JSON.stringify(out));
if(failures.length)process.exitCode=1;
