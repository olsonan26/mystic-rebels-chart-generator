'use strict';
let researchVersion=0;
function researchHtml(data){
 const r=data.reading,a=data.annual,packet=data.assessment;
 const cards=Object.entries(a.fields).map(([key,v])=>'<article class="number-card"><h4>'+esc({ess:'Essence · experience',py:'Personal Year · cycle',com:'Combiner · approach'}[key])+'</h4><strong>'+esc(v.trail.join('/'))+'</strong><p>'+esc(key==='com'?'How to approach matters in this year.':key==='ess'?'Present frame of mind and experiential themes.':'The yearly cycle in the selected method.')+'</p><details><summary>Category-specific source text</summary><p class="catalogue-note">Adult reference wording; this is not an established biography or an approved child-specific interpretation.</p><p class="catalogue-text">'+esc(v.meaning.text||'No source entry is available.')+'</p><p>'+esc(v.rawFormula)+'</p></details></article>').join('');
 const route=r.root_route.path.concat(r.root_route.repeat?[r.root_route.repeat+' (repeat)']:[]);
 const nodes=Object.values(packet.assessments).map(n=>'<details class="method-details"><summary>'+esc(n.id+' · '+n.position+' · '+(n.house?'H'+n.house:'house unavailable'))+'</summary>'+n.stages.map(s=>'<section class="assessment-stage"><h5>'+esc(s.stage[0].toUpperCase()+s.stage.slice(1))+' <small>'+esc(s.status.replaceAll('_',' '))+'</small></h5><p>'+esc(s.meaning||'')+'</p><pre>'+esc(JSON.stringify(s,null,2))+'</pre></section>').join('')+'<h5>Delegate occupants</h5><pre>'+esc(JSON.stringify(n.delegate_payload,null,2))+'</pre></details>').join('');
 const months='<details class="method-details"><summary>Optional monthly calculations</summary><div class="table-scroll"><table><thead><tr><th>Month</th><th>PM</th><th>PME</th><th>MCOM</th><th>Indicator</th></tr></thead><tbody>'+a.months.map(m=>'<tr><td>'+m.month+'</td><td>'+esc(m.pm.trail.join('/'))+'</td><td>'+esc(m.pme.trail.join('/'))+'</td><td>'+esc(m.mcom.trail.join('/'))+'</td><td>'+esc(m.indicator.tone)+': '+esc(m.indicator.reasons.join('; '))+'</td></tr>').join('')+'</tbody></table></div><p>These are symbolic calculation markers, not probabilities of harm. Annual bands and monthly colors are separate.</p></details>';
 return '<article class="research-reading"><span class="research-label">Conditional research reflection</span><h4>'+esc(r.title)+'</h4><p class="subtle">'+esc(r.scope)+'</p>'+r.paragraphs.map(p=>'<p>'+esc(p)+'</p>').join('')+'<p class="reflection">'+esc(r.question)+'</p></article><div class="number-grid">'+cards+'</div><p>'+esc(a.year+' · '+a.name_basis+' · birth-name scenario · yearly values change on January 1.')+'</p>'+months+'<details class="method-details"><summary>Explain the ordered assessment</summary><p>'+esc(packet.stage_order.join(' → '))+'</p><p>'+esc(route.join(' → '))+'</p><p>Sign-ruler links are distinct from decan refinements and directed aspects. Missing rules remain visible.</p>'+nodes+'<h4>Source decisions still open</h4><ul>'+Object.entries(packet.decisions).map(([id,t])=>'<li>'+esc(id+': '+t)+'</li>').join('')+'</ul></details>';
}
async function loadResearch(){
 if(!state.result)return;
 const version=++researchVersion,year=Number($('research-year').value);
 if(!Number.isInteger(year)){ $('research-status').textContent='Choose a whole-number year.';return; }
 $('research-status').textContent='Following the ruler connections and calculating the year…';
 $('research-button').disabled=true;
 try{
  const profile=state.result.profile;
  const input={full_name:profile.full_name,birth_date:profile.birth_date,birth_time:profile.birth_time,
   time_accuracy:profile.time_accuracy,latitude:profile.latitude,longitude:profile.longitude,
   timezone:profile.timezone,location_name:profile.location_name,coordinate_provenance:profile.coordinate_provenance,
   uncertainty_seconds:profile.uncertainty_seconds,fold:profile.fold,year,topic:$('research-topic').value};
  const response=await fetch('/api/research',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(input)});
  const data=await response.json();if(version!==researchVersion)return;
  if(!response.ok)throw new Error(data.error?.message||'The assessment could not be created.');
  state.result.research=data;$('research-result').innerHTML=researchHtml(data);
  $('research-status').textContent='Assessment ready. Degree meaning and directed aspects remain explicitly incomplete.';
 }catch(e){if(version===researchVersion){delete state.result.research;$('research-result').replaceChildren();$('research-status').textContent=e.message;}}
 finally{if(version===researchVersion)$('research-button').disabled=false;}
}
document.addEventListener('comparison-ready',()=>{
 researchVersion++;delete state.result.research;$('research-result').replaceChildren();
 $('research-year').value=Math.max(Number(state.result.profile.birth_date.slice(0,4)),Number(new Intl.DateTimeFormat('en',{year:'numeric',timeZone:'America/Denver'}).format(new Date())));
 loadResearch();
});
$('research-button').addEventListener('click',loadResearch);
$('research-topic').addEventListener('change',loadResearch);
window.researchReadingHtml=()=>state.result?.research?'<section><h2>Ordered assessment and yearly direction</h2>'+researchHtml(state.result.research)+'</section>':'';
