// User-specified chart presentation rules; these do not compute matching scores.
const powers=[11,13,16];
const compoundText=value=>value.trail.join('/');
export const hasPatternPower=value=>Boolean(value?.trail?.some(n=>powers.includes(n)));
// Inspect numeric stages, never substrings or reconstructed powers from a root.
export function compoundAlert(value){
  const stages=(value?.trail||[]).flatMap((n,index)=>powers.includes(n)?[{marker:n,index,
    reductionInputs:index>0?String(value.trail[index-1]).split('').map(Number):null}]:[]);
  return {active:stages.length>0,markers:[...new Set(stages.map(s=>s.marker))],stages};
}
const iso=(year,month=1)=>`${year}-${String(month).padStart(2,'0')}-01`;
export function timelineCalculations(annual,month,personId='',identity=null){
  if(!annual||!month)return [];
  const year=annual.calendarYear,mi=month.monthIndex;
  const pmActive=month.pm.isPowerNumber?month.pm.raw:month.pm.root;
  const pmeActive=[11,22,33].includes(month.pme.raw)?month.pme.raw:month.pme.root;
  const inputs={PYE:annual.activeLetterOrdinals?.map(o=>o.value),COM:[annual.ess.raw,annual.py.raw],
    PY:identity?[identity.day,identity.month,annual.cy.root]:null,PM:[annual.py.root,month.cm],PME:[annual.ess.root,pmActive],MCOM:[pmeActive,pmActive]};
  return [['PYE',annual.ess],['PY',annual.py],['COM',annual.com],['PM',month.pm],['PME',month.pme],['MCOM',month.mcom]].map(([source,value])=>{
    const monthly=['PM','PME','MCOM'].includes(source),alert=compoundAlert(value);
    return {personId,source,year,month:monthly?mi:null,start:iso(year,monthly?mi:1),
      end:monthly?(mi===12?iso(year+1):iso(year,mi+1)):iso(year+1),
      endExclusive:true,inputs:inputs[source],rawFormula:value.rawFormula,raw:value.raw,trail:[...value.trail],root:value.root,...alert,
      components:inputs[source]?.length===2&&inputs[source].reduce((a,b)=>a+b,0)===value.raw?inputs[source]:null};
  });
}
export function annualBars(annual){
  return {topBar:hasPatternPower(annual?.ess)?'red':null,bottomBar:hasPatternPower(annual?.py)?'red':annual?.py?.root===9?'orange':null};
}
export function annualChartSummary(annual){
  if(!annual)return 'Personal chart unavailable.';
  return `PYE: ${compoundText(annual.ess)}\nCOM: ${compoundText(annual.com)}\nPY: ${compoundText(annual.py)}`;
}
export function periodChartSummary(annual,month){
  if(!annual||!month)return annualChartSummary(annual);
  const alerts=timelineCalculations(annual,month).filter(v=>v.active&&v.source!=='COM');
  return `${annualChartSummary(annual)}\nPM: ${compoundText(month.pm)}\nPME: ${compoundText(month.pme)}\nMCOM: ${compoundText(month.mcom)}\n${alerts.length?'Alerts: '+alerts.map(v=>`${v.source} (${v.markers.join(', ')})`).join('; '):'No compound alerts'}`;
}

export function patternIndicator(annual,month,birthMonth,monthIndex){
  if(!annual||!month||!Number.isInteger(birthMonth)||birthMonth<1||birthMonth>12){
    return {tone:'unavailable',leaf:false,topBar:null,bottomBar:null,reasons:['Personal chart unavailable.']};
  }
  const red=[],yellow=[];
  // The month fill represents monthly calculations. Annual signals have their
  // own PYE/PY bands; annual COM never repaints the monthly calculation.
  for(const [label,value] of [['PME',month.pme],['PM',month.pm],['MCOM',month.mcom]]){
    if(hasPatternPower(value))red.push(`${label} ${compoundText(value)} contains 11, 13 or 16`);
  }
  for(const [left,a,right,b] of [['PYE',annual.ess,'PY',annual.py],['PYE',annual.ess,'PM',month.pm],['PME',month.pme,'PY',annual.py],['PME',month.pme,'PM',month.pm]]){
    if(a?.root>0&&a.root===b?.root)yellow.push(`${left} ${compoundText(a)} mirrors ${right} ${compoundText(b)} (digit ${a.root})`);
  }
  return {tone:red.length?'red':yellow.length?'yellow':'green',leaf:monthIndex+1>=birthMonth,...annualBars(annual),
    redReasons:red,yellowReasons:yellow,
    reasons:red.length?red:yellow.length?yellow:['No red or yellow chart rule applies.']};
}
