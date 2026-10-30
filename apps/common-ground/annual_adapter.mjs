import fs from 'node:fs';
import {buildPersonChart} from './vendor/staff/chart-engine.mjs';
import {compoundAlert,patternIndicator} from './vendor/staff/pattern-indicators.mjs';
const catalogue=JSON.parse(fs.readFileSync(new URL('./data/annual-catalogue.json',import.meta.url),'utf8'));
const input=JSON.parse(fs.readFileSync(0,'utf8'));
function meaning(category,value){
  for(const number of [...new Set([value.raw,...value.trail,value.root])]){
    const text=catalogue[category]?.[number];
    if(text)return {category,number,text,exact:number===value.raw,source_status:'REPOSITORY_AUTHORED_VOCABULARY'};
  }
  return {category,number:null,text:null,exact:false};
}
const chart=buildPersonChart({FullName:input.name,txtBirthdate:input.birth_date.split('-').reverse().join('-')},input.year,0);
const annual=chart.focus;
const roles={ess:'Essence',py:'Personal Year',com:'Combiner'};
const result={method_id:'staff-annual-4172789-v1',source_commit:'4172789db1034072f50c78178187e839fa710fb5',
  year:input.year,name_basis:input.name,name_policy:'BIRTH_NAME_SCENARIO',boundary:'January 1; end exclusive January 1 of next year',
  letter_cycle_age:annual.age,active_letters:annual.activeLetterOrdinals,
  fields:Object.fromEntries(Object.entries(roles).map(([key,category])=>[key,{...annual[key],meaning:meaning(category,annual[key]),alert:compoundAlert(annual[key])}])),
  months:annual.months.map((m,i)=>({month:i+1,pm:m.pm,pme:m.pme,mcom:m.mcom,indicator:patternIndicator(annual,m,chart.identity.month,i)})),
  personal_report_approved:false};
process.stdout.write(JSON.stringify(result));
